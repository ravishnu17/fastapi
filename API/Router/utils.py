from passlib.context import CryptContext

pwd=CryptContext(schemes=['bcrypt'],deprecated='auto')

def hash(password:str):
    return pwd.hash(password)

def verify(plain_pwd,hash_pwd):
    return pwd.verify(plain_pwd,hash_pwd)