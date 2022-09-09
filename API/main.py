from fastapi import FastAPI
from .import model
from .db import engine
from .Router import post,login  , vote


app=FastAPI()
app.include_router(post.router)
app.include_router(login.router)
app.include_router(vote.root)
    
# model.Base.metadata.create_all(bind=engine)    
    
 

@app.get("/")
def root():
    return {'message':'Fastapi run successfully'}

