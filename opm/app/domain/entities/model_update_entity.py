from dataclasses import dataclass


@dataclass
class NewUserEntity:
    employee_id: str


@dataclass
class ModelUpdateEntity:
    new_employee_list: [NewUserEntity]
