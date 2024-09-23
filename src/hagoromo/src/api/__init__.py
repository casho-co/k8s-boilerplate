from fastapi import APIRouter
from .launch import router as launch_router
from .health import router as health_router
from .user import router as user_router

api_router = APIRouter()

# Add all routes here
api_router.include_router(health_router, prefix='/health', tags=['health'])
api_router.include_router(user_router, prefix='/user', tags=['user'])
api_router.include_router(launch_router,prefix='/launch', tags=['launch'])