from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

from dotenv import load_dotenv
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")

pwd_context = CryptContext(
    schemes=["argon2", "pbkdf2_sha256"],
    default="argon2",
)

def hash_password(password: str) -> str:
    passwd = pwd_context.hash(password)
    return passwd

def check_password(password:str, hashed_password:str) -> bool:
    is_match = pwd_context.verify(password, hashed_password)
    return is_match

#create authorization token using JWT for login
def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



