
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users_table"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    slugname = Column(String, unique=True, index=True)
    email = Column(String)
    language = Column(String)
    is_human = Column(Boolean)
    telegram_id = Column(Integer, unique=True, index=True)
    tasks_link = relationship(argument="EventModel", back_populates="owner_link")

class EventModel(Base):
    __tablename__ = "events_table"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
    date = Column(Date)
    time = Column(Time)
    owner_link = relationship(argument="UserModel", back_populates="tasks_link")
    owner_id = Column(Integer, ForeignKey("users_table.id")) 
    dealer = Column(String)
    
