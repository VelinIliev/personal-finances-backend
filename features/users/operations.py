import os
from datetime import timedelta, datetime
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette import status

import database
from features.users.models import User

load_dotenv()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = os.getenv("SECRET_KEY_JWT")
ALGORITHM = os.getenv("ALGORITHM_JWT")

oath2_bearer = OAuth2PasswordBearer(tokenUrl='users/token')


def get_all_users(user):
    if user.get('role') == 1:
        with database.get_session() as session:
            users = session.query(User).order_by(User.id.asc()).all()
            return users
    raise HTTPException(status_code=403, detail='Unauthorized')


def get_user_by_id(user, user_id):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    if user.get('id') != user_id and user.get('role') != 1:
        raise HTTPException(status_code=403, detail="Unauthorized.")

    with database.get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return user


def create_user(create_user_request):
    with database.get_session() as session:
        create_user_model = User(
            email=create_user_request.email,
            username=create_user_request.username,
            first_name=create_user_request.first_name,
            last_name=create_user_request.last_name,
            role=create_user_request.role,
            # hashed_password=create_user_request.password,
            hashed_password=bcrypt_context.hash(create_user_request.password),
            is_active=True
        )
        session.add(create_user_model)
        session.commit()

        user = session.query(User).filter(User.username == create_user_model.username).first()

        return user


def authenticate_user(username: str, password: str):
    with database.get_session() as session:

        user = session.query(User).filter(User.username == username).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials.")

        if not bcrypt_context.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials.")
        token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials.")
        return token


def change_password(user, input_model):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    with database.get_session() as session:
        user_model = session.query(User).filter(User.id == user.get('id')).first()

        if not bcrypt_context.verify(input_model.old_password, user_model.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Error on password change.")
        user_model.hashed_password = bcrypt_context.hash(input_model.new_password)
        session.add(user_model)
        session.commit()


def create_access_token(username: str, user_id: int, role: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oath2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: int = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials.")
        return {'username': username, 'id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.")
