from fastapi import Body, Request, HTTPException, status
from pydantic import TypeAdapter
from typing  import List
from fastapi.encoders import jsonable_encoder
from src.models.location import Location
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.models.response_model import Pagination, PaginationResponse
from bson import ObjectId


async def getAllLocation(db : AsyncIOMotorDatabase, query : QueryParameter ) -> PaginationResponse: # type: ignore
    match = {}
    skip = 0
    if query.search :
        match["kota"] = query.search
    
    if query.page:
        skip = (query.page -1) * query.limit
        
    list_location = await db.location.find(match).limit(query.limit).skip(skip).to_list(query.limit)
    total_records = await db.location.count_documents(match)
    res = TypeAdapter(List[Location]).validate_python(list_location)
    
    return PaginationResponse(message="Location", status=200, data = res, pagination=Pagination(total_records=total_records, current_page=query.page))

async def addOneLocation(db : AsyncIOMotorDatabase, data : Location )-> Location: # type: ignore
    data = jsonable_encoder(data)
    if data.get('_id'):
        data['_id'] = ObjectId()
        # data.pop('_id')
    res = await db.location.insert_one(data)
    print(res)
    return str(res.inserted_id)


async def deleteOneLocation(db : AsyncIOMotorDatabase, id : ObjectId ): # type: ignore
    res = await db.location.delete_one({"_id": ObjectId(id)})
    print(str(res.raw_result))
    return str(res.raw_result)


async def updateOneLocation(db : AsyncIOMotorDatabase, id : ObjectId ,data=Location): # type: ignore
    try:
        data = jsonable_encoder(data)
        if data.get('_id') == 'False':
            data.pop('_id')
        print(data)
        res = await db.location.replace_one({"_id": ObjectId(id)},data)
        print(res.modified_count)
        return ("replaced %s document" % res.modified_count)
    except Exception as e:
        print(e)