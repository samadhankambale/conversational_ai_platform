from pydantic import BaseModel

class RegisterRequest(BaseModel):
    user_id: str
    password: str

class LoginRequest(BaseModel):
    user_id: str
    password: str



