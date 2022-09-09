from fastapi import  APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db import get_db
from ..import schema,model
from .import utils,oAuth2

router=APIRouter(
    tags=['Login']
)

@router.post("/register",status_code=status.HTTP_201_CREATED,response_model=schema.user_response)
def register(data:schema.register,db:Session=Depends(get_db)):
    data.password=utils.hash(data.password)
    new_user=model.user(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@router.post("/loginC")
def login(data:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    login_data=db.query(model.user).filter(model.user.email==data.username).first()
    if not login_data :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    check=utils.verify(data.password,login_data.password)
    if check:
       
        return {"status":"success"}
    else :
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    
@router.post("/login",response_model=schema.token)
def login(data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    login_data=db.query(model.user).filter(model.user.email==data.username).first()
    if not login_data :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    check=utils.verify(data.password,login_data.password)
    if check:
        token_data = oAuth2.createToken(userData= {"id":login_data.id})
        return {"access_token":token_data,"token_type":"bearer"}
    else :
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")    