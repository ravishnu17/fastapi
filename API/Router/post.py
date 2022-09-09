from fastapi import Depends,status,HTTPException,Response,APIRouter
from sqlalchemy.orm import Session
from..import model,schema
from ..db import get_db
from .import oAuth2
from typing import List, Optional
from sqlalchemy import  func

router=APIRouter(
    prefix='/get',
    tags=['post']
)


#display all post
@router.get('/posts',response_model=List[schema.VoteCount])
def posts( limit:int = 5 ,skip : int = 0 , search:Optional[str]='' , db:Session=Depends(get_db)):
    # data=db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    data = db.query(model.Post ,func.count(model.vote.post_id).label("votes") ).join(model.vote , model.Post.id == model.vote.post_id , isouter = True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return data

#create a post
@router.post('/newpost',status_code=status.HTTP_201_CREATED,response_model=schema.out)
def crtpost(data :schema.Post,db:Session=Depends(get_db),get_user = Depends(oAuth2.current_user)):
    new_data=model.Post(ower_id = get_user.id , **data.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

#get particular post by owner id
@router.get("/owner",response_model=List[schema.VoteCount])
def post(db:Session=Depends(get_db),get_user = Depends(oAuth2.current_user)):
    print(get_user.id)
    data = db.query(model.Post ,func.count(model.vote.post_id).label("votes") ).join(model.vote , model.Post.id == model.vote.post_id , isouter = True).group_by(model.Post.id).filter(model.Post.ower_id == get_user.id).all()    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} was not found")
       
    return data

#get particular post
@router.get("/post/{id}" , response_model=List[schema.VoteCount])
def post(id:int,db:Session=Depends(get_db),get_user = Depends(oAuth2.current_user)):
    print(get_user.id)
    data = db.query(model.Post ,func.count(model.vote.post_id).label("votes") ).join(model.vote , model.Post.id == model.vote.post_id , isouter = True).group_by(model.Post.id).filter(model.Post.id == id).all()    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} was not found")
       
    return data

    
#delete data      
@router.delete("/{id}")
def delete(id:int,db:Session=Depends(get_db) , get_user = Depends(oAuth2.current_user)):
    print(id)
    data=db.query(model.Post).filter(model.Post.id==id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} not exist")
    
    if data.first().ower_id != get_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Unauthorized operation")
    else:
        data.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
       
#update post data
@router.put("/{id}",response_model=schema.VoteCount)
def update(id:int,data:schema.Post,db:Session=Depends(get_db) ,get_user = Depends(oAuth2.current_user)):
    fetch_data=db.query(model.Post).filter(model.Post.id==id)
    if not fetch_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Id {id} not exists")
    
    print(id , fetch_data.first().ower_id ,get_user.id , (fetch_data.first().ower_id != get_user.id))
    
    if (fetch_data.first().ower_id) != get_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Unauthorized operation")
    print(id,data.dict())
    fetch_data.update(data.dict(),synchronize_session=False)
    db.commit()
    
    data = db.query(model.Post , func.count(model.vote.post_id).label("votes")).join(model.vote , model.vote.post_id == model.Post.id , isouter = True).group_by(model.Post.id).filter(model.Post.id == id).first()    
    return data