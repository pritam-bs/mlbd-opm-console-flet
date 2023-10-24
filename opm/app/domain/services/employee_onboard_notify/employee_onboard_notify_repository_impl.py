from typing import List
from opm.app.data.model.error.response_error import ResponseError
from ....data.services.employee_onboard_notify.employee_onboard_notify_service import EmployeeOnboardNotifyService
from ....domain.error.app_error import AppException
from ....domain.services.employee_onboard_notify.employee_onboard_notify_repository import EmployeeOnboardNotifyRepository


class EmployeeOnboardNotifyRepositoryImpl(EmployeeOnboardNotifyRepository):

    def __init__(self, employee_onboard_notify_service: EmployeeOnboardNotifyService) -> None:
        super().__init__(employee_onboard_notify_service)
        self.employee_onboard_notify_service = employee_onboard_notify_service

    async def submit(self, employee_list: List[str]):
        try:
            await self.employee_onboard_notify_service.notify_success(employee_list=employee_list)
            return True
        except ResponseError as response_error:
            raise AppException.from_response_error(response_error)
