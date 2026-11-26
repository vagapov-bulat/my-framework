from src.main.api.foundation.endpoint import Endpoint
from typing import Callable, Dict


class HttpRequester:
    def __init__(self, request_spec: Dict, endpoint: Endpoint, response_spec: Callable):
        self.request_spec = request_spec # Хэдеры
        self.endpoint = endpoint  # Тело запроса: полня, URL
        self.response_spec = response_spec # Ответ, статус коды
