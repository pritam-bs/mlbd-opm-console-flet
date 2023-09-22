from pydantic import BaseModel
from data.model.meal.meal_type import MealType


class MealBody(BaseModel):
    employee_id: str
    meals: MealType

    def to_json(self):
        json_data = self.model_dump_json()
        return json_data
