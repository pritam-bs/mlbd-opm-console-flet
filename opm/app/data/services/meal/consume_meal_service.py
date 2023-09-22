from ....data.api.api_client import APIClient
from ....data.model.meal.meal_type import MealType
from ....data.model.request_body.meal.meal_body import MealBody
from ....data.model.meal.meal_dto import MealDTO


class ConsumeMealService:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def consume_meal(self, employee_id: str, meal: MealType) -> bool:
        meal_body = MealBody(employee_id=employee_id, meals=meal)
        response = await self.api_client.path(
            '/consume_meal'
        ).json(
            meal_body.to_json()
        ).post().request()

        meal_dto = MealDTO.from_json(response)
        return meal_dto
