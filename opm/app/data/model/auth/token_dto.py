from pydantic import BaseModel, ValidationError
import json
from loguru import logger
from ....data.model.error.response_error import ResponseError


class TokenDTO(BaseModel):
    access_token: str
    refresh_token: str

    @classmethod
    def from_json(cls, json_data):
        try:
            token_dto = TokenDTO.model_validate_json(json_data)
            return token_dto
        except ValueError as e:
            logger.debug(f"Value error: {e}")
            raise ResponseError.validation()

    @classmethod
    def from_dict(cls, dict):
        try:
            token_dto = TokenDTO(**dict)
            return token_dto
        except ValidationError as validation_error:
            logger.debug(f"Validation error: {validation_error}")
            raise ResponseError.validation()
