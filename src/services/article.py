from datetime import datetime
from fastapi import Body, Request, HTTPException, status
from pydantic import TypeAdapter
from typing  import List
from fastapi.encoders import jsonable_encoder
from src.models.article import Article, ArticleForm
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.models.response_model import Pagination, PaginationResponse
from bson import ObjectId
from src.models.product import UpdateStatusModel


async def getAllArticles(db : AsyncIOMotorDatabase, query : QueryParameter ) -> PaginationResponse: # type: ignore
    match = {}
    skip = 0
    if query.search :
        match["title"] = query.search
    if query.page:
        skip = (query.page -1) * query.limit
    if query.status is not None:
        match["status"] = query.status
        
    articles = await db.article.find(match).limit(query.limit).skip(skip).to_list(query.limit)
    total_records = await db.article.count_documents(match)
    res = TypeAdapter(List[Article]).validate_python(articles)
    
    
    return PaginationResponse(message="Articles", status=200, data = res, pagination=Pagination(total_records=total_records, current_page=query.page))

async def createArticle(db : AsyncIOMotorDatabase, data : ArticleForm )-> ArticleForm: # type: ignore
    try:
        data_dict = jsonable_encoder(data)

        if data_dict.get('_id'):
            data_dict['_id'] = ObjectId()

        data_dict["created_at"] = datetime.utcnow()

        if data_dict.get("status") is None:
            data_dict["status"] = 10

        res = await db.article.insert_one(data_dict)
        print(res)
        return {"message":"success"}
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while creating the article: {str(e)}")

async def updateArticle(db: AsyncIOMotorDatabase, id: ObjectId, data: ArticleForm): # type: ignore
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

async def deleteArticle(db : AsyncIOMotorDatabase, id : ObjectId ): # type: ignore
    try:
        res = await db.article.delete_one({"_id": ObjectId(id)})
        print(str(res.raw_result))
        return str(res.raw_result)
    except Exception as e:
        print(e)

async def updateOneStatus(db : AsyncIOMotorDatabase, id : ObjectId, data : UpdateStatusModel): # type: ignore
    try:
        res = await db.article.update_one(
            {"_id": id},
            {"$set": {"status": data.status}}
        )

        if res.modified_count == 0:
            raise HTTPException(status_code=404, detail="Article not found or status unchanged")

        return {
            "message": "Article status updated successfully",
            "status": data.status
        }
    except Exception as e:
        print(e)
