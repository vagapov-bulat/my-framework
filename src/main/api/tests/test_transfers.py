from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.account_table import Account
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from sqlalchemy.orm import Session


class TestTransfer:
    # ПОЛОЖИТЕЛЬНАЯ ПРОВЕРКА: Перевод денег с аккаунта на аккаунт

    def test_transfer_valid(self, api_manager: ApiManager,transfer_account_request, db_session: Session):
        # Вытягиваем из фикстуры transfer_account_request
        create_user_req, transfer_account_req, id_account_1, id_account_2 = transfer_account_request
        response = api_manager.user_steps.transfer_account_request(transfer_account_req, create_user_req)

        # Проверки
        assert response.fromAccountId == transfer_account_req.fromAccountId
        assert response.toAccountId == transfer_account_req.toAccountId

        # Проверки БД
        transaction_from_db_1 = Transaction.get_transaction_from_account_id(db_session, id_account_1)
        assert transaction_from_db_1.from_account_id == transfer_account_req.fromAccountId

        transaction_from_db_2 = Transaction.get_transaction_to_account_id(db_session, id_account_2)
        assert transaction_from_db_2.to_account_id == transfer_account_req.toAccountId


    # НЕГАТИВНАЯ ПРОВЕРКА: Перевод средств с 1 счета на 2 без токена авторизации
    def test_bank_acc_invalid_401(self, api_manager: ApiManager, transfer_account_request_invalid_401, db_session: Session):
        # Вытягиваем из фикстуры transfer_account_request
        create_user_req, transfer_account_req, id_account_1, id_account_2 = transfer_account_request_invalid_401
        api_manager.user_steps.transfer_account_invalid_401(transfer_account_req, create_user_req)

        # Проверки БД
        transaction_from_db_1 = Transaction.get_transaction_from_account_id(db_session, id_account_2)
        assert transaction_from_db_1 is None