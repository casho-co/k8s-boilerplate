from fastapi import APIRouter
from .view import router as user_router
router = APIRouter()

router.include_router(user_router, tags=['user'])
