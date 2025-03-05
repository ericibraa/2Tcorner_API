from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.endpoints import user, product, merk, type, location, category, article, upload
from motor.core import AgnosticDatabase
from src.models.user import LoginData
from src.models.response_model import LoginResponse

from src.database.mongo import getDB
import src.services.user as userService

router = APIRouter()
router.include_router(user.router)
router.include_router(product.router)
router.include_router(merk.router)
router.include_router(type.router)
router.include_router(location.router)
router.include_router(category.router)
router.include_router(article.router)
router.include_router(upload.router)


@router.post("/token", response_description="Get Token", response_model=LoginResponse)
async def getToken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AgnosticDatabase = Depends(getDB)
):
    print(form_data)
    
    return await  userService.getToken(db=db, email=form_data.username, password=form_data.password)
