from dataclasses import dataclass
from enum import Enum
from typing import List


class BookingUpdateActionEntity(str, Enum):
    update = "UPDATE"
    delete = "DELETE"


class MealType(Enum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    SNACKS = "SNACKS"


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
