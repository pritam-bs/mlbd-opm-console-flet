from typing import List
from ....domain.entities.meal_entity_type import MealEntityType
from ....data.services.meal.consume_meal_service import ConsumeMealService


class ConsumeMealRepository:
    def __init__(self, consume_meal_service: ConsumeMealService) -> None:
        pass

    async def submit(self, employee_id: str, meals: List[MealEntityType]):
        pass
