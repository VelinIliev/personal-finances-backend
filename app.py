from fastapi import FastAPI

import features

app = FastAPI(docs_url='/docs', redoc_url='/redoc')

app.include_router(features.transactions.router.transactions_router, prefix='/transactions', tags=['transactions'])
app.include_router(features.transactions.categories_router, prefix='/categories', tags=['categories'])
app.include_router(features.users.router.users_router, prefix='/users', tags=['users'])

