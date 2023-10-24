from typing import Union, List

from ...domain.error.app_error import AppException
from ...domain.services.employee_onboard_notify.employee_onboard_notify_repository import EmployeeOnboardNotifyRepository


class EmployeeOnboardNotifyUsecase:
    def __init__(self, employee_onboard_notify_repository: EmployeeOnboardNotifyRepository):
        self.employee_onboard_notify_repository = employee_onboard_notify_repository

    async def run(self, employee_list: List[str]) -> Union[bool, AppException]:
        return await self.employee_onboard_notify_repository.submit(employee_list=employee_list)
