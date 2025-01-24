from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL для подключения к БД
SQL_DB_URL = 'sqlite:///./test.db'

# Описываем движок для подключения. Снимаем ограничение на кол-во подключений к БД
engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False})

# Для взаимодействия с сессией. Отключили автоматическию синхронизацию. Покдлючаем движок
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Создается базовый класс из описанных моделей в models.py
Base = declarative_base()