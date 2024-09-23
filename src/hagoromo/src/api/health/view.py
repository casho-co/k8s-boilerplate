from fastapi import APIRouter

router = APIRouter()


@router.get('/',)
def ping():
    return {"message": "Application is live"}

