from pydantic import BaseModel
from .meal_type import MealType


class MealDTO(BaseModel):
    employee_id: str
    meal: MealType

    @classmethod
    def from_json(cls, json_data):
        meal_dto = MealDTO.model_validate_json(json_data=json_data)
        return meal_dto
