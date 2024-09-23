from fastapi import APIRouter
from .view import router as launch_router

router = APIRouter()

router.include_router(launch_router, tags=['launch'])