from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.requests.requestor import Requester


class CreditRequestRequester(Requester):
    def post(self, credit_request_request: CreditRequestRequest) -> CreditRequestResponse | Response:
        url= f"{self.base_url}/credit/request"
        response= requests.post(
            url=url,
            headers=self.headers,
            json=credit_request_request.model_dump()
        )

        self.response_spec(response)

        if response.status_code in  [HTTPStatus.CREATED, HTTPStatus.OK]:
            return CreditRequestResponse(**response.json())
        return response