from fastapi import APIRouter,Query, Depends
from typing import List, Union
from src.models.product import Location
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.location as service

router = APIRouter(prefix="/location", tags=["Locations"])

@router.get("/", response_description="List Locations", response_model= PaginationResponse)
async def getLocations(
    db: AsyncIOMotorDatabase = Depends(getDB),
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None)
):
    query = QueryParameter(search=search, limit=limit, page=page )
    
    return await service.getAllLocation(db=db, query= query)

@router.post("/")
async def createLocations(
    location : Location,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.addOneLocation(db=db,data=location)



@router.delete("/{id}")
async def deleteLocations(
    id : str,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.deleteOneLocation(db=db,id=id)


@router.put("/{id}")
async def UpdateLocation(
    id : str,
    location : Location,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.updateOneLocation(db=db,id=id,data=location)