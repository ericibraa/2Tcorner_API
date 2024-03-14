from fastapi import Body, Request, HTTPException, status
from pydantic import TypeAdapter
from typing  import List
from fastapi.encoders import jsonable_encoder
from src.models.product import Type
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.models.response_model import Pagination, PaginationResponse
from bson import ObjectId


async def getAllType(db : AsyncIOMotorDatabase, query : QueryParameter ) -> PaginationResponse:
    match = {}
    skip = 0
    if query.search :
        match["name"] = query.search
    
    if query.page:
        skip = (query.page -1) * query.limit
        
    list_type = await db.type.find(match).limit(query.limit).skip(skip).to_list(query.limit)
    total_records = await db.type.count_documents(match)
    res = TypeAdapter(List[Type]).validate_python(list_type)
    
    
    return PaginationResponse(message="Type", status=200, data = res, pagination=Pagination(total_records=total_records, current_page=query.page))

async def addOneType(db : AsyncIOMotorDatabase, data : Type )-> Type:
    data = jsonable_encoder(data)
    if data.get('_id'):
        data['_id'] = ObjectId()
        # data.pop('_id')
    res = await db.type.insert_one(data)
    print(res)
    return str(res.inserted_id)


async def deleteOneType(db : AsyncIOMotorDatabase, id : ObjectId ):
    res = await db.type.delete_one({"_id": ObjectId(id)})
    print(str(res.raw_result))
    return str(res.raw_result)