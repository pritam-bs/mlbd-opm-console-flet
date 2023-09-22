from enum import Enum


class ResponseCode(Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503

    # Additional errors
    UNKNOWN_ERROR = 1000
    NETWORK_ERROR = 1001
    INVALID_INPUT = 1002
    VALIDATION_ERROR = 1003

    @classmethod
    def map_status_to_enum(cls, status_code):
        try:
            return ResponseCode(status_code)
        except ValueError:
            return ResponseCode.UNKNOWN_ERROR

    @classmethod
    def is_successful(cls, status_code) -> bool:
        success_statuses = {
            ResponseCode.OK.value,
            ResponseCode.CREATED.value,
            ResponseCode.ACCEPTED.value,
            ResponseCode.NO_CONTENT.value
        }
        if status_code in success_statuses:
            return True
        else:
            return False
