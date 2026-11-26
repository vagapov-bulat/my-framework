import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.apps.mini_apps import GenUsername
from sqlalchemy.orm import Session



@pytest.mark.test
class TestCreateUser:

    # ПОЗИТИВНЫЙ кейс на создание USER
    def test_create_user_valid(self, api_manager: ApiManager, db_session: Session):

        # Создание user, status: 200
        # Используем pydantic модель для запроса от Юзера
        create_user_request = CreateUserRequest(username="Gosha13", password="Pass123+", role="ROLE_USER")
        response = api_manager.admin_steps.create_user(create_user_request)

        # Проверки
        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        # Проверки БД
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username

    # Параметры для НЕГАТИВНЫХ СЦЕНАРИЕВ создания USER
    @pytest.mark.parametrize(
        ("username", "password"),
        [
            # Для проверки username
            ("Булатп", "Pass123+"), # (-) Кириллица
            ("Bt", "Pass123+"), # (-) < 3 символа (lat)
            ("Bulaaaaaaaagaaaat", "Pass123+"), # (-) > 15 символа (16 симв, lat)
            ("Bulakt%", "Pass123+"), # (-) спец. символ
            # Для проверки password
            ("Bulat3", "Пассворд123+"), # (-) Кириллица
            ("Bulat3", "Pa123+"), # (-) < 8 символов (lat)
            ("Bulat3", "password123+"), # (-) < 1 загл. букв.
            ("Bulat3", "Password123"), # (-) < 1 спец. симв.
            ("Bulat3", "Password+"), # (-) < 1 цифры
        ]
    )

    # НЕГАТИВНЫЙ кейс с невалидными полями username/password при создании пользователя
    def test_create_user_invalid_username_400(self, api_manager: ApiManager, db_session: Session, username: str, password: str):
        #gen_username = GenUsername.generate_username()
        # Создаем пользователя
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid_400(create_user_request)

        # Проверки БД: Проверяем что в БД не записался пользователь, т.к. он invalid_400
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'User created - ERROR'

    # НЕГАТИВНЫЙ кейс на проверку на неверного токена (status 401)
    def test_create_user_invalid_token_401(self, api_manager: ApiManager, db_session: Session):
        gen_username = GenUsername.generate_username()
        create_user_request = CreateUserRequest(username=gen_username, password="Pass123+", role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid_401(create_user_request)

        # Проверки БД
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'User created - ERROR'


