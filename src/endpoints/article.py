from fastapi import APIRouter, HTTPException,Query, Depends
from typing import List, Union

from slugify import slugify
from src.models.article import Article, ArticleForm
from src.models.query_paramater import QueryParameter
from motor.motor_asyncio import  AsyncIOMotorDatabase
from src.database.mongo import getDB
from src.models.response_model import PaginationResponse
import src.services.article as service
from bson import ObjectId
from src.models.user import User
import src.services.user as userService

router = APIRouter(prefix="/articles", tags=["Article"])

articles = []
@router.get("/", response_description="List Article", response_model= PaginationResponse)
async def getArticles(
    db: AsyncIOMotorDatabase = Depends(getDB), # type: ignore
    limit :Union[int, None] = Query(default=None),
    page :Union[int, None]= Query(default=None),
    search : Union[str, None] = Query(default=None)
):
    query = QueryParameter(search=search, limit=limit, page=page )
    
    return await service.getAllArticles(db=db, query= query)

@router.get("/{slug}", response_model=Article)
async def getArticleDetail(
    slug: str,
    db: AsyncIOMotorDatabase = Depends(getDB) # type: ignore
):
    
    article = await db.article.find_one({"slug": slug})
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article["_id"] = str(article["_id"])
    
    return article

@router.post("/")
async def createArticle(
    article : ArticleForm,
    db: AsyncIOMotorDatabase = Depends(getDB)): # type: ignore
    current_user: User = Depends(userService.getCurrentUser),

    article_data = article.dict()
    
    article_data["slug"] = slugify(article.title) if not article.slug else article.slug
    
    return await service.createArticle(db=db,data=article_data)

@router.put("/{id}", response_model=ArticleForm)
async def updateArticle(
    id: str,
    article: ArticleForm,
    db: AsyncIOMotorDatabase = Depends(getDB), # type: ignore
    current_user: User = Depends(userService.getCurrentUser),
):
    object_id = ObjectId(id)

    updated_article = await service.updateArticle(db=db, id=object_id, data=article)
    
    if updated_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return updated_article

@router.delete("/{id}")
async def deleteArticle(
    id : str,
    db: AsyncIOMotorDatabase = Depends(getDB)): # type: ignore
    current_user: User = Depends(userService.getCurrentUser),
    
    return await service.deleteArticle(db=db,id=id)
