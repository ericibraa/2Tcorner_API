from fastapi import APIRouter, HTTPException,Query, Depends
from typing import List, Union
from src.models.product import Type
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.type as service
from bson import ObjectId

router = APIRouter(prefix="/type", tags=["Type"])

@router.get("/", response_description="List Type", response_model= PaginationResponse)
async def getType(
    db: AsyncIOMotorDatabase = Depends(getDB),  # type: ignore
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None)
):
    query = QueryParameter(search=search, limit=limit, page=page )
    
    return await service.getAllType(db=db, query= query)

@router.get("/{id}", response_model=Type)
async def getTypeDetail(
    id: str,
    db: AsyncIOMotorDatabase = Depends(getDB)):  # type: ignore

    object_id = ObjectId(id)
    
    type = await db.type.find_one({"_id": object_id})
    
    if not type:
        raise HTTPException(status_code=404, detail="Type not found")
    
    type["_id"] = str(type["_id"])
    
    return type

@router.post("/")
async def createType(
    type : Type,
    db: AsyncIOMotorDatabase = Depends(getDB)):  # type: ignore
    
    return await service.addOneType(db=db,data=type)



@router.delete("/{id}")
async def deleteType(
    id : str,
    db: AsyncIOMotorDatabase = Depends(getDB)):  # type: ignore
    
    return await service.deleteOneType(db=db,id=id)

@router.put("/{id}")
async def UpdateType(
    id : str,
    type : Type,
    db: AsyncIOMotorDatabase = Depends(getDB)):  # type: ignore
    
    object_id = ObjectId(id)
    
    updated_merk = await service.updateOneType(db=db, id=object_id, data=type)
    
    if updated_merk is None:
        raise HTTPException(status_code=404, detail="Type not found")
    
    return updated_merk