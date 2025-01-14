"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

from sqlalchemy import create_engine
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from slugify import slugify

from web.data_schemas import *
from .base_models import UserModel, EventModel

import logging

local_engine = create_engine("sqlite:///Udatabase.db")

"""
    other functionality

    ## Create database file
    Base.metadata.create_all(bind=local_engine)

    ## create
    obj = UserModel(...)
    db_session.add(obj)
        or
    query = text("Insert Into <base> (name, slug) Values(:name, :slug)")
    db_session.execute(query, {"name": item_name, "slug": item_slug})
    db_session.commit()


    ## find 
    user = db_session.query(UserModel).filter(UserModel.id == user_id).first()  ##  all()

    

    ## delete
    db_session.delete(user)

    ## get
    query = text("Select * From <base>") // SQL code
    query = text("Select * From <base> Where name=:name") // SQL code
    ## get list of UserModel objects
    result = db_session.execute(query).fetchall()  ## get all data or fetchone() - get first
    result = db_session.execute(query, {"name": usr_name}).fetchone()



"""

local_session = sessionmaker(bind=local_engine, autoflush=False)

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
    '''
        Get list of all users from datatbase as sequence of UserModel()
    '''
    return db_session.scalars(select(UserModel).where()).all()

# def read_base_user(db_session: Session, telegram_id: int = None):
#     try:
#         user = db_session.scalar(select(UserModel).where(UserModel.telegram_id == telegram_id))
#         return user
#     except Exception:
#         return None
    
def read_base_user(telegram_id: int = None):
    '''
        Find user in database by telegram id
        Return: UserModel() | None
    '''
    db_session = local_session()
    try:
        user = db_session.scalar(select(UserModel).where(UserModel.telegram_id == telegram_id))
        return user
    except Exception:
        return None
    finally:
        db_session.close()
 

def make_slug(username: str, firstname: str, lastname: str):
    return slugify(f"{username}_{firstname}_{lastname}")

def create_base_user(user: CreateUser):
    db_session = local_session()
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
    db_session.close()
    


"""
    Events table
"""
def create_base_event(event: CreateEvent):
    db_session = local_session()
    db_session.execute(insert(EventModel).values(task = event.task,
                                                 date = event.date,
                                                 time = event.time,
                                                 owner_id = event.owner_id,
                                                 dealer = event.dealer
                                                )
                        )
    db_session.commit()
    db_session.close()


def get_all_events(db_session: Session):
    return db_session.scalars(select(EventModel).where()).all()


def read_users_events(user_id: int):
    user = read_base_user(user_id)

    db_session = local_session()
    events = db_session.scalars(select(EventModel).where(EventModel.owner_id == user.id)).all()
    db_session.close()

    return events


def update_base_event(event_id: int, event: CreateEvent):
    db_session = local_session()
    item = db_session.scalar(select(EventModel).where(EventModel.id == event_id))
    if item is None:
        db_session.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {event_id} not found")
    else:
        db_session.execute(update(EventModel).where(EventModel.id == event_id).values(task = event.task,
                                                                                      date = event.date,
                                                                                      time = event.time,
                                                                                      owner_id = event.owner_id,
                                                                                      dealer = event.dealer)
                                                                                    )
        db_session.commit()
        db_session.close()

def delete_base_event(event_id: int):
    '''
        Delete event with id = event_id from datatbase
    '''
    db_session = local_session()
    db_session.execute(delete(EventModel).where(EventModel.id == event_id))
    db_session.commit()
    db_session.close()
