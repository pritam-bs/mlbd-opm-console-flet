from typing import Optional, Dict
from pydantic import BaseModel
from enum import Enum
from ...data.model.error.response_error import ResponseError
from ...data.model.error.response_code import ResponseCode


class AppErrorCode(Enum):
    INVALID_INPUT = 1000
    PERMISSION_DENIED = 1001
    API_REQUEST_FAILED = 1002
    API_UNAUTHORIZED = 1003
    NETWORK = 1004
    UNKNOWN = 1004


class ErrorModel(BaseModel):
    status_code: AppErrorCode
    content: Optional[dict]


class AppException(Exception):
    def __init__(self, error: ErrorModel):
        self.error = error

    @classmethod
    def invalid_input(cls, content: Dict = None):
        _content: Dict = {"message": "Invalid input."}
        if content:
            _content.update(content)
        error = ErrorModel(
            status_code=AppErrorCode.INVALID_INPUT, content=_content)
        return AppException(error=error)

    @classmethod
    def permission_denied(cls, content: Dict = None):
        _content: Dict = {"message": "Permission denied."}
        if content:
            _content.update(content)
        error = ErrorModel(
            status_code=AppErrorCode.PERMISSION_DENIED, content=_content)
        return AppException(error=error)

    @classmethod
    def api_request(cls, content: Dict = None):
        _content: Dict = {"message": "API request failed."}
        if content:
            _content.update(content)
        error = ErrorModel(
            status_code=AppErrorCode.API_REQUEST_FAILED, content=_content)
        return AppException(error=error)

    @classmethod
    def api_unauthorized(cls, content: Dict = None):
        _content: Dict = {"message": "API request unauthorized."}
        if content:
            _content.update(content)
        error = ErrorModel(
            status_code=AppErrorCode.API_UNAUTHORIZED, content=_content)
        return AppException(error=error)

    @classmethod
    def network(cls, content: Dict = None):
        _content: Dict = {"message": "Network error occurred."}
        if content:
            _content.update(content)
        error = ErrorModel(
            status_code=AppErrorCode.NETWORK, content=_content)
        return AppException(error=error)

    @classmethod
    def unknown(cls, content: Dict = None):
        _content: Dict = {"message": "Unknown error occurred."}
        if content:
            _content.update(content)
        error = ErrorModel(
            status_code=AppErrorCode.UNKNOWN, content=_content)
        return AppException(error=error)

    @classmethod
    def from_response_error(cls, response_error: ResponseError):
        if response_error.status_code == ResponseCode.UNAUTHORIZED:
            return AppException.api_unauthorized()
        elif 400 <= response_error.status_code.value <= 599:
            content: Dict = {"code": response_error.status_code.value,
                             "message": response_error.message,
                             "data": response_error.data}
            app_exception = AppException.api_request(content=content)
            return app_exception
        elif response_error.status_code == ResponseCode.NETWORK_ERROR:
            return AppException.network()
        elif response_error.status_code == ResponseCode.INVALID_INPUT:
            return AppException.invalid_input()
        else:
            return AppException.unknown()
