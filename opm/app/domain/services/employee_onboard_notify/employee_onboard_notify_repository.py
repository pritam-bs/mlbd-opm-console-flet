from ....data.services.employee_onboard_notify.employee_onboard_notify_service import EmployeeOnboardNotifyService
from typing import List


class EmployeeOnboardNotifyRepository:
    def __init__(self, employee_onboard_notify_service: EmployeeOnboardNotifyService) -> None:
        pass

    async def submit(self, employee_list: List[str]):
        pass
