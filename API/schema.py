from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional

class Post(BaseModel):
    title:str
    content:str
    run:bool=True
    
    
class user_response(BaseModel):
    email: EmailStr
    id: int
    class Config:
        orm_mode=True    
    
class out(BaseModel):
    id :int
    title: str
    content: str
    ower_id : int
    owner : user_response
    class Config:
        orm_mode=True
        
class VoteCount(BaseModel):
    Post : out
    votes : int  
    class Config:
        orm_mode=True      
        
class register(BaseModel):
    email: EmailStr
    password:str
        
class login(BaseModel):
    email: EmailStr
    password:str
    class Config:
        orm_mode=True   
     
class token(BaseModel):
    access_token:str
    token_type: str
    class Config:
        orm_mode=True
    
class token_data(BaseModel):
    id : Optional[int]=None
    
class vote (BaseModel):
    post_id : int
    dir : int    