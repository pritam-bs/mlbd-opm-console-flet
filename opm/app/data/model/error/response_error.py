from aiohttp import ClientResponse
from .response_code import ResponseCode


class ResponseError(Exception):
    def __init__(self, status_code: ResponseCode, message: str = None, data: any = None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def __str__(self):
        if self.message:
            return f"HTTP Status {self.status_code}: {self.message}"
        else:
            return f"HTTP Status {self.status_code}"

    @classmethod
    def from_response(cls, response: ClientResponse):
        """
        Create a ResponseError instance from an aiohttp.ClientResponse.
        """
        status_code = ResponseCode(response.status)
        data = response.json() if response.headers.get(
            'content-type') == 'application/json' else None
        message = f"Request failed with status code {status_code.value}"

        return cls(status_code, message, data)

    @classmethod
    def network(cls):
        message = "Request failed due to network error"
        return cls(ResponseCode.NETWORK_ERROR, message, None)

    @classmethod
    def unknown(cls):
        message = "Request failed due to unknown error"
        return cls(ResponseCode.UNKNOWN_ERROR, message, None)

    @classmethod
    def input(cls):
        message = "Request failed due to invalid input"
        return cls(ResponseCode.INVALID_INPUT, message, None)

    @classmethod
    def validation(cls):
        message = "Request failed due to validation error"
        return cls(ResponseCode.VALIDATION_ERROR, message, None)
