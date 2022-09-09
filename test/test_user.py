from API import schema
from jose import jwt
from API.config import setting
import pytest

def test_root(client):
    res=client.get('/')
    print(res.json())
    assert res.status_code == 200
    
def test_register_user(client):
    res = client.post('/register',json={'email':'ravi@gmail.com',"password":"ravi"})
    new_user=schema.user_response(**res.json())
    assert res.status_code ==  201
    assert new_user.email == "ravi@gmail.com"
    
def test_login(client , testUser):
    res = client.post('/login' , data={"username":testUser['email'],"password":testUser['password']})
    login = schema.token(**res.json())
    assert res.status_code==200
    id = jwt.decode(login.access_token , setting.secret_key , algorithms=[setting.algorithm])  
    assert id['id'] == testUser['id']
    assert login.token_type=='bearer'  

@pytest.mark.parametrize("email,password,status_code",[('ravi@gmail.com','ravishnu',404),("ravi","ravi",404),(None,"ravi",422),("ravi@gmail.com",None,422)])
def test_invalid_login(client , email , password , status_code):
    res = client.post("/login",data={"username":email,"password":password})
    assert res.status_code == status_code    
    # assert res.json().get('detail') == "Invalid Credentials"
    

        
    