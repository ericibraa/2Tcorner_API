from fastapi import Body, Depends, Request, HTTPException, status
from typing  import List, Union
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from config.config import get_configs
from src.database.mongo import getDB
from src.models.user import User, TokenData
from src.models.response_model import LoginResponse
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.helper.user_security import verify_password, create_access_token
from bson import ObjectId
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def getAllUser(db:AsyncIOMotorDatabase, query : QueryParameter ) -> List[User]:
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

async def getUserByEmail(db:AsyncIOMotorDatabase, email: EmailStr)->Union[User, None]:
    user = await db.wa_user_admin.find_one({"email":email})
    if user:
        print(type(user))

        return User.model_validate(user)
    else:
        return None
    
async def getToken(db:AsyncIOMotorDatabase, email: EmailStr , password :str)->LoginResponse:
    user = await getUserByEmail(db=db, email=email)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    else:
        if not verify_password(password, user.password):
             raise HTTPException(status_code=401, detail="Could not validate credentials")
        else: 
            payloadData = {
                "email":user.email,
                "id":str(user.id)
            }
            token = create_access_token(data=payloadData )
            print(token)
            return LoginResponse(access_token=token, token_type="bearer")


async def getCurrentUser(db :AsyncIOMotorDatabase = Depends(getDB), token: str = Depends(oauth2_scheme))-> User:
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
    except JWTError:
        raise credentials_exception
    user = await getUserByEmail(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user