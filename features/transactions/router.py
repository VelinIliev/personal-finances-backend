from typing import Annotated

import fastapi
from fastapi import Depends, Path
from starlette import status

import features.transactions.operations
from features.transactions.input_models import TransactionInputModel, CategoryInputModel
from features.transactions.responses import TransactionResponse, CategoryResponse
from features.users.operations import get_current_user

router = fastapi.APIRouter()

transactions_router = fastapi.APIRouter()
categories_router = fastapi.APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


@transactions_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_transactions(user: user_dependency):
    transactions = features.transactions.operations.get_all_transactions(user)
    return transactions


@transactions_router.get("/{transaction_id}",
                         status_code=status.HTTP_200_OK,
                         response_model=TransactionResponse)
async def get_transaction_by_id(
        user: user_dependency,
        transaction_id:
        int = Path(gt=0)):
    transaction = features.transactions.operations.get_transaction_by_id(user, transaction_id)
    return transaction


@transactions_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(
        user: user_dependency,
        transaction_request: TransactionInputModel):
    transaction = features.transactions.operations.create_transaction(user, transaction_request)
    return transaction


@transactions_router.put("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_transaction(user: user_dependency,
                             transaction_request: TransactionInputModel,
                             transaction_id: int = Path(gt=0)):
    features.transactions.operations.update_transaction(user, transaction_request, transaction_id)


@transactions_router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(user: user_dependency, transaction_id: int = Path(gt=0)):
    features.transactions.operations.delete_transaction(user, transaction_id)


@categories_router.get("/", status_code=status.HTTP_200_OK, response_model=list[CategoryResponse])
async def get_all_categories():
    return features.transactions.operations.get_all_categories()


@categories_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(user: user_dependency,
                          category_request: CategoryInputModel):
    features.transactions.operations.create_category(category_request)
    return


@categories_router.put("/{category_id}", status_code=status.HTTP_201_CREATED)
async def edit_category(user: user_dependency,
                        category_request: CategoryInputModel, category_id: int):
    features.transactions.operations.edit_category(category_request, category_id)
    return
