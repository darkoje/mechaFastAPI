from sqlalchemy import Boolean, Column, Integer, String
from database import database

Base = database.base


class Mecha(Base):
    __tablename__ = "mechas"
    mecha_id = Column(Integer, primary_key=True, unique=True, index=True)
    owner = Column(String)
    staked = Column(Integer)

    class Config:
        orm_mode = True


class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    is_running = Column(Boolean, default=False)