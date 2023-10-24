from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from loguru import logger
from ...domain.entities.meal_type import MealType


@dataclass
class BookingEntity:
    name: str
    email: str
    employee_id: str
    is_emergency: bool
    booked_meals: Optional[List[MealType]] = None
    consumed_meals: Optional[List[MealType]] = None

    def is_consumed(self, meal: MealType) -> bool:
        if self.consumed_meals is None:
            return False
        is_consumed = self.consumed_meals and meal in self.consumed_meals
        logger.debug(f"Is {meal.value} consumed: {is_consumed}")
        return is_consumed
