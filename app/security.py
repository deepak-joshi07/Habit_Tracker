import uuid
from passlib.hash import pbkdf2_sha256
from passlib.utils import saslprep
from .models import UserModel
from datetime import datetime
from sqlmodel import select 


def hash_password(password):
    normalised = saslprep(password)
    hashed = pbkdf2_sha256.hash(normalised)
    return hashed

def create_user(username , email , password, session ):
    existing_user = session.exec(
    select(UserModel)
    .where(UserModel.username == username)
        ).first()
    
    if existing_user:
        raise ValueError("Username already exists")
     
    existing_email = session.exec(
    select(UserModel)
    .where(UserModel.email == email)
        ).first()
    
    if existing_email:
        raise ValueError("Email already exists")
    
    user_id = str(uuid.uuid4())
    hashed = hash_password(password)

    

    user = UserModel(user_id = user_id , username=username , email=email , hashed_password = hashed)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def verify_password(password ,email, session):
    details = session.exec(
        select(UserModel)
        .where(UserModel.email == email)
        ).first()
    if not details:
        return False
    passw = details.hashed_password
    normalised = saslprep(password)
    return pbkdf2_sha256.verify(normalised , passw)

    
        
