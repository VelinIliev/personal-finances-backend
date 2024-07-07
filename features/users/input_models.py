import re
from typing import Optional

import pydantic
from email_validator import validate_email
from fastapi import HTTPException
from pydantic import field_validator

import database
from features.users.models import User
from features.users.helpers import validate_password


class CreateUserInputModel(pydantic.BaseModel):
    username: str = pydantic.Field(min_length=3, max_length=255)
    email: str
    first_name: Optional[str] = pydantic.Field(min_length=1, max_length=255)
    last_name: Optional[str] = pydantic.Field(min_length=1, max_length=255)
    password: str
    role: int

    @field_validator('username', mode='after')
    @classmethod
    def validate_user_username(cls, username):
        with database.get_session() as session:
            user = session.query(User).filter(User.username == username).first()
            if user:
                raise HTTPException(status_code=400, detail="User with this username exist.")
        return username

    @field_validator('email', mode='after')
    @classmethod
    def validate_user_email(cls, email):
        try:
            validate_email(email)
        except Exception as e:
            raise ValueError(f"Invalid email address: {e}")

        with database.get_session() as session:
            user = session.query(User).filter(User.email == email).first()
            if user:
                raise HTTPException(status_code=400, detail="User with this email exist.")

        return email

    @field_validator('password', mode='after')
    @classmethod
    def validate_user_password(cls, password):
        validate_password(password)
        return password


class ChangePasswordInputModel(pydantic.BaseModel):
    old_password: str
    new_password: str

    @field_validator('new_password', mode='after')
    @classmethod
    def validate_new_password(cls, password):
        validate_password(password)
        return password



