from pydantic import BaseModel, ValidationError
from typing import Optional, Dict
from loguru import logger


class AuthDTO(BaseModel):
    @classmethod
    def key(cls):
        return {"key": "AuthInfo"}

    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict: Dict):
        try:
            auth_dto = AuthDTO(**data_dict)
            return auth_dto
        except ValidationError as error:
            logger.info(f"Validation error: {error}")
            return None

    def to_dict(self) -> Dict:
        data = self.model_dump()
        data.update(AuthDTO.key())
        return data
