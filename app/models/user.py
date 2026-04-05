from pydantic import BaseModel

class UserProfile(BaseModel):
    user_id: str
    preferences: dict