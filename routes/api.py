from fastapi import APIRouter
from src.endpoints import user, product

router = APIRouter()
router.include_router(user.router)
router.include_router(product.router)