from fastapi import Body, Request, HTTPException, status
from pydantic import TypeAdapter
from typing  import List
from fastapi.encoders import jsonable_encoder
from src.models.article import Article
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.models.response_model import Pagination, PaginationResponse
from bson import ObjectId


async def getAllArticles(db : AsyncIOMotorDatabase, query : QueryParameter ) -> PaginationResponse:
    match = {}
    skip = 0
    if query.search :
        match["title"] = query.search
    
    if query.page:
        skip = (query.page -1) * query.limit
        
    articles = await db.article.find(match).limit(query.limit).skip(skip).to_list(query.limit)
    total_records = await db.article.count_documents(match)
    res = TypeAdapter(List[Article]).validate_python(articles)
    
    
    return PaginationResponse(message="Articles", status=200, data = res, pagination=Pagination(total_records=total_records, current_page=query.page))

async def createArticle(db : AsyncIOMotorDatabase, data : Article )-> Article:
    try:
        data = jsonable_encoder(data)
        if data.get('_id'):
            data['_id'] = ObjectId()
        res = await db.article.insert_one(data)
        print(res)
        return {"message":"success"}
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while creating the article: {str(e)}")

async def updateArticle(db: AsyncIOMotorDatabase, id: ObjectId, data: Article):
    try:
        existing_article = await db.article.find_one({"_id": id})
        
        if not existing_article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        data_dict = data.dict(exclude_unset=True) 

        result = await db.article.update_one({"_id": id}, {"$set": data_dict})

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made to the Article.")
        
        update_article = await db.article.find_one({"_id": id})
        
        update_article["_id"] = str(update_article["_id"])
        
        return update_article
    except Exception as e:
        print(f"Error updating product: {str(e)}") 
        raise Exception(f"An error occurred while updating the article: {str(e)}")

async def deleteArticle(db : AsyncIOMotorDatabase, id : ObjectId ):
    try:
        res = await db.article.delete_one({"_id": ObjectId(id)})
        print(str(res.raw_result))
        return str(res.raw_result)
    except Exception as e:
        print(e)
