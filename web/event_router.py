from fastapi import APIRouter, HTTPException

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, status
from sqlalchemy import select, insert, update, delete
from slugify import slugify

from database.db import *

from database.base_models import EventModel
from .data_schemas import *


event_router = APIRouter(prefix="/event", tags=["Event"])

@event_router.get("/")
async def all_events(db: Annotated[Session, Depends(get_db)]):
    return get_all_events(db)
    
@event_router.get("/user_id")
async def events_of_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    return read_users_events(db, user_id)


@event_router.post("/create")
async def create_event(db: Annotated[Session, Depends(get_db)], event: CreateEvent):
    create_base_event(db, event)

    return {"status_code": status.HTTP_200_OK, "transaction": f"Event {event.task} created"}

