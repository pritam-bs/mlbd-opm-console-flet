from typing import List
from ....data.api.api_client import APIClient
from ....data.model.request_body.employee_list.employee_list_body import EmployeeListBody


class EmployeeOnboardNotifyService:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def notify_success(self, employee_list: List[str]) -> bool:
        employee_list_body = EmployeeListBody(employees=employee_list)
        response = await self.api_client.path(
            '/face-registration/success'
        ).json(
            employee_list_body.to_json()
        ).post().request()

        if response is not None:
            return True
        else:
            return False
