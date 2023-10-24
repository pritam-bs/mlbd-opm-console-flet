from ....domain.error.app_error import AppException
from ....data.model.error.response_error import ResponseError
from ....domain.entities.meal_type import MealType
from ....data.services.meal.consume_meal_service import ConsumeMealService
from ....domain.services.meal.consume_meal_repository import ConsumeMealRepository
from typing import List


class ConsumeMealRepositoryImpl(ConsumeMealRepository):
    def __init__(self, consume_meal_service: ConsumeMealService) -> None:
        self.consume_meal_service = consume_meal_service

    async def submit(self, employee_id: str, meals: List[MealType]):
        try:
            await self.consume_meal_service.consume_meal(employee_id=employee_id, meal_list=meals)
            return True
        except ResponseError as response_error:
            raise AppException.from_response_error(response_error)
