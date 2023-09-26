from typing import List, Optional, Dict
from typing_extensions import TypedDict
from pydantic import BaseModel, ValidationError
from ....data.model.meal.meal_type import MealType
from loguru import logger
from ....data.model.error.response_error import ResponseError
from pydantic import TypeAdapter


class BookingStatus(BaseModel):
    employee_id: str
    name: str
    email: str
    booked_meals: Optional[List[MealType]] = None
    consumed_meals: Optional[List[MealType]] = None
    is_emergency: bool


class BookingDTO(BaseModel):
    bookings: List[BookingStatus]

    @classmethod
    def from_json(cls, json_data):
        try:
            type_adapter = TypeAdapter(List[BookingStatus])
            booking_list = type_adapter.validate_json(json_data)
            booking_dto = BookingDTO(bookings=booking_list)
            return booking_dto
        except ValueError as e:
            logger.debug(f"Value error: {e}")
            raise ResponseError.validation()

    @classmethod
    def from_dict(cls, dict: List[Dict]):
        try:
            type_adapter = TypeAdapter(List[BookingStatus])
            booking_list = type_adapter.validate_python(dict, strict=None)
            booking_dto = BookingDTO(bookings=booking_list)
            return booking_dto
        except ValidationError as error:
            logger.info(f"Validation error: {error}")
            raise ResponseError.validation()
