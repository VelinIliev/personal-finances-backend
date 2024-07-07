from typing import Optional

import pydantic
from fastapi import HTTPException
from pydantic import field_validator


class CategoryInputModel(pydantic.BaseModel):
    name: str = pydantic.Field(min_length=3, max_length=100)
    sub_category: str = pydantic.Field(min_length=3, max_length=100)
    type: str = pydantic.Field(min_length=3, max_length=10)

    @field_validator('type', mode='after')
    @classmethod
    def validate_type(cls, type):
        if type.lower() not in ['income', 'outcome']:
            raise HTTPException(status_code=400, detail="Invalid type.")
        return type


class CategoryIdInputModel(pydantic.BaseModel):
    id: int


class TransactionInputModel(pydantic.BaseModel):
    title: str = pydantic.Field(min_length=3, max_length=50)
    description: str = pydantic.Field(min_length=3, max_length=100)
    type: str = pydantic.Field(min_length=3, max_length=10)
    amount: float = pydantic.Field(ge=0)
    categories: list[int]

    @field_validator('type', mode='after')
    @classmethod
    def validate_type(cls, type):
        if type.lower() not in ['income', 'outcome']:
            raise HTTPException(status_code=400, detail="Invalid type.")
        return type

    @field_validator('amount', mode='before')
    @classmethod
    def validate_amount(cls, amount):
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0.")
        return amount
