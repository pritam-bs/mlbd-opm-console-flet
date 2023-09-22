from pydantic import BaseModel
from loguru import logger


class AuthBody(BaseModel):
    client_name: str
    password: str

    def to_json(self):
        json_data = self.model_dump_json()
        return json_data
