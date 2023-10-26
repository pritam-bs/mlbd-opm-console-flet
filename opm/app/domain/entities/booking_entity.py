from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from loguru import logger
from ...domain.entities.meal_entity_type import MealEntityType


@dataclass
class BookingEntity:
    name: str
    email: str
    employee_id: str
    is_emergency: bool
    booked_meals: Optional[List[MealEntityType]] = None
    consumed_meals: Optional[List[MealEntityType]] = None

    def is_consumed(self, meal: MealEntityType) -> bool:
        if self.consumed_meals is None:
            return False
        is_consumed = self.consumed_meals and meal in self.consumed_meals
        return is_consumed
