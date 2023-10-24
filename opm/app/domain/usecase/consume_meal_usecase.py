from typing import List, Union
from ...domain.entities.meal_entity_type import MealEntityType
from ...domain.error.app_error import AppException
from ...domain.services.meal.consume_meal_repository import ConsumeMealRepository


class ConsumeMealUsecase:
    def __init__(self, consume_meal_repository: ConsumeMealRepository):
        self.consume_meal_repository = consume_meal_repository

    async def run(self, employee_id: str, meals: List[MealEntityType]) -> Union[bool, AppException]:
        return await self.consume_meal_repository.submit(employee_id=employee_id, meals=meals)
