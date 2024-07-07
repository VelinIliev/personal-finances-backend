from datetime import datetime
from typing import Any

from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    type: str
    sub_category: str


class TransactionResponse(BaseModel):
    id: int
    title: str
    description: str
    type: str
    amount: float
    created_on: datetime
    updated_on: datetime
    user: int
    categories: list[CategoryResponse] | Any = None
