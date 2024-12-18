"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

from sqlalchemy import create_engine
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from .base_models import UserModel

local_engine = create_engine("sqlite:///Udatabase.db")

local_session = sessionmaker(bind=local_engine)

async def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

def get_all_users(db_session: Session):
    return db_session.scalars(select(UserModel).where()).all()

def get_user(db_session: Session, user_id: int):
    return db_session.scalar(select(UserModel).where(UserModel.id == user_id))