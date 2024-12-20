"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

from sqlalchemy import create_engine
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from slugify import slugify

from web.data_schemas import CreateUser
from .base_models import UserModel, EventModel


local_engine = create_engine("sqlite:///Udatabase.db")

local_session = sessionmaker(bind=local_engine)

async def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

"""
    Users table
"""

def get_all_users(db_session: Session):
    return db_session.scalars(select(UserModel).where()).all()

def read_base_user(db_session: Session, user_id: int, slug: str | None):
    if slug is None:
        return db_session.scalar(select(UserModel).where(UserModel.id == user_id))
    else:
        return db_session.scalar(select(UserModel).where(UserModel.slugname == slug))

def make_slug(username: str, firstname: str, lastname: str):
    return slugify(f"{username}_{firstname}_{lastname}")

def create_base_user(db_session: Session, user: CreateUser):
    db_session.execute(insert(UserModel).values(username = user.username,
                                                firstname = user.firstname,
                                                lastname = user.lastname,
                                                slugname = make_slug(user.username, user.firstname, user.lastname),
                                                email = user.email,
                                                language = user.language,
                                                is_human = user.is_human,
                                                telegram_id = user.telegram_id
                                                )
                        )
    db_session.commit()


"""
    Events table
"""

def get_all_events(db_session: Session):
    return db_session.scalars(select(EventModel).where()).all()