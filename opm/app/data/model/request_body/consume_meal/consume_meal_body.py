from typing import List
from pydantic import BaseModel
from .....data.model.meal.meal_type import MealType


class ConsumeMealBody(BaseModel):
    employee_id: str
    meal_data: List[MealType]

    def to_json(self):
        json_data = self.model_dump_json()
        return json_data
