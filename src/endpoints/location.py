from bson import ObjectId
from fastapi import APIRouter, HTTPException,Query, Depends
from typing import List, Union
from src.models.location import Location
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

@router.get("/{id}", response_model=Location)
async def getLocationDetail(
    id: str,
    db: AsyncIOMotorDatabase = Depends(getDB)
):
    object_id = ObjectId(id)
    
    location = await db.location.find_one({"_id": object_id})
    
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    location["_id"] = str(location["_id"])
    
    return location

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