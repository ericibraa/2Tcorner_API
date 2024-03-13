from fastapi import APIRouter,Query, Depends
from typing import List, Union
from src.models.product import Merk
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.merk as service

router = APIRouter(prefix="/merk", tags=["Merks"])

merks = []
@router.get("/", response_description="List Merks", response_model= PaginationResponse)
async def getMerks(
    db: AsyncIOMotorDatabase = Depends(getDB),
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None)
):
    query = QueryParameter(search=search, limit=limit, page=page )
    
    return await service.getAllMerks(db=db, query= query)

@router.post("/")
async def createMerk(
    merk : Merk,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.addOneMerks(db=db,data=merk)



@router.post("/delete/{id}")
async def deleteMerk(
    id : str,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.deleteOneMerks(db=db,id=id)