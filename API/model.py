from sqlalchemy import Column, Integer,String,Boolean ,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .db import Base
from sqlalchemy.orm import relationship
    
class user(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False ,unique=True )
    password=Column(String,nullable=False)
    time=Column(TIMESTAMP,nullable=False,server_default=text('now()'))

class Post(Base):
    __tablename__="posts"
    
    id=Column(Integer,primary_key=True,nullable=False)
    ower_id = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    run=Column(Boolean,server_default='True')
    
    owner = relationship("user")
    
class vote(Base):    
    __tablename__ = "votes"
    user_id = Column(Integer  , ForeignKey("users.id" , ondelete="CASCADE") ,primary_key= True , nullable = False)
    post_id = Column(Integer , ForeignKey("posts.id" , ondelete="CASCADE"),primary_key= True , nullable = False)

# class Sample(Base):
#     __tablename__ = "Sample"
#     id  =Column(Integer, primary_key=True , nullable=False)
#     name = Column(String , nullable=False)
#     age = Column(String , nullable = False)
#     date = Column(TIMESTAMP , server_default = ( 'text(now()'))