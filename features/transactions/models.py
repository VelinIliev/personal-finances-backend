from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import database
from database import Base


class TransactionCategory(Base):
    __tablename__ = 'transaction_category'
    id = Column(Integer, primary_key=True)
    transaction_id = Column('transaction_id', Integer, ForeignKey('transactions.id'))
    category_id = Column('category_id', Integer, ForeignKey('categories.id'))


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sub_category = Column(String(100), nullable=False)
    type = Column(String(10), nullable=False, default="outcome")
    transactions = relationship("Transaction", secondary='transaction_category', back_populates='categories',
                                lazy='selectin')


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    type = Column(String(10), nullable=False, default="outcome")
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = Column(Integer, ForeignKey("users.id"), nullable=False)
    categories = relationship("Category", secondary='transaction_category', back_populates='transactions',
                              lazy='selectin')


def fill_database():
    with database.get_session() as session:
        session.add_all([
            Category(id=1, name='Salary', sub_category='Income', type='income'),
            Category(id=2, name='Freelance', sub_category='Income', type='income'),
            Category(id=3, name='Business Income', sub_category='Income', type='income'),
            Category(id=4, name='Investment Returns', sub_category='Income', type='income'),
            Category(id=5, name='Rental Income', sub_category='Income', type='income'),
            Category(id=6, name='Dividends', sub_category='Income', type='income'),
            Category(id=7, name='Bonuses', sub_category='Income', type='income'),
            Category(id=8, name='Gifts', sub_category='Income', type='income'),
            Category(id=9, name='Refunds', sub_category='Income', type='income'),
            Category(id=10, name='Other', sub_category='Income', type='income'),
            Category(id=11, name='Rent', sub_category='Housing', type='outcome'),
            Category(id=12, name='Property Taxes', sub_category='Housing', type='outcome'),
            Category(id=13, name='Home Insurance', sub_category='Housing', type='outcome'),
            Category(id=14, name='Maintenance and Repairs', sub_category='Housing', type='outcome'),
            Category(id=15, name='Electricity', sub_category='Utilities', type='outcome'),
            Category(id=16, name='Water', sub_category='Utilities', type='outcome'),
            Category(id=17, name='Gas', sub_category='Utilities', type='outcome'),
            Category(id=18, name='Central Heating', sub_category='Utilities', type='outcome'),
            Category(id=19, name='Internet', sub_category='Utilities', type='outcome'),
            Category(id=20, name='Cable/Satellite TV', sub_category='Utilities', type='outcome'),
            Category(id=21, name='Phone', sub_category='Utilities', type='outcome'),
            Category(id=22, name='Groceries', sub_category='Food', type='outcome'),
            Category(id=23, name='Dining Out', sub_category='Food', type='outcome'),
            Category(id=24, name='Coffee Shops', sub_category='Food', type='outcome'),
            Category(id=25, name='Snacks', sub_category='Food', type='outcome'),
            Category(id=26, name='Public Transportation', sub_category='Transportation', type='outcome'),
            Category(id=27, name='Fuel', sub_category='Transportation', type='outcome'),
            Category(id=28, name='Car Payments', sub_category='Transportation', type='outcome'),
            Category(id=29, name='Car Insurance', sub_category='Transportation', type='outcome'),
            Category(id=30, name='Car Maintenance', sub_category='Transportation', type='outcome'),
            Category(id=31, name='Parking', sub_category='Transportation', type='outcome'),
            Category(id=32, name='Taxis/RideSharing', sub_category='Transportation', type='outcome'),
            Category(id=33, name='Health Insurance', sub_category='Healthcare', type='outcome'),
            Category(id=34, name='Doctor Visits', sub_category='Healthcare', type='outcome'),
            Category(id=35, name='Dental Care', sub_category='Healthcare', type='outcome'),
            Category(id=36, name='Vision Care', sub_category='Healthcare', type='outcome'),
            Category(id=37, name='Medications', sub_category='Healthcare', type='outcome'),
            Category(id=38, name='Wellness', sub_category='Healthcare', type='outcome'),
            Category(id=39, name='Haircuts and Salons', sub_category='Personal Care', type='outcome'),
            Category(id=40, name='Cosmetics', sub_category='Personal Care', type='outcome'),
            Category(id=41, name='Personal Hygiene', sub_category='Personal Care', type='outcome'),
            Category(id=42, name='Tuition', sub_category='Education', type='outcome'),
            Category(id=43, name='Tuition', sub_category='Books and Supplies', type='outcome'),
            Category(id=44, name='Student Loans', sub_category='Books and Supplies', type='outcome'),
            Category(id=45, name='Childcare', sub_category='Family and Children', type='outcome'),
            Category(id=46, name='School Fees', sub_category='Family and Children', type='outcome'),
            Category(id=47, name='Toys and Games', sub_category='Family and Children', type='outcome'),
            Category(id=48, name='Baby Supplies', sub_category='Family and Children', type='outcome'),
            Category(id=49, name='Movies and Concerts', sub_category='Entertainment and Recreation', type='outcome'),
            Category(id=50, name='Sports and Fitness', sub_category='Entertainment and Recreation', type='outcome'),
            Category(id=51, name='Hobbies', sub_category='Entertainment and Recreation', type='outcome'),
            Category(id=52, name='Streaming Services', sub_category='Entertainment and Recreation', type='outcome'),
            Category(id=53, name='Travel and Vacations', sub_category='Entertainment and Recreation', type='outcome'),
            Category(id=54, name='Clothes', sub_category='Clothing', type='outcome'),
            Category(id=55, name='Shoes', sub_category='Clothing', type='outcome'),
            Category(id=56, name='Accessories', sub_category='Clothing', type='outcome'),
            Category(id=57, name='Savings Account', sub_category='Savings and Investments', type='outcome'),
            Category(id=58, name='Retirement Contributions', sub_category='Savings and Investments', type='outcome'),
            Category(id=59, name='Stocks and Bonds', sub_category='Savings and Investments', type='outcome'),
            Category(id=60, name='Real Estate Investments', sub_category='Savings and Investments', type='outcome'),
            Category(id=61, name='Credit Card Payments', sub_category='Debt Payments', type='outcome'),
            Category(id=62, name='Loan Repayments', sub_category='Debt Payments', type='outcome'),
            Category(id=63, name='Charity', sub_category='Gifts and Donations', type='outcome'),
            Category(id=64, name='Gifts for Family and Friends', sub_category='Gifts and Donations', type='outcome'),
            Category(id=65, name='Subscriptions', sub_category='Miscellaneous', type='outcome'),
            Category(id=66, name='Memberships', sub_category='Miscellaneous', type='outcome'),
            Category(id=67, name='Pets', sub_category='Miscellaneous', type='outcome'),
            Category(id=68, name='Others', sub_category='Miscellaneous', type='outcome'),
        ])
        session.commit()


# fill_database()
