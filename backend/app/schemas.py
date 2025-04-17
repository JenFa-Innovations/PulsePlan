from pydantic import BaseModel

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
