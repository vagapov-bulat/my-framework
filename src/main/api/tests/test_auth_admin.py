import pytest
import random, string

from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_spec import RequestsSpecs
from src.main.api.specs.response_spec import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester



class TestAuthAdmin:
    # ПОЗИТИВНЫЙ КЕЙС: Авторизация с валидными данными
    def test_auth_admin_valid(self, api_manager):
        # Используем pydantic модель
        auth_admin_request = AuthLoginRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(auth_admin_request)

        # Проверки
        assert response.user.username == auth_admin_request.username
        assert response.user.role == "ROLE_ADMIN"

    # Параметры для негативного кейса с невалидными данными (пустые username, password)
    @pytest.mark.parametrize(
        "username, password",
        [
            ("", "123456"), #400
            ("admin", ""), #400
        ]
    )
    # НЕГАТИВНЫЙ КЕЙС: Авторизация с невалидными данными
    def test_auth_admin_invalid_400(self, username, password, api_manager):
        auth_admin_request = AuthLoginRequest(username=username, password=password)
        api_manager.admin_steps.login_user_invalid_400(auth_admin_request)

    # Параметры для (-) с неверным username/password (status: 401)
    @pytest.mark.parametrize(
        "username, password",
        [
            ("bulat", "123456"), # Неверный логин
            ("admin", "654321"), # Неверный пароль
        ]
    )

    # (-) Авторизация с неверным username/password
    def test_auth_admin_invalid_username_password_401(self, username, password, api_manager):
        auth_admin_request = AuthLoginRequest(username=username, password=password)
        api_manager.admin_steps.login_user_invalid_401(auth_admin_request)


    """========ПРОВЕРКИ АВТОРИЗАЦИИ ЮЗЕРА======="""

    # (+) Корректная авторизация юзера
    def test_auth_user_valid(self, api_manager, create_user_request):

        # Обращаемся к фикстуре создания пользователя
        response = api_manager.admin_steps.login_user(create_user_request)

        # Проверки
        assert response.user.username == create_user_request.username
        assert response.user.role == create_user_request.role


    # (-) Авторизация пользователя (некорректный юзернейм)
    def test_user_auth_invalid_401(self, api_manager, create_user_request):
        auth_admin_request = AuthLoginRequest(username="tester201", password="Pass123+")
        api_manager.admin_steps.login_user_invalid_401(auth_admin_request)


    # (-) Авторизация с пустым полем пароля
    def test_user_auth_missing_400(self, api_manager, create_user_request):
        auth_admin_request = AuthLoginRequest(username="tester201", password="Pass123+")
        api_manager.admin_steps.login_user_invalid_401(auth_admin_request)