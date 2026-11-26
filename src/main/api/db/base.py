# ОТСЮДА НАСЛЕДУЮТСЯ ВСЕ МОДЕЛЬКИ
# Здесь создается базовый класс, который хранит метаданные всех таблиц

from sqlalchemy.orm import declarative_base

Base = declarative_base()
