import pytest
from src.main.api.db.engine import engine, SessionLocal

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()

    # Транзакция -- пакет, в к-й мы складываем несколько операций с БД
    transaction = connection.begin()

    # Сессия -- объект ORM, через который мы выполняем операции с БД
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        # Закрываем сессию
        session.close()
        # Откат транзакции
        transaction.rollback()
        # Закрываем соединение с БД
        connection.close()
