from models import create_user_request
from models.credit_repay_request import CreditRepayRequest
from models.credit_request_request import CreditRequestRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.specs.response_spec import ResponseSpecs
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_spec import RequestsSpecs
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.status_code_201()
        ).post()

        return response

    def create_account_invalid_403(self):
        CrudRequester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.status_code_403()
        ).post()

    #================DEPOSIT================#

    def deposit_account(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_200()
        ).post(deposit_account_request)
        return response

    def deposit_account_invalid_400(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        CrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_400()
        ).post(deposit_account_request)

    def deposit_account_invalid_401(self, deposit_account_request: DepositAccountRequest):
        CrudRequester(
            RequestsSpecs.no_auth_headers(),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_401()
        ).post(deposit_account_request)

    # ================TRANSFER================#

    def transfer_account_request(self, transfer_account_request: TransferAccountRequest, create_user_request):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.status_code_200()
        ).post(transfer_account_request)

        return response

    def transfer_account_invalid_401(self, transfer_account_request: TransferAccountRequest, create_user_request):
        CrudRequester(
            RequestsSpecs.no_auth_headers(),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.status_code_401()
        ).post(transfer_account_request)

    # ================CREDIT================#

    def credit_request(self, credit_request_request: CreditRequestRequest, create_user_request_credit):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(
                username=create_user_request_credit.username,
                password=create_user_request_credit.password
            ),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.status_code_201()
        ).post(credit_request_request)
        return response

    def credit_request_invalid_404(self, credit_request_request: CreditRequestRequest, create_user_request_credit):
        CrudRequester(
            RequestsSpecs.auth_headers(
                username=create_user_request_credit.username,
                password=create_user_request_credit.password
            ),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.status_code_404()
        ).post(credit_request_request)

    # ================REPAY================#

    def credit_repay(self, credit_repay_request: CreditRepayRequest, create_user_request_credit):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.status_code_200()
        ).post(credit_repay_request)
        return response

    def credit_repay_invalid_422(self, credit_repay_request: CreditRepayRequest, create_user_request_credit):
        CrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.status_code_422()
        ).post(credit_repay_request)