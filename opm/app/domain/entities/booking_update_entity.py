from dataclasses import dataclass
from enum import Enum
from typing import List
from ...domain.entities.meal_type import MealType


class BookingUpdateActionEntity(str, Enum):
    update = "UPDATE"
    delete = "DELETE"


@dataclass
class BookingUpdateInfoEntity:
    name: str
    email: str
    employee_id: str
    booked_meals: List[MealType]
    consumed_meals: List[MealType]
    is_emergency: bool


@dataclass
class BookingUpdateEntity:
    action: BookingUpdateActionEntity
    booking_update_info: BookingUpdateInfoEntity


@dataclass
class BookingUpdateListEntity:
    booking_update_list: List[BookingUpdateEntity]
