from fastapi import APIRouter,Query, Depends
from typing import List, Union
from src.models.product import Product
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.product as service

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_description="List Products", response_model= PaginationResponse)
async def getProducts(
    db: AsyncIOMotorDatabase = Depends(getDB),
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None)
):
    query = QueryParameter(search=search, limit=limit, page=page )
    
    return await service.getAllProucts(db=db, query= query)

