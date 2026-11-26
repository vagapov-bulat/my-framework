from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse
from src.main.api.requests.requestor import Requester


class TransferAccountRequester(Requester):
    def post(self, transfer_account_request: TransferAccountRequest) -> TransferAccountResponse | Response:
        url= f"{self.base_url}/account/transfer"
        response= requests.post(
            url=url,
            headers=self.headers,
            json=transfer_account_request.model_dump()
        )

        self.response_spec(response)

        if response.status_code in  [HTTPStatus.CREATED, HTTPStatus.OK]:
            return TransferAccountResponse(**response.json())
        return response