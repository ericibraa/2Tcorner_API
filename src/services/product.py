from fastapi import Body, Request, HTTPException, status
from pydantic import TypeAdapter
from typing  import List
from fastapi.encoders import jsonable_encoder
from src.models.product import Product, ProductForm
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.models.response_model import Pagination, PaginationResponse
from bson import ObjectId

def serialize_objectid(value):
    if isinstance(value, ObjectId):
        return str(value)
    elif isinstance(value, dict):
        return {k: serialize_objectid(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [serialize_objectid(v) for v in value]
    return value


async def getAllProducts(db: AsyncIOMotorDatabase, query: QueryParameter) -> PaginationResponse:
    match = {}
    skip = 0
    if query.search:
        match["name"] = {"$regex": query.search, "$options": "i"}

    # Default values for pagination
    page = query.page or 1
    limit = query.limit or 10
    skip = (page - 1) * limit

    pipeline = [
        {"$match": match},
        {
            "$lookup": {
                "from": "merk",
                'localField': 'merk',
                "foreignField": '_id',
                "as": "merk_details"
            }
        },
         {
            "$lookup": {
                "from": "type",
                'localField': 'type',
                "foreignField": '_id',
                "as": "type_details"
            }
        },
        {
            "$unwind": {
                "path": "$merk_details",
                "preserveNullAndEmptyArrays": True 
            }
        },
        {
            "$unwind": {
                "path": "$type_details",
                "preserveNullAndEmptyArrays": True 
            }
        },
        # Skip and limit for pagination
        {"$skip": skip},
        {"$limit": limit}
    ]

    # Perform the aggregation query
    products = await db.product.aggregate(pipeline).to_list(length=limit)

    # Serialize ObjectIds to strings
    products = [{k: serialize_objectid(v) for k, v in product.items()} for product in products]

    # Get total count (without the lookup or unwind, just match)
    total_records = await db.product.count_documents(match)

    # Validate products after serialization
    list_product = TypeAdapter(List[Product]).validate_python(products)

    # Return paginated response
    return PaginationResponse(
        message="Products",
        status=200,
        data=list_product,
        pagination=Pagination(
            total_records=total_records,
            current_page=page
        )
    )

async def getDetailProduct(db: AsyncIOMotorDatabase, id: ObjectId):
    pipeline = [
         {"$match": {"_id": id}},
        {
            "$lookup": {
                "from": "merk",
                'localField': 'merk',
                "foreignField": '_id',
                "as": "merk_details"
            }
        },
         {
            "$lookup": {
                "from": "type",
                'localField': 'type',
                "foreignField": '_id',
                "as": "type_details"
            }
        },
        {
            "$unwind": {
                "path": "$merk_details",
                "preserveNullAndEmptyArrays": True 
            }
        },
        {
            "$unwind": {
                "path": "$type_details",
                "preserveNullAndEmptyArrays": True 
            }
        },
    ]
    products = await db.product.aggregate(pipeline).to_list(length=1)

    if products:
            return serialize_objectid(products[0])
    return None


async def addOneProduct(db : AsyncIOMotorDatabase, data : ProductForm )-> dict:
    try:
        data = jsonable_encoder(data)
        data["_id"] = ObjectId()
        if (data.get("merk")):
            data["merk"] = ObjectId(data["merk"])

        if (data.get("type")):
            data["type"] = ObjectId(data["type"])

        res = await db.product.insert_one(data)
        print(res)
        return {"message":"success"}
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while creating the product: {str(e)}")


async def updateOneProduct(db: AsyncIOMotorDatabase, id: ObjectId, data: Product):
    try:
        existing_product = await db.product.find_one({"_id": id})
        
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        data_dict = data.dict(exclude_unset=True) 

        result = await db.product.update_one({"_id": id}, {"$set": data_dict})

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made to the product.")
        
        if (data.get("merk")):
            data["merk"] = ObjectId(data["merk"])

        if (data.get("type")):
            data["type"] = ObjectId(data["type"])
        
        updated_product = await db.product.find_one({"_id": id})

        updated_product["merk"] = ObjectId(updated_product["merk"])

        updated_product["type"] = ObjectId(updated_product["type"])
        
        updated_product["_id"] = str(updated_product["_id"])    
        
        return updated_product
    except Exception as e:
        print(f"Error updating product: {str(e)}") 
        raise Exception(f"An error occurred while updating the product: {str(e)}")

async def deleteOneProduct(db : AsyncIOMotorDatabase, id : ObjectId ):
    try:
        res = await db.product.delete_one({"_id": ObjectId(id)})
        print(str(res.raw_result))
        return str(res.raw_result)
    except Exception as e:
        print(e)


