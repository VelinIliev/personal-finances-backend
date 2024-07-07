from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id:  int
    email: str
    username: str
    first_name: str
    last_name: str
    role: int
    created_on: datetime
    updated_on: datetime
