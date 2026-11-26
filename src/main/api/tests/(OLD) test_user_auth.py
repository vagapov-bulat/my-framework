import requests, pytest
import random, string
from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.auth_login_response import AuthLoginResponse
from src.main.api.models.create_user_request import CreateUserRequest




# Генератор USERNAME
def generate_username(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class TestUserLogin:

    # (+) Корректная авторизация юзера
    def test_auth_user_valid(self):
        gen_username = generate_username()
        # (+) авторизация ADMIN
        # Используем pydantic модель
        auth_admin_request = AuthLoginRequest(username="admin", password="123456")

        auth_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=auth_admin_request.model_dump(),
            headers={
                "accept": "application / json",
                "Content-Type": "application/json"
            }
        )

        # Проверки
        assert auth_admin_response.status_code == 200
        # Используем модель для ответа запроса
        auth_login_response = AuthLoginResponse(**auth_admin_response.json())

        # Проверки
        assert auth_admin_request.username == auth_login_response.user.username
        assert auth_login_response.user.role == "ROLE_ADMIN"

        token = auth_admin_response.json()["token"]

        # (+) создание USER
        # Используем pydantic модель для запроса от Юзера
        create_user_request = CreateUserRequest(username=gen_username, password="Pass123+", role="ROLE_USER")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json= create_user_request.model_dump(),
            headers={
                "accept": "*/*",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        # Проверки
        assert create_user_response.status_code == 200


        # Корректная авторизация созданного пользователя
        # (+) Проверка авторизации USER после регистрации
        auth_admin_request = AuthLoginRequest(username="User11", password="Pass123+", role="ROLE_USER")

        auth_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json= auth_admin_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        # Проверяем status 200
        assert auth_user_response.status_code == 200

        # Используем модель для ответа запроса
        auth_login_response = AuthLoginResponse(**auth_user_response.json())

        # Проверки
        assert auth_admin_request.username == auth_login_response.user.username
        assert auth_login_response.user.role == "ROLE_USER"

    # (-) Авторизация пользователя (некорректный юзернейм)
    def test_user_auth_invalid(self):
        # Генерируем username
        gen_username = generate_username()

        # Авторизация админа
        # Используем pydantic модель
        auth_admin_request = AuthLoginRequest(username="admin", password="123456")

        auth_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=auth_admin_request.model_dump(),
            headers={
                "accept": "application / json",
                "Content-Type": "application/json"
            }
        )

        # Проверки
        assert auth_admin_response.status_code == 200
        # Используем модель для ответа запроса
        auth_login_response = AuthLoginResponse(**auth_admin_response.json())

        # Проверки
        assert auth_admin_request.username == auth_login_response.user.username
        assert auth_login_response.user.role == "ROLE_ADMIN"

        token = auth_admin_response.json()["token"]


        # (-) Авторизация юзера с неверным логином или паролем (401)
        create_user_request = CreateUserRequest(username=gen_username+'1', password="Pass123+", role="ROLE_USER")
        auth_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=create_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        # Проверяем status 401 (неверный username/password)
        assert auth_user_response.status_code == 401

   # (-) Авторизация с пустым полем пароля
    def test_user_auth_missing(self):
        # Генерируем username
        gen_username = generate_username()
        # (+) авторизация ADMIN
        # Используем pydantic модель
        auth_admin_request = AuthLoginRequest(username="admin", password="123456")

        auth_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=auth_admin_request.model_dump(),
            headers={
                "accept": "application / json",
                "Content-Type": "application/json"
            }
        )

        # Проверки
        assert auth_admin_response.status_code == 200
        # Используем модель для ответа запроса
        auth_login_response = AuthLoginResponse(**auth_admin_response.json())

        # Проверки
        assert auth_admin_request.username == auth_login_response.user.username
        assert auth_login_response.user.role == "ROLE_ADMIN"

        token = auth_admin_response.json()["token"]

        create_user_request = CreateUserRequest(username=gen_username + '1', password="", role="ROLE_USER")

        auth_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=create_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        # Проверяем status 400 (пустой username/password)
        assert auth_user_response.status_code == 400