from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    otp_code: str

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True  # Enables ORM-to-Pydantic conversion
    }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str

class TaskBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True