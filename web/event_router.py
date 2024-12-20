from fastapi import APIRouter, HTTPException

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, status
from sqlalchemy import select, insert, update, delete
from slugify import slugify

from database.db import get_db
from database.db import get_all_events
from database.base_models import EventModel
from .data_schemas import *


event_router = APIRouter(prefix="/event", tags=["Event"])

@event_router.get("/")
async def all_events(db: Annotated[Session, Depends(get_db)]):
    return get_all_events(db)
    


