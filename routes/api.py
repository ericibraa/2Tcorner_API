from fastapi import APIRouter
from src.endpoints import user, product, merk, type, location, category

router = APIRouter()
router.include_router(user.router)
router.include_router(product.router)
router.include_router(merk.router)
router.include_router(type.router)
router.include_router(location.router)
router.include_router(category.router)