from dataclasses import dataclass
from typing import List


@dataclass
class NewUserEntity:
    employee_id: str


@dataclass
class ModelUpdateEntity:
    new_employee_list: List[NewUserEntity]
