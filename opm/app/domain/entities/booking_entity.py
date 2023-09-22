from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class MealType(Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    SNACKS = "Snacks"


@dataclass
class BookingEntity:
    name: str
    email: str
    employee_id: str
    is_emergency: bool
    booked_meals: Optional[List[MealType]] = None
    consumed_meals: Optional[List[MealType]] = None
