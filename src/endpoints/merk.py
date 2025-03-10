from fastapi import APIRouter,Query, Depends
from typing import List, Union
from src.models.user import User
from src.models.product import Merk
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.merk as service
import src.services.user as userService
from bson import ObjectId

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

@router.get("/{id}", response_model=Merk)
async def getMerkDetail(
    id: str,
    db: AsyncIOMotorDatabase = Depends(getDB)
):
    object_id = ObjectId(id)
    
    merk = await db.merk.find_one({"_id": object_id})
    
    if not merk:
        raise HTTPException(status_code=404, detail="Merk not found")
    
    merk["_id"] = str(merk["_id"])
    
    return merk

@router.post("/")
async def createMerk(
    merk : Merk,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    current_user: User = Depends(userService.getCurrentUser),
    
    return await service.addOneMerks(db=db,data=merk)



@router.delete("/{id}")
async def deleteMerk(
    id : str,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    current_user: User = Depends(userService.getCurrentUser),
    
    return await service.deleteOneMerks(db=db,id=id)

@router.put("/{id}", response_model=Merk)
async def updateMerk(
    id: str,
    merk: Merk,
    db: AsyncIOMotorDatabase = Depends(getDB),
    current_user: User = Depends(userService.getCurrentUser)
):
    # Convert the string id to ObjectId
    object_id = ObjectId(id)
    
    # Call the service to update the merk
    updated_merk = await service.updateOneMerk(db=db, id=object_id, data=merk)
    
    if updated_merk is None:
        raise HTTPException(status_code=404, detail="Merk not found")
    
    return updated_merk