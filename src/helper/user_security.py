import bcrypt
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Union
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from config.config import get_configs
from src.database.mongo import getDB
from src.models.user import TokenData, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def generate_salt():
    return bcrypt.gensalt().decode()


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    config = get_configs()
    print(config)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=2)
    to_encode.update({"exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode,config.jwt_secrete_key, algorithm=config.jwt_algorithm)
    return encoded_jwt

