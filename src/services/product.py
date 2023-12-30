from fastapi import Body, Request, HTTPException, status
from pydantic import TypeAdapter
from typing  import List
from fastapi.encoders import jsonable_encoder
from src.models.product import Product
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.models.response_model import Pagination, PaginationResponse


async def getAllProucts(db : AsyncIOMotorDatabase, query : QueryParameter ) -> PaginationResponse:
    pipeline= []
    match = {}
    skip = 0
    if query.search :
        match["email"] = query.search
        
    pipeline.append({
        "$match":match
    })

    if query.page:
        skip = (query.page -1) * query.limit
        pipeline.append({"$skip": skip})
    pipeline.append({"$limit":query.limit})

    lookup_brand = {
        "$lookup":{
            "from": "wa_brand",
            "localField": "brand",
            "foreignField": "_id",
            "as":"brand_detail" 
        }
    }
    pipeline.append(lookup_brand)

    unwind_brand = {
        "$unwind":{
            "path":"$brand_detail",
            "preserveNullAndEmptyArrays":True
        }
    }
    pipeline.append(unwind_brand)
    print(pipeline)
    products = await db.wa_product.aggregate(pipeline=pipeline).to_list(length=None)
    total_records = await db.wa_product.count_documents(match)

    list_product = TypeAdapter(List[Product]).validate_python(products)
 
    
    return PaginationResponse(message="Products", status=200, data = list_product, pagination=Pagination(total_records=total_records, current_page=query.page))




