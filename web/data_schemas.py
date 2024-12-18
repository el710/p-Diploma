
from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
