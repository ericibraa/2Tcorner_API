from fastapi import Body, Request, HTTPException, status
from pydantic import TypeAdapter
from typing  import List
from fastapi.encoders import jsonable_encoder
from src.models.product import Product
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
                "from": "merk",  # The collection to join
                "let": {"merk_id": "$merk"},  # Variable from the product document
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": [
                                    {"$toObjectId": "$$merk_id"}, "$_id"
                                ]
                            }
                        }
                    }
                ],
                "as": "merk_details"  # The result will be placed in this field
            }
        },
        {
            "$unwind": {
                "path": "$merk_details",
                "preserveNullAndEmptyArrays": True  # Keep products without merk details
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

async def addOneProduct(db : AsyncIOMotorDatabase, data : Product )-> Product:
    try:
        data = jsonable_encoder(data)
        if data.get('_id'):
            data['_id'] = ObjectId()
            # data.pop('_id')
        res = await db.product.insert_one(data)
        print(res)
        return ("document %s has been created" % str(res.inserted_id))
    except Exception as e:
        print(e)

async def updateOneProduct(db: AsyncIOMotorDatabase, id: ObjectId, data: Product):
    try:
        existing_product = await db.product.find_one({"_id": id})
        
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        data_dict = data.dict(exclude_unset=True) 

        result = await db.product.update_one({"_id": id}, {"$set": data_dict})

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made to the product.")
        
        updated_product = await db.product.find_one({"_id": id})
        
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


