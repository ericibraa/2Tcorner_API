from fastapi import Body, Request, HTTPException, status
from pydantic import TypeAdapter
from typing  import List
from fastapi.encoders import jsonable_encoder
from src.models.product import Merk
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.models.response_model import Pagination, PaginationResponse
from bson import ObjectId


async def getAllMerks(db : AsyncIOMotorDatabase, query : QueryParameter ) -> PaginationResponse:
    match = {}
    skip = 0
    if query.search :
        match["name"] = query.search
    
    if query.page:
        skip = (query.page -1) * query.limit
        
    list_merk = await db.merk.find(match).limit(query.limit).skip(skip).to_list(query.limit)
    total_records = await db.merk.count_documents(match)
    res = TypeAdapter(List[Merk]).validate_python(list_merk)
    
    
    return PaginationResponse(message="Merk", status=200, data = res, pagination=Pagination(total_records=total_records, current_page=query.page))

async def addOneMerks(db : AsyncIOMotorDatabase, data : Merk )-> Merk:
    try:
        data = jsonable_encoder(data)
        if data.get('_id'):
            data['_id'] = ObjectId()
            # data.pop('_id')
        res = await db.merk.insert_one(data)
        print(res)
        return ("document %s has been created" % str(res.inserted_id))
    except Exception as e:
        print(e)


async def deleteOneMerks(db : AsyncIOMotorDatabase, id : ObjectId ):
    try:
        res = await db.merk.delete_one({"_id": ObjectId(id)})
        print(str(res.raw_result))
        return str(res.raw_result)
    except Exception as e:
        print(e)


async def updateOneMerk(db: AsyncIOMotorDatabase, id: ObjectId, data: Merk):
    try:
        existing_merk = await db.merk.find_one({"_id": id})
        
        if not existing_merk:
            raise HTTPException(status_code=404, detail="Merk not found")
        
        data_dict = data.dict(exclude_unset=True) 

        result = await db.merk.update_one({"_id": id}, {"$set": data_dict})

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made to the merk.")
        
        updated_merk = await db.merk.find_one({"_id": id})
        
        updated_merk["_id"] = str(updated_merk["_id"])
        
        return updated_merk
    except Exception as e:
        print(f"Error updating merk: {str(e)}") 
        raise Exception(f"An error occurred while updating the merk: {str(e)}")
