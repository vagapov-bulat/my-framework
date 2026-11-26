from classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit

class TestCreditRepay:

    # ПОЛОЖИТЕЛЬНЫЙ КЕЙС: Погашение кредита
    def test_credit_repay_valid(self, api_manager: ApiManager, credit_repay_request, db_session: Session):
        create_user_req, credit_request_req, credit_repay_req, id_credit = credit_repay_request
        response = api_manager.user_steps.credit_repay(credit_repay_req, create_user_req)

        assert response.amountDeposited == credit_repay_req.amount
        assert response.creditId == id_credit

        # Проверки БД
        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_request_req.accountId)
        assert credit_from_db.account_id == credit_request_req.accountId
        assert credit_from_db.amount == credit_request_req.amount
        assert credit_from_db.term_months == credit_request_req.termMonths


    # НЕГАТИВНЫЙ КЕЙС Суммы недостаточно для погашения кредита
    def test_credit_repay_not_enough_money_422(self, api_manager: ApiManager, credit_repay_request_invalid_422, db_session: Session):
        create_user_req, credit_request_req, credit_repay_req, id_credit = credit_repay_request_invalid_422
        api_manager.user_steps.credit_repay_invalid_422(credit_repay_req, create_user_req)

        # Проверки БД
        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_request_req.accountId)
        assert credit_from_db.account_id == credit_request_req.accountId
        assert credit_from_db.amount == credit_request_req.amount
        assert credit_from_db.term_months == credit_request_req.termMonths