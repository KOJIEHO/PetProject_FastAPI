from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
from models.models import Base, User, Post
from database.database import engine, session_local
from schemas.schemas import UserCreate, User as DbUser, PostCreate, PostResponse

test = 'test'

app = FastAPI()

# Настройка CORS
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine) 


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close


# Когда передаются данные через post запрос, то автоматически передаются данные о пользователе + подключаемся к БД
@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Когда передаются данные через post запрос, то автоматически передаются данные о статье + подключаемся к БД
@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


# Когда передаются данные через post запрос, то автоматически передаются данные о статье + подключаемся к БД
@app.get("/posts/", response_model=List[PostResponse])
async def get_post(db: Session = Depends(get_db)):
    db_posts = db.query(Post).all()
    if db_posts is None:
        raise HTTPException(status_code=404, detail='Posts not found')
    return db_posts


@app.get("/users/{name}", response_model=DbUser)
async def user(name: str, db: Session = Depends(get_db)) -> DbUser:
    db_user = db.query(User).filter(User.name == name).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found') 

    return db_user
