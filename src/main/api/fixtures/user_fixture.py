import pytest

from classes.api_manager import ApiManager
from models.credit_repay_request import CreditRepayRequest
from models.credit_request_request import CreditRequestRequest
from models.deposit_account_request import DepositAccountRequest
from models.transfer_account_request import TransferAccountRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def create_user_request(api_manager):
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)
    return create_user_req

@pytest.fixture
# Фикстура создает пользователя, авторизует его, создает аккаунт, отправляет валидный запрос
def deposit_account_request(api_manager):
    # Создается и авторизуется пользователь
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    # Создается аккаунт
    create_account_req = api_manager.user_steps.create_account(create_user_req)

    # Вытягиваем id
    id_account = create_account_req.id

    deposit_account_req = DepositAccountRequest(accountId=id_account, amount=1000.5)
    return create_account_req, deposit_account_req

@pytest.fixture
def deposit_account_request(api_manager):
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)
    create_account_req = api_manager.user_steps.create_account(create_user_req)
    deposit_account_req = DepositAccountRequest(accountId=create_account_req.id, amount=1000.5)
    return create_user_req, deposit_account_req   # первый – CreateUserRequest

@pytest.fixture
def deposit_account_invalid_request_400(api_manager):
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)
    create_account_req = api_manager.user_steps.create_account(create_user_req)
    deposit_account_req = DepositAccountRequest(accountId=create_account_req.id, amount=-1000.5)
    return create_user_req, deposit_account_req

@pytest.fixture
def deposit_account_invalid_request_401(api_manager):
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)
    create_account_req = api_manager.user_steps.create_account(create_user_req)
    deposit_account_req = DepositAccountRequest(accountId=create_account_req.id, amount=1000.5)
    return create_user_req, deposit_account_req

@pytest.fixture
def transfer_account_request(api_manager):
    # Создаем пользователя и авторизуемся
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаем акк 1 и 2
    create_acc_req_1 = api_manager.user_steps.create_account(create_user_req)
    create_acc_req_2 = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id созданных аккаунтов
    id_account_1 = create_acc_req_1.id
    id_account_2 = create_acc_req_2.id

    # Пополняем счет в банке
    deposit_account_req = DepositAccountRequest(accountId=id_account_1, amount=1000.5)
    api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)

    # Запрашиваем перевод
    transfer_account_req = TransferAccountRequest(fromAccountId=id_account_1, toAccountId=id_account_2, amount=1000.5)
    return create_user_req, transfer_account_req, id_account_1, id_account_2

@pytest.fixture
def transfer_account_request_invalid_401(api_manager: ApiManager):
    # Создаем пользователя и авторизуемся
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаем акк 1 и 2
    create_acc_req_1 = api_manager.user_steps.create_account(create_user_req)
    create_acc_req_2 = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id созданных аккаунтов
    id_account_1 = create_acc_req_1.id
    id_account_2 = create_acc_req_2.id

    # Пополняем счет в банке
    deposit_account_req = DepositAccountRequest(accountId=id_account_1, amount=1000.5)
    api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)

    # Запрашиваем перевод
    transfer_account_req = TransferAccountRequest(fromAccountId=id_account_1, toAccountId=id_account_2, amount=1000.5)

    # Возвращаем тело запроса
    return create_user_req, transfer_account_req, id_account_1, id_account_2

@pytest.fixture
def create_user_request_credit(api_manager: ApiManager):
    # Создаем пользователя с ролью ROLE_CREDIT_SECRET и авторизуемся
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)

    # Возвращаем тело запроса
    return create_user_req

@pytest.fixture
# Фикстура создает пользователя, авторизуется, запрашивает и погашает кредит
def credit_repay_request(api_manager: ApiManager):
    # Создаем пользователя и авторизуемся
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаем акк
    create_acc_req = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id созданных аккаунтов
    id_account = create_acc_req.id

    # Запрашиваем кредит
    credit_request_req = CreditRequestRequest(accountId=id_account, amount=5000.5, termMonths=12)
    credit = api_manager.user_steps.credit_request(credit_request_req, create_user_req)

    # Вытягиваем id кредита
    id_credit = credit.creditId

    # Закрываем кредит
    credit_repay_req = CreditRepayRequest(creditId=id_credit, accountId=id_account, amount=5000.5)

    # Возвращаем тело запроса
    return create_user_req, credit_request_req, credit_repay_req, id_credit

@pytest.fixture
# Фикстура создает пользователя, авторизуется, запрашивает и погашает кредит с недостаточной суммой для погашения
def credit_repay_request_invalid_422(api_manager: ApiManager):
    # Создаем пользователя и авторизуемся
    create_user_req = CreateUserRequest(username="Tester2", password="Pass123+", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаем акк
    create_acc_req = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id созданных аккаунтов
    id_account = create_acc_req.id

    # Запрашиваем кредит
    credit_request_req = CreditRequestRequest(accountId=id_account, amount=5000.5, termMonths=12)
    credit = api_manager.user_steps.credit_request(credit_request_req, create_user_req)

    # Вытягиваем id кредита
    id_credit = credit.creditId

    # Закрываем кредит
    credit_repay_req = CreditRepayRequest(creditId=id_credit, accountId=id_account, amount=4000.5)

    # Возвращаем тело запроса
    return create_user_req, credit_request_req, credit_repay_req, id_credit