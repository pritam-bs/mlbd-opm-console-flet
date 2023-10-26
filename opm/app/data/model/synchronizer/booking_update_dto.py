from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, TypeAdapter, ValidationError
from loguru import logger
from typing import List
from pydantic import BaseModel
from ....data.model.meal.meal_type import MealType


class BookingUpdateActionDTO(str, Enum):
    update = "UPDATE"
    delete = "DELETE"


class BookingUpdateInfoDTO(BaseModel):
    name: str
    email: str
    employee_id: str
    booked_meals: Optional[List[MealType]] = None
    consumed_meals: Optional[List[MealType]] = None
    is_emergency: bool


class BookingUpdateDTO(BaseModel):
    action: BookingUpdateActionDTO
    booking_data: BookingUpdateInfoDTO


class BookingUpdateListDTO(BaseModel):
    booking_update_list: List[BookingUpdateDTO]

    @classmethod
    def from_json(cls, json_data):
        try:
            type_adapter = TypeAdapter(List[BookingUpdateDTO])
            booking_update_list = type_adapter.validate_json(json_data)
            model_update_list_dto = BookingUpdateListDTO(
                booking_update_list=booking_update_list)
            return model_update_list_dto
        except ValueError as e:
            logger.debug(f"Value error: {e}")

    @classmethod
    def from_dict(cls, data: List[Dict]):
        try:
            type_adapter = TypeAdapter(List[BookingUpdateDTO])
            booking_update_list = type_adapter.validate_python(
                data, strict=None)
            model_update_list_dto = BookingUpdateListDTO(
                booking_update_list=booking_update_list)
            return model_update_list_dto
        except ValidationError as error:
            logger.info(f"Validation error: {error}")
