from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


posts = [
    {'id': 1, 'title': 'News 1', 'body':'Text 1'},
    {'id': 2, 'title': 'News 2', 'body':'Text 2'},
    {'id': 3, 'title': 'News 3', 'body':'Text 3'},
]

# Обработка всех постов
@app.get("/items")
async def items() -> list:
    return posts


# Обработка динамического параметра
@app.get("/items/{id}")
async def items(id: int) -> dict:
    for post in posts:
        if post['id'] == id:
            return post
      
    return HTTPException(status_code=404, detail='Post not found')


# Обработка необязательного параметра
@app.get("/search")
async def search(post_id: Optional[int] = None) -> dict:
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return post
    else:
        return {"data": "No post id provided"}
    