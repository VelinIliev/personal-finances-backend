from typing import Annotated

import fastapi
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import features.users.operations
from features.users.responses import UserResponse
from features.users.input_models import CreateUserInputModel, ChangePasswordInputModel
from features.users.responses import Token
from features.users.operations import get_current_user

router = fastapi.APIRouter()

users_router = fastapi.APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


@users_router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_all_users(user: user_dependency):
    return features.users.operations.get_all_users(user)


@users_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(user: user_dependency, user_id: int):
    return features.users.operations.get_user_by_id(user, user_id)


@users_router.post("/",
                   status_code=status.HTTP_201_CREATED,
                   response_model=UserResponse)
async def create_user(create_user_request: CreateUserInputModel):
    user = features.users.operations.create_user(create_user_request)
    return user


@users_router.post("/token",
                   status_code=status.HTTP_200_OK,
                   response_model=Token)
async def login_for_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token = features.users.operations.authenticate_user(form_data.username, form_data.password)
    return {'access_token': token, 'token_type': 'bearer'}


@users_router.put("/change-password",
                  status_code=status.HTTP_204_NO_CONTENT
                  )
async def change_password(user: user_dependency, input_model: ChangePasswordInputModel):
    features.users.operations.change_password(user, input_model)
    return
