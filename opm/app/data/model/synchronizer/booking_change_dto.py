from typing import Dict
from pydantic import BaseModel, ValidationError
from loguru import logger
from ....data.model.error.response_error import ResponseError


class BookingChangeDTO(BaseModel):
    employee_id: str

    @classmethod
    def from_json(cls, json_data):
        try:
            booking_change_dto = BookingChangeDTO.model_validate_json(
                json_data=json_data)
            return booking_change_dto
        except ValueError as e:
            logger.debug(f"Value error: {e}")
            raise ResponseError.validation()

    @classmethod
    def from_dict(cls, dict: Dict):
        try:
            booking_change_dto = BookingChangeDTO(**dict)
            return booking_change_dto
        except ValidationError as error:
            logger.info(f"Validation error: {error}")
            raise ResponseError.validation()
