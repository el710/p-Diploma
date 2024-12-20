
from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str
    language: str
    is_human: bool
    telegram_id: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str


"""
    Event
"""

class CreateEvent(BaseModel):
    task: str
    date: str
    time: str
    owner_id: int
    dealer: str