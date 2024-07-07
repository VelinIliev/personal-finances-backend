from datetime import datetime

from pydantic import field_validator
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from email_validator import validate_email
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, nullable=False)
