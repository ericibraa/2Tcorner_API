from typing import Union
from bson import ObjectId
from fastapi import APIRouter, HTTPException,Query, Depends
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.models.query_paramater import QueryParameter
from src.models.response_model import PaginationResponse
from src.database.mongo import getDB
import src.services.banner as service
from src.models.banner import CreateBannerRequest

router = APIRouter(prefix="/banner", tags=["Banner"])

banners = []
@router.get("/", response_description="List Banner", response_model=PaginationResponse)
async def getBanner(
    db: AsyncIOMotorDatabase = Depends(getDB), # type: ignore
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
):
    query = QueryParameter(limit=limit, page=page )
    return await service.getAllBanner(db=db, query=query)

@router.post("/", response_description="Create Banner")
async def create_banner(
    banner: CreateBannerRequest,
    db: AsyncIOMotorDatabase = Depends(getDB), # type: ignore
):
    result = await db.banner.insert_one(banner.dict())
    return {"message": "Banner created", "id": str(result.inserted_id)}

@router.delete("/{id}", response_description="Delete Banner")
async def delete_banner(id: str, db: AsyncIOMotorDatabase = Depends(getDB)): # type: ignore
    result = await db.banner.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Banner not found")
    return {"message": "Banner deleted successfully"}