from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    age: int


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    # Предустановленный класс, который дает понимание для программы, что подключаем orm (в данном случае - алхимия)
    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    body: str
    author_id: int


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    author: User

    # Предустановленный класс, который дает понимание для программы, что подключаем orm (в данном случае - алхимия)
    # На основе данного класса будет создана таблица в БД
    class Config:
        orm_mode = True
