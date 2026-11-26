from src.main.api.fixtures.user_fixture import deposit_account_invalid_request_401, deposit_account_invalid_request_400
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session

class TestAccDeposit:

    # ПОЛОЖИТЕЛЬНАЯ ПРОВЕРКА: ПОПОЛНЕНИЯ БАЛАНСА
    def test_deposit_account_valid_200(self, api_manager: ApiManager, deposit_account_request, db_session: Session):
        # Берем фикстуру deposit_account_request
        create_user_req, deposit_account_req = deposit_account_request
        response = api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)
        assert response.balance == deposit_account_req.amount

        # Проверки БД
        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db.balance == deposit_account_req.amount, "Balance in DB should be equal to deposit_account_req.amount"

    # НЕГАТИВНАЯ ПРОВЕРКА: некорректного тела запроса при пополнении баланса (400)
    def test_bank_acc_invalid_400(self, api_manager: ApiManager, deposit_account_invalid_request_400, db_session: Session):
        create_user_req, deposit_account_req = deposit_account_invalid_request_400
        api_manager.user_steps.deposit_account_invalid_400(create_user_req, deposit_account_req)

        # Проверки БД
        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        # Проверяем наличие Баланса
        assert account_from_db is not None, "Account should exist"
        # Если ошибка 400, то баланс не меняется
        assert account_from_db.balance == 0, "Balance in DB should not change if invalid Response"

    # НЕГАТИВНАЯ ПРОВЕРКА: Пополнение баланса без токена авторизации
    def test_bank_acc_invalid_401(self, api_manager: ApiManager, deposit_account_invalid_request_401, db_session: Session):
        create_user_req, deposit_account_req = deposit_account_invalid_request_401
        api_manager.user_steps.deposit_account_invalid_401(deposit_account_req)

        # Проверки БД
        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        # Проверяем наличие Баланса
        assert account_from_db is not None, "Account should exist"
        # Если ошибка 401, то баланс не меняется
        assert account_from_db.balance == 0, "Balance in DB should not change if invalid Response"