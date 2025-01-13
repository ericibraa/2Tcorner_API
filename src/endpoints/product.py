from fastapi import APIRouter, HTTPException,Query, Depends
from typing import List, Union
from src.models.product import Product, ProductForm
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.product as service
from bson import ObjectId

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_description="List Products", response_model= PaginationResponse)
async def getProducts(
    db: AsyncIOMotorDatabase = Depends(getDB),
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None)
):
    query = QueryParameter(search=search, limit=limit, page=page )
    
    products = await service.getAllProducts(db=db, query=query)

    # Debugging: Log the returned products
    print(f"Products Data: {products}")

    return products

@router.get("/{id}", response_model=Product)
async def getProductDetail(
    id: str,
    db: AsyncIOMotorDatabase = Depends(getDB)
):
    object_id = ObjectId(id)
    
    product = await service.getDetailProduct(db=db, id=object_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product["_id"] = str(product["_id"])
    
    return product

@router.post("/")
async def createProduct(
    product : ProductForm,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.addOneProduct(db=db,data=product)

@router.put("/{id}", response_model=Product)
async def updateProduct(
    id: str,
    product: Product,
    db: AsyncIOMotorDatabase = Depends(getDB)
):
    object_id = ObjectId(id)
    
    update_product = await service.updateOneProduct(db=db, id=object_id, data=product)
    
    if update_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return update_product

@router.delete("/{id}")
async def deleteProduct(
    id : str,
    db: AsyncIOMotorDatabase = Depends(getDB)):
    
    return await service.deleteOneProduct(db=db,id=id)