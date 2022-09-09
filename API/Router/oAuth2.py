from datetime import datetime, timedelta
from jose import JWTError,jwt
from fastapi import Depends,status,HTTPException
from API import model
from ..import schema,db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..config import setting

oAuth= OAuth2PasswordBearer(tokenUrl="login" )

#needed secret_key ,Algorithm, data, expire time
secter_key=setting.secret_key
Algorithm=setting.algorithm
expire=setting.token_expiration

def createToken(userData:dict):
    to_encode =userData.copy()  # make copy of data
    ExpireTime=datetime.utcnow()+timedelta(minutes=expire) #set expire time in date format
    to_encode.update({"exp":ExpireTime}) #add expire time with user data
    
    encoded = jwt.encode(to_encode,secter_key, algorithm=Algorithm) #encode using jwt function
    
    return encoded #return the data

def verify_token(token,credential_exception):
    try:
        payload=jwt.decode(token,secter_key,algorithms=[Algorithm])
        id=payload.get("id")
        print(id)
        if id is None:
            raise credential_exception
        token_data =schema.token_data(id=id)
        print("token",token_data)
    except JWTError:
        raise credential_exception
    
    return token_data
    
def current_user(token:str = Depends(oAuth)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not a valid user",headers={"www-Authenticate":"bearer"})
    return  verify_token(token,credential_exception)
    
    