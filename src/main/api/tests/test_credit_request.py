from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.db.models.credit_table import Credit
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from sqlalchemy.orm import Session

class TestCreditRequest:

    # ПОЛОЖИТЕЛЬНЫЙ КЕЙС: Перевод денег с аккаунта на аккаунт
    def test_credit_request_valid(self, api_manager, create_user_request_credit, db_session: Session):
        # Создаем пользователя, авторизуемся и создаем акк
        account = api_manager.user_steps.create_account(create_user_request_credit)

        # Сохраняем id счета
        acc_id = account.id

        # Запрос на кредит
        credit_req = CreditRequestRequest(accountId=acc_id, amount=6000.0, termMonths=12)
        response = api_manager.user_steps.credit_request(credit_req, create_user_request_credit)

        # Проверки
        assert response.amount == credit_req.amount
        assert response.termMonths == credit_req.termMonths

        # Проверки БД
        credit_from_db = Credit.get_credit_by_account_id(db_session, acc_id)
        assert credit_from_db.account_id == credit_req.accountId
        assert credit_from_db.amount == credit_req.amount
        assert credit_from_db.term_months == credit_req.termMonths

    # НЕГАТИВНЫЙ КЕЙС: Запрос на получение второго кредита у одного пользователя
    def test_credit_request_invalid_404(self, api_manager, create_user_request_credit, db_session: Session):
        # Создаём аккаунт
        account = api_manager.user_steps.create_account(create_user_request_credit)
        acc_id = account.id

        # Первый запрос на кредит (успешный)
        credit_req = CreditRequestRequest(accountId=acc_id, amount=5000.0, termMonths=12)
        api_manager.user_steps.credit_request(credit_req, create_user_request_credit)

        # Второй запрос на кредит (ожидаем 404)
        api_manager.user_steps.credit_request_invalid_404(credit_req, create_user_request_credit)

        # Проверки БД
        credit_from_db = Credit.get_credit_by_account_id_all(db_session, acc_id)
        assert len(credit_from_db) == 1
