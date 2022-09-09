from fastapi import APIRouter , Depends ,HTTPException,status
from ..import db ,schema , model
from .import oAuth2
from sqlalchemy.orm import Session

root = APIRouter(
    tags=['Vote']
)

@root.post("/vote")
def vote(vote : schema.vote , db:Session = Depends(db.get_db) , current_user = Depends(oAuth2.current_user)):
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Post not found")
    vote_data = db.query(model.vote).filter(model.vote.post_id ==vote.post_id , model.vote.user_id == current_user.id)
    found = vote_data.first()
    if vote.dir == 1 :
        if found :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT ,detail="You Already voted")
        new = model.vote(post_id = vote.post_id , user_id = current_user.id)
        db.add(new)
        db.commit()
        return {"msg":f"You voted for post id {vote.post_id}"}
    else :
        if not found :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="You didn't vote")
        vote_data.delete(synchronize_session=False)
        db.commit()
        return {"msg":f"Vote removed for this id {vote.post_id}"}
    