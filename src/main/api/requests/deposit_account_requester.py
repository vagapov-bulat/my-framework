from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.requestor import Requester


class DepositAccountRequester(Requester):
    def post(self, deposit_account_request: DepositAccountRequest) -> DepositAccountResponse | Response:
        url= f"{self.base_url}/account/deposit"
        response= requests.post(
            url=url,
            headers=self.headers,
            json=deposit_account_request.model_dump()
        )

        self.response_spec(response)

        if response.status_code in  [HTTPStatus.CREATED, HTTPStatus.OK]:
            return DepositAccountResponse(**response.json())
        return response