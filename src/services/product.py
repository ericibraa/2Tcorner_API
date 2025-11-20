from datetime import datetime 
from fastapi import Body, Request, HTTPException, status
from pydantic import TypeAdapter
from typing  import List
from fastapi.encoders import jsonable_encoder
from slugify import slugify
from src.models.product import Product, ProductForm, UpdateStatusModel
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.models.response_model import Pagination, PaginationResponse
from bson import ObjectId
from urllib.parse import urlparse

def serialize_objectid(value):
    if isinstance(value, ObjectId):
        return str(value)
    elif isinstance(value, dict):
        return {k: serialize_objectid(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [serialize_objectid(v) for v in value]
    return value


async def getAllProducts(db: AsyncIOMotorDatabase, query: QueryParameter) -> PaginationResponse: # type: ignore
    match = {}
    if query.status is not None:
        match["status"] = query.status
    if query.search:
        match["name"] = {"$regex": query.search, "$options": "i"}
    if query.machine:
        match["category"] = {"$regex": query.machine, "$options": "i"}
    if query.cc:
        match["cc"] = {"$regex": query.cc, "$options": "i"}    
    if query.years:
        match["year"] = {"$regex": query.years, "$options": "i"}
    if query.grade:
        match["grade"] = {"$regex": query.grade, "$options": "i"}
    if query.type:
        match["type"] = query.type
    if query.location:
        match["location"] = query.location

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
            "$lookup": {
                "from": "location",
                'localField': 'location',
                "foreignField": '_id',
                "as": "location_details"
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
        {
            "$unwind": {
                "path": "$location_details",
                "preserveNullAndEmptyArrays": True 
            }
        },
        {"$skip": skip},
        {"$limit": limit}
    ]

    products = await db.product.aggregate(pipeline).to_list(length=limit)

    products = [{k: serialize_objectid(v) for k, v in product.items()} for product in products]

    total_records = await db.product.count_documents(match)

    list_product = TypeAdapter(List[Product]).validate_python(products)

    return PaginationResponse(
        message="Products",
        status=200,
        data=list_product,
        pagination=Pagination(
            total_records=total_records,
            current_page=page
        )
    )

async def getDetailProduct(db: AsyncIOMotorDatabase, slug: str):  # type: ignore
    pipeline = [
    {"$match": {"slug": slug}},
    {
        "$lookup": {
            "from": "merk",
            "localField": "merk",
            "foreignField": "_id",
            "as": "merk_details"
        }
    },
    {
        "$lookup": {
            "from": "type",
            "localField": "type",
            "foreignField": "_id",
            "as": "type_details"
        }
    },
    {
        "$lookup": {
            "from": "location",
            "localField": "location",
            "foreignField": "_id",
            "as": "location_details"
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
    {
        "$unwind": {
            "path": "$location_details",
            "preserveNullAndEmptyArrays": True
        }
    }
]

    products = await db.product.aggregate(pipeline).to_list(length=1)

    if products:
            return serialize_objectid(products[0])
    return None

async def get_next_sequence(db: AsyncIOMotorDatabase, year: int, month: int) -> int: # type: ignore
    counter_id = f"sku_{year}_{month:02d}" 

    counter = await db.counters.find_one_and_update(
        {"_id": counter_id},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )

    return counter["seq"]

async def generate_sku(db: AsyncIOMotorDatabase) -> str: # type: ignore
    prefix = "2CN"
    now = datetime.now()
    year = now.year
    month = now.month 

    sequence = await get_next_sequence(db, year, month)

    sequence_str = f"{month:02d}{sequence}"

    sku_code = f"{prefix}-{year}-{sequence_str}"
    return sku_code

async def addOneProduct(db : AsyncIOMotorDatabase, data : ProductForm )-> dict:  # type: ignore
    try:
        data = jsonable_encoder(data)
        data["_id"] = ObjectId()
        if (data.get("merk")):
            data["merk"] = ObjectId(data["merk"])

        if (data.get("type")):
            data["type"] = ObjectId(data["type"])

        if (data.get("location")):
            data["location"] = ObjectId(data["location"])

        if not data.get("sku_code"):
            data["sku_code"] = await generate_sku(db)

        if not data.get("code"):
            data["code"] = data["sku_code"]

        data["status"] = 10

        if (data.get("instagram")):
            instagram_url = data["instagram"]
            parsed_url = urlparse(instagram_url)
            base_url = parsed_url._replace(query='').geturl() 
            embed_url = base_url + 'embed' 
            data["instagram"] = embed_url
        res = await db.product.insert_one(data)
        print(res)
        return {"message":"success"}
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while creating the product: {str(e)}")


async def updateOneProduct(db: AsyncIOMotorDatabase, id: ObjectId, data: ProductForm):  # type: ignore
    try:
        existing_product = await db.product.find_one({"_id": id})
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")

        data_dict = data.dict(exclude_unset=True)

        if "merk" in data_dict and data_dict["merk"]:
            data_dict["merk"] = ObjectId(data_dict["merk"])

        if "type" in data_dict and data_dict["type"]:
            data_dict["type"] = ObjectId(data_dict["type"])

        if "location" in data_dict and data_dict["location"]:
            data_dict["location"] = ObjectId(data_dict["location"])

        data_dict["status"] = 10  

        result = await db.product.update_one({"_id": id}, {"$set": data_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made to the product.")

        updated_product = await db.product.find_one({"_id": id})

        if updated_product:
            if "merk" in updated_product and updated_product["merk"]:
                updated_product["merk"] = str(updated_product["merk"])
            if "type" in updated_product and updated_product["type"]:
                updated_product["type"] = str(updated_product["type"])
            if "location" in updated_product and updated_product["location"]:
                updated_product["location"] = str(updated_product["location"])


        return updated_product

    except Exception as e:
        print(f"Error updating product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the product: {str(e)}")

async def deleteOneProduct(db : AsyncIOMotorDatabase, id : ObjectId ):  # type: ignore
    try:
        res = await db.product.delete_one({"_id": ObjectId(id)})
        print(str(res.raw_result))
        return str(res.raw_result)
    except Exception as e:
        print(e)

async def updateOneStatus(db : AsyncIOMotorDatabase, id : ObjectId, data : UpdateStatusModel): # type: ignore
    try:
        res = await db.product.update_one(
            {"_id": id},
            {"$set": {"status": data.status}}
        )

        if res.modified_count == 0:
            raise HTTPException(status_code=404, detail="Product not found or status unchanged")

        return {
            "message": "Product status updated successfully",
            "status": data.status
        }
    except Exception as e:
        print(e)
