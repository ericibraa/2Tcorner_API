from fastapi import APIRouter
from src.endpoints import user, product, merk

router = APIRouter()
router.include_router(user.router)
router.include_router(product.router)
router.include_router(merk.router)