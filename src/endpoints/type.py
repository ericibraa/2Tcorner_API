from fastapi import APIRouter,Query, Depends
from typing import List, Union
from src.models.product import Type
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.type as service

router = APIRouter(prefix="/type", tags=["Type"])

@router.get("/", response_description="List Type", response_model= PaginationResponse)
async def getType(
    db: AsyncIOMotorDatabase = Depends(getDB),
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None)
):
    query = QueryParameter(search=search, limit=limit, page=page )
    
    return await service.getAllType(db=db, query= query)

@router.post("/")
async def createType(
    type : Type,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.addOneType(db=db,data=type)



@router.delete("/{id}")
async def deleteType(
    id : str,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.deleteOneType(db=db,id=id)

@router.put("/{id}")
async def UpdateType(
    id : str,
    type : Type,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.updateOneType(db=db,id=id,data=type)