from typing import List
from pydantic import BaseModel


class EmployeeListBody(BaseModel):
    employees: List[str]

    def to_json(self):
        json_data = self.model_dump_json()
        return json_data
