from fastapi import HTTPException

import database
from features.transactions.models import Transaction, Category


def get_all_transactions(user):
    with database.get_session() as session:
        if user.get('role') == 1:
            return session.query(Transaction).all()

        return session.query(Transaction).filter(Transaction.user == user.get('id')).all()


def get_transaction_by_id(user, transaction_id):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    transaction = get_transaction(user, transaction_id)

    if transaction is None:
        raise HTTPException(status_code=404, detail="Not found.")

    return transaction


def create_transaction(user, transaction_request):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    with database.get_session() as session:
        transaction_model = Transaction(
            title=transaction_request.title,
            description=transaction_request.description,
            amount=transaction_request.amount,
            user=user.get('id'),
            categories=[]
        )
        for category_id in transaction_request.categories:
            category = session.query(Category).filter(Category.id == category_id).first()
            if category:
                transaction_model.categories.append(category)
        session.add(transaction_model)
        session.commit()

        return session.query(Transaction).filter(Transaction.id == transaction_model.id).first()


def update_transaction(user, transaction_request, transaction_id):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    with database.get_session() as session:

        transaction_model = get_transaction(user, transaction_id)

        if transaction_model is None:
            raise HTTPException(status_code=404, detail="Not Found.")

        transaction_model.title = transaction_request.title
        transaction_model.description = transaction_request.description
        transaction_model.type = transaction_request.type
        transaction_model.amount = transaction_request.amount

        session.add(transaction_model)
        session.commit()


def delete_transaction(user, transaction_id):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    with database.get_session() as session:
        transaction_model = get_transaction(user, transaction_id)

        if transaction_model is None:
            raise HTTPException(status_code=404, detail="Not Found.")

        session.delete(transaction_model)
        session.commit()


def get_transaction(user, transaction_id):
    with database.get_session() as session:
        if user.get('role') == 1:
            transaction = session.query(Transaction) \
                .filter(Transaction.id == transaction_id) \
                .first()
        else:
            transaction = session.query(Transaction) \
                .filter(Transaction.user == user.get('id')) \
                .filter(Transaction.id == transaction_id) \
                .first()
        return transaction


def get_all_categories():
    with database.get_session() as session:
        categories = session.query(Category).all()
        return categories


def create_category(category_request):
    with database.get_session() as session:
        category_model = Category(**category_request.model_dump())

        session.add(category_model)
        session.commit()

        return


def edit_category(category_request, category_id):
    with database.get_session() as session:
        category_model = session.query(Category).filter(Category.id == category_id).first()

        if category_model is None:
            raise HTTPException(status_code=404, detail="Not Found.")

        category_model.name = category_request.name

        session.add(category_model)
        session.commit()
