import jwt
from datetime import timedelta , datetime , timezone
from fastapi import Depends , HTTPException
from jwt.exceptions import InvalidTokenError
from sqlmodel import select , Session
from .db import get_session
from .models import UserModel
from .security import verify_password
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "1e82c2a1e01b2c30a20704199aae60c9d376e3bb130efc4217cd8aed915f9ff7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def authenticate_user(password, email,session):
    valid_user = session.exec(
    select(UserModel)
    .where(UserModel.email == email)
).first()

    if not valid_user:
        return False

    if not verify_password(
         password,
         valid_user.hashed_password
    ):
        return False

    return valid_user

def create_access_token(data:dict , expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm= ALGORITHM)
    return encode_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except InvalidTokenError:
        return None

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl= "/login"
)


def get_current_user(token: str = Depends(oauth2_scheme),session: Session = Depends(get_session)):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    user = session.exec(
        select(UserModel)
        .where(UserModel.email == email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user