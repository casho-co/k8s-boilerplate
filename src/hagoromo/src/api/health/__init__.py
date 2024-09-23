from fastapi import APIRouter
from .view import router as health_router

router = APIRouter()

router.include_router(health_router, tags=['health'])