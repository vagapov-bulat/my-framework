# Здесь пишем движок SQLALCHEMY, к-й управляет соединением с БД

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main.api.configs.config import Config

# Открываем соединение.
# echo = False - отключаем вывод логов sql
engine = create_engine(Config.fetch('dataBaseUrl'), echo=False)
SessionLocal = sessionmaker(bind=engine)
