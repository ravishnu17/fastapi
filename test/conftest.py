import json
from fastapi.testclient import TestClient
from API import model
from API.main import app
from API.config import setting
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine    
from API.db import get_db ,Base
import pytest
from API.Router.oAuth2 import createToken


SQLALCHEMY_DATABASE_URL=f'postgresql://{setting.db_username}:{setting.db_password}@{setting.db_host}:{setting.db_port}/{setting.db_name}api_test' #'://user:password@host/db_name'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal_test=sessionmaker(autocommit=False,autoflush=False,bind=engine)


# @pytest.fixture
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db=SessionLocal_test()
    
#     try:
#         yield db
#     finally:
#         db.close()    
    

@pytest.fixture()
def client():    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=SessionLocal_test()
    def getTest_db():
        try:
            yield db
        finally:
            db.close()    
    app.dependency_overrides[get_db]=getTest_db
    
    yield TestClient(app)
    
@pytest.fixture
def testUser(client):
    userData = {"email":"ravi@gmail.com","password":"ravi"}
    res=client.post("/register",json=userData)
    assert res.status_code == 201
    
    testUser = res.json()
    testUser['password']=userData['password']
    return testUser

@pytest.fixture
def token(testUser):
    return createToken({"id":testUser['id']}) 


@pytest.fixture
def authorized_client(client , token):
    client.headers = {**client.headers,"Authorization":f"bearer {token}"}
    return client

@pytest.fixture
def testPost(authorized_client , testUser):
    post_data=[{"title":"C","content":"Basic","ower_id":testUser['id'],"run":False},{"title":"C++","content":"OOPS","ower_id":testUser['id']}]
    # def add_post(post):
    #     return  model.Post(**post)
    # mapPost = map(add_post , post_data)
    
    # post = list(mapPost)
    # session.add_all(post)
    # session.commit()
    res = authorized_client.post("/get/newpost",json = post_data)
    testpost = res.json()
    return testpost
    # return session.query(model.Post).all()