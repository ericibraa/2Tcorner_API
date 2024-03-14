from fastapi import APIRouter,Query, Depends
from typing import List, Union
from src.models.product import Category
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.category as service

router = APIRouter(prefix="/category", tags=["Categories"])

Categories = []
@router.get("/", response_description="List Categories", response_model= PaginationResponse)
async def getCategories(
    db: AsyncIOMotorDatabase = Depends(getDB),
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None)
):
    query = QueryParameter(search=search, limit=limit, page=page )
    
    return await service.getAllCategory(db=db, query= query)

@router.post("/")
async def createCategory(
    category : Category,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.addOneCategory(db=db,data=category)



@router.delete("/{id}")
async def deleteCategory(
    id : str,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.deleteOneCategory(db=db,id=id)



@router.put("/{id}")
async def UpdateCategory(
    id : str,
    category : Category,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.updateOneCategory(db=db,id=id,data=category)