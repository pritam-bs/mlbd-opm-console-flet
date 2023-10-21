from typing import Dict, List
from pydantic import BaseModel, TypeAdapter, ValidationError
from loguru import logger
from ..error.response_error import ResponseError


class NewUserDTO(BaseModel):
    employee_id: str


class ModelUpdateDTO(BaseModel):
    onboarded_users: List[NewUserDTO]

    @classmethod
    def from_json(cls, json_data):
        try:
            type_adapter = TypeAdapter(List[NewUserDTO])
            new_users = type_adapter.validate_json(json_data)
            model_update_dto = ModelUpdateDTO(onboarded_users=new_users)
            return model_update_dto
        except ValueError as e:
            logger.debug(f"Value error: {e}")

    @classmethod
    def from_dict(cls, dict: List[Dict]):
        try:
            type_adapter = TypeAdapter(List[NewUserDTO])
            new_users = type_adapter.validate_python(dict, strict=None)
            model_update_dto = ModelUpdateDTO(onboarded_users=new_users)
            return model_update_dto
        except ValidationError as error:
            logger.info(f"Validation error: {error}")
