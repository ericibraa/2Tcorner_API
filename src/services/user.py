from fastapi import Body, Depends, Request, HTTPException, status
from typing  import List, Union, Annotated
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from config.config import get_configs
from src.database.mongo import getDB
from src.models.user import User, TokenData, UserForm
from src.models.response_model import LoginResponse
from src.models.query_paramater import QueryParameter
from motor.core import AgnosticDatabase
from src.helper.user_security import verify_password, create_access_token, get_password_hash
from bson import ObjectId
import jwt
from jwt.exceptions import InvalidTokenError 
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", )


async def getAllUser(db : AgnosticDatabase, query : QueryParameter ) -> List[User]:
    match = {}
    skip = 0
    if query.search :
        match["email"] = query.search
    
    if query.page:
        skip = (query.page -1) * query.limit

    print(skip) 
    print(query.page)

    users = await db.user.find(match).limit(query.limit).skip(skip).to_list(query.limit)
    print(users)
    return users

async def getUserByEmail(db:AgnosticDatabase, email: EmailStr)->Union[User, None]:
    user = await db.user.find_one({"email":email})
    if user:
        print(type(user))

        return User.model_validate(user)
    else:
        return None
    
async def getToken(db:AgnosticDatabase, email: EmailStr , password :str)->LoginResponse:
    user = await getUserByEmail(db=db, email=email)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    else:
        if not verify_password(password, user.password):
             raise HTTPException(status_code=401, detail="Could not validate credentials")
    
        payloadData = {
            "email":user.email,
            "id":str(user.id)
        }
        token = create_access_token(data=payloadData )
        print(token)
        return LoginResponse(access_token=token, token_type="bearer")


async def getCurrentUser(db : AgnosticDatabase = Depends(getDB), token: str = Depends(oauth2_scheme))-> User:
    print(token)
    config = get_configs()
    print(config)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        
        payload = jwt.decode(token, config.jwt_secrete_key, algorithms=[config.jwt_algorithm])
        
        id: str = payload.get("id")
        email :str = payload.get("email")
        print(payload)
        if email is None:
            raise credentials_exception
        token_data = TokenData(id=id, email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = await getUserByEmail(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def create_user( db : AgnosticDatabase ,user:UserForm ,):
    print(user)
    password = get_password_hash(password=user.password)
    try:
        await db.user.insert_one({"email":user.email, "password":password,"name":user.name })
        return True
    except Exception as e:
        print(e)
        raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error",
            
        )
    
