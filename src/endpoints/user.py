from fastapi import APIRouter, Body, Request, status, Query, Depends
from typing import List, Union
from src.models.user import User, LoginData, UserForm
from src.models.query_paramater import QueryParameter

from motor.core import AgnosticDatabase
from src.database.mongo import getDB
from src.models.response_model import LoginResponse
from typing_extensions import Annotated
import src.services.user as userService

router = APIRouter(prefix="/users", tags=["User"])

@router.get("", response_description="List Users", response_model=List[User])
async def getUsers(
    db: AgnosticDatabase = Depends(getDB),
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None)
    
):
    query = QueryParameter(search=search, limit=limit, page=page )
    return await userService.getAllUser(db=db, query= query)


@router.post("/token", response_description="Get Token", response_model=LoginResponse)
async def getToken(
    login_data : LoginData,
    db: AgnosticDatabase = Depends(getDB)
):
    print(login_data)
    
    return await  userService.getToken(db=db, email=login_data.email, password=login_data.password)

@router.get("/me", response_description="Get User", response_model=User)
async def getUser(user: Annotated[User, Depends(userService.getCurrentUser)]):
    return user

@router.post("", response_description="Create User")
async def createUser(user: UserForm, db : Annotated[ AgnosticDatabase, Depends(getDB)]):
    if await userService.create_user(user= user, db=db):
        return {"message":"Success"} 