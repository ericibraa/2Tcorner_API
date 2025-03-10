from fastapi import APIRouter, HTTPException,Query, Depends
from typing import List, Union
from src.models.user import User
from src.models.product import Product, ProductForm
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.product as service
import src.services.user as userService
from bson import ObjectId
from slugify import slugify

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_description="List Products", response_model= PaginationResponse)
async def getProducts(
    db: AsyncIOMotorDatabase = Depends(getDB), # type: ignore
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None),
    machine : Union[str, None] = Query(default=None),
    cc : Union[str, None] = Query(default=None),
    years : Union[str, None] = Query(default=None),
    grade : Union[str, None] = Query(default=None),
    type: Union[str, None] = Query(default=None),
):
    
    query = QueryParameter(search=search, limit=limit, page=page, machine=machine, cc=cc, years=years, grade=grade, type=type)
    
    products = await service.getAllProducts(db=db, query=query)

    # Debugging: Log the returned products
    print(f"Products Data: {products}")

    return products

@router.get("/{slug}", response_model=Product)
async def getProductDetail(
    slug: str,
    db: AsyncIOMotorDatabase = Depends(getDB) # type: ignore
):
    
    product = await service.getDetailProduct(db=db, slug=slug)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product["_id"] = str(product["_id"])
    
    return product

@router.post("/")
async def createProduct(
    product : ProductForm,
    db: AsyncIOMotorDatabase = Depends(getDB)):  # type: ignore
    current_user: User = Depends(userService.getCurrentUser),

    product_data = product.dict()
    
    product_data["slug"] = slugify(product.name) if not product.slug else product.slug
    
    return await service.addOneProduct(db=db,data=product_data)

@router.put("/{id}", response_model=Product)
async def updateProduct(
    id: str,
    product: ProductForm,
    db: AsyncIOMotorDatabase = Depends(getDB),  # type: ignore
    current_user: User = Depends(userService.getCurrentUser),
):
    object_id = ObjectId(id)

    update_product = await service.updateOneProduct(db=db, id=object_id, data=product)
    
    if update_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return update_product

@router.delete("/{id}")
async def deleteProduct(
    id : str,
    db: AsyncIOMotorDatabase = Depends(getDB)):  # type: ignore
    current_user: User = Depends(userService.getCurrentUser),
    
    return await service.deleteOneProduct(db=db,id=id)