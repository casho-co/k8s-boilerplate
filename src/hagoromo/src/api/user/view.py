from datetime import datetime
import uuid
from fastapi import APIRouter, HTTPException, Request, status
from pymongo.errors import DuplicateKeyError
from ...models.user import User

router = APIRouter()



@router.post('/',response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User, request: Request):
    users_collection = request.app.db['users']
    try:
        user_data = user.model_dump()
        user_data["id"] = str(uuid.uuid4())
        user_data["created_at"] = datetime.now() 
        await users_collection.insert_one(user_data)
        return user
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User already exists")
