from datetime import datetime
import uuid
from pydantic import BaseModel, Field

class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        json_encoders = {
            uuid.UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }