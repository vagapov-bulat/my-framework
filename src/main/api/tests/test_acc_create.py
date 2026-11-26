import requests

from classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session


class TestBankAccCreate:

    # (+) Создание банк. аккаунта
    def test_create_account_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.create_account(create_user_request)

        # Проверки
        assert response.balance == 0

        # Проверки БД
        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Account is not created, ID is not in DB'
        assert account_from_db.balance is not None, 'Balance field is not found in DB'

    # НЕГАТИВНАЯ Проверка некорректного тела запроса при пополнении баланса (400)
    def test_create_account_invalid_400(self):
        auth_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={"username": "admin",
                  "password": "123456"
                  },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        # Проверяем ожидаемый статус 200
        assert auth_admin_response.status_code == 200
        # Сохраняем токен ADMIN
        adm_token = auth_admin_response.json().get("token")

        # (+) Создание user, status: 200
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Kot133",
                "password": "Pass123+",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "*/*",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {adm_token}"
            }
        )
        # Проверяем status 200
        assert create_user_response.status_code == 200

        # (+) Проверка авторизации USER после регистрации
        auth_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Kot133",
                "password": "Pass123+",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        # Проверяем status 200
        assert auth_user_response.status_code == 200
        # Сохраняем токен авторазации USER
        user_token = auth_user_response.json().get("token")

        # Создаем банковский аккаунт как USER
        bank_acc_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {user_token}"
            }
        )

        # Проверяем ожидаемый статус 201
        assert bank_acc_response.status_code == 201
        # Проверяем ожидаемый balance = 0
        assert bank_acc_response.json().get("balance") == 0
        # Вытягиваем Id аккаунта
        user_id = bank_acc_response.json().get("id")

        # Пополнение банковского счета на X Сумму
        deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": "1234",
                "amount": 100
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {user_token}"
            }
        )

        # Проверяем ожидаемый статус 400
        assert deposit_response.status_code == 400

    # (-) Пополнение баланса без токена авторизации
    def test_create_account_invalid_401(self):
        auth_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={"username": "admin",
                  "password": "123456"
                  },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        # Проверяем ожидаемый статус 200
        assert auth_admin_response.status_code == 200
        # Сохраняем токен ADMIN
        adm_token = auth_admin_response.json().get("token")

        # (+) Создание user, status: 200
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Kot143",
                "password": "Pass123+",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "*/*",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {adm_token}"
            }
        )
        # Проверяем status 200
        assert create_user_response.status_code == 200

        # (+) Проверка авторизации USER после регистрации
        auth_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Kot143",
                "password": "Pass123+",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        # Проверяем status 200
        assert auth_user_response.status_code == 200
        # Сохраняем токен авторазации USER
        user_token = auth_user_response.json().get("token")

        # Создаем банковский аккаунт как USER
        bank_acc_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {user_token}"
            }
        )

        # Проверяем ожидаемый статус 201
        assert bank_acc_response.status_code == 201
        # Проверяем ожидаемый balance = 0
        assert bank_acc_response.json().get("balance") == 0
        # Вытягиваем Id аккаунта
        user_id = bank_acc_response.json().get("id")

        # Пополнение банковского счета на X Сумму
        deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": user_id,
                "amount": 100
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer"
            }
        )

        # Проверяем ожидаемый статус 401
        assert deposit_response.status_code == 401

    # НЕГАТИВНЫЙ КЕЙС: Попытка создать аккаунт из-под админа
    def test_create_account_invalid_403(self, api_manager: ApiManager, db_session: Session):
        # Количество записей в БД до отправки запроса
        before_count = Account.count_all(db_session)

        api_manager.user_steps.create_account_invalid_403()

        after_count = Account.count_all(db_session)
        # Проверки БД
        assert before_count == after_count, 'Account is created = ERROR'