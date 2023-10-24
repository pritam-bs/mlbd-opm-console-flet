from ....data.api.api_client import APIClient
from ....data.model.meal.meal_type import MealType
from ....data.model.request_body.consume_meal.consume_meal_body import ConsumeMealBody


class ConsumeMealService:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def consume_meal(self, employee_id: str, meal_list: MealType):
        consume_meal_body = ConsumeMealBody(
            employee_id=employee_id, meal_data=meal_list)
        await self.api_client.path(
            '/meal-consumption'
        ).json(
            consume_meal_body.to_json()
        ).put().request()
