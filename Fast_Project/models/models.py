from database.database import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__ = "users"

    # Создаем колонки со своими параметрами
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)


class Post(Base):
    __tablename__ = "posts"

    # Создаем колонки со своими параметрами
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User")
