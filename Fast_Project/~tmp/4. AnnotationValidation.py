from fastapi import FastAPI, HTTPException, Path, Query
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel, Field
import sqlite3


app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


# Здесь для аннотации используем именно Field, т.к. работаем с классом
class UserCreate(BaseModel):
    name: Annotated[str, Field(..., title='Имя пользователя', min_length=2, max_length=20)]
    age: Annotated[int, Field(..., title='Возраст пользователя', ge=1, le=120)]

    
users = [
    {'id': 1, 'name': 'Sasha', 'age': 14},
    {'id': 2, 'name': 'Alex', 'age': 28},
    {'id': 3, 'name': 'Bob', 'age': 56},
]

posts = [
    {'id': 1, 'title': 'News 1', 'body':'Text 1', 'author': users[1]},
    {'id': 2, 'title': 'News 2', 'body':'Text 2', 'author': users[0]},
    {'id': 3, 'title': 'News 3', 'body':'Text 3', 'author': users[2]},
]

# Обработка всех постов
@app.get("/items")
async def items() -> List[Post]:
    post_object = []
    for post in posts:
        post_object.append(Post(id=post['id'], title=post['title'], body=post['body']))
    return post_object


@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user ['id'] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail='User not found')
    
    new_post_id = len(posts) + 1

    new_post = {'id': new_post_id, 'title': post.title, 'body': post.body, 'author': author}
    posts.append(new_post)

    return Post(**new_post)


@app.post("/user/add")
async def add_user(user: UserCreate) -> User:    
    new_user_id = len(users) + 1

    new_user = {'id': new_user_id, 'name': user.name, 'age': user.age}
    users.append(new_user)

    return Post(**new_user)


# Обработка динамического параметра
# ge - число 'id' должно быть >= 1
# lt - число 'id' должно быть < 100
# Здесь для аннотации используем именно Path, т.к. имеем динамический параметр 'id'
@app.get("/items/{id}")
async def items(id: Annotated[int, Path(..., title='Здесь указывается id поста', ge=1, lt=100)]) -> Post:
    for post in posts:
        if post['id'] == id:
            return Post(**post)
      
    return HTTPException(status_code=404, detail='Post not found')


# Обработка необязательного параметра - '?' или '$'
# Здесь для аннотации используем именно Query, т.к. не имеем динамичесеого параметра
@app.get("/search")
async def search(post_id: Annotated[
    Optional[int], 
    Query(title="ID of post to search for", ge=1, le=50)
]) -> Dict[str, Optional[Post]]:
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return {"data": Post(**Post)}
        raise HTTPException(status_code=404, detail='Post not found')
    else:
        return {"data": "None"}