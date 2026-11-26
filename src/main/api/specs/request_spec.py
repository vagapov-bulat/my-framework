import requests

from configs.config import Config
from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.auth_login_response import AuthLoginResponse



class RequestsSpecs:
    @staticmethod
    def base_headers():
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        request = AuthLoginRequest(username=username, password=password)
        response = requests.post(
            url= f"{Config.fetch('backendUrl')}/auth/token/login",
            json= request.model_dump(),
            headers=RequestsSpecs.base_headers()
        )

        if response.status_code == 200:
            response_data = AuthLoginResponse(**response.json())
            token = response_data.token

            headers = RequestsSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"

            return headers
        raise Exception("Failed Authorization")

    @staticmethod
    def no_auth_headers():
        return RequestsSpecs.base_headers()


