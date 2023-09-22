from typing import Dict
from aiohttp import (
    BasicAuth,
    ClientResponse,
    ClientResponseError,
    ClientSession,
    TraceConfig,
    TraceRequestStartParams,
    hdrs,
    ClientTimeout,
    ClientError,
    ClientResponseError,
)

from ...data.api.client import RetryClient
from ...data.api.retry_options import ListRetry
from ...data.model.error.response_error import ResponseError
from loguru import logger
import asyncio
from ...dependency_containers.local_data_container import LocalDataContainer
from ...data.model.auth.auth_dto import AuthDTO
from ...data.api.token_refresher import token_refresh
from ..model.error.response_code import ResponseCode


class APIClient:

    def __init__(self, base_url) -> None:
        self._base_url = base_url
        self._timeout = ClientTimeout(total=60, connect=30)
        self._method = None
        self._path = None
        self._headers = {}
        self._params = {}
        self._json = None
        self._session = ClientSession(
            timeout=self._timeout, base_url=self._base_url)
        retry_options = ListRetry(
            delays=[10]*3,
            statuses={ResponseCode.UNAUTHORIZED.value},
            exceptions={ConnectionError},
            retry_all_server_errors=True,
            evaluate_response_callback=self.evaluate_response)
        self._retry_client = RetryClient(
            client_session=self._session,
            retry_options=retry_options)
        self.local_data_container = LocalDataContainer()
        self.auth_local_datasource = self.local_data_container.auth_local_datasource()

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._close())

    async def _close(self):
        if self._session is not None:
            await self._session.close()

    async def evaluate_response(self, response: ClientResponse) -> bool:
        status = ResponseCode.map_status_to_enum(response.status)
        if status == ResponseCode.UNAUTHORIZED:
            auth_dto = self.auth_local_datasource.get()
            refresh_token = auth_dto.refresh_token
            try:
                new_token_dict = await token_refresh(refresh_token=refresh_token)
                auth_dto = AuthDTO(**new_token_dict)
                self.auth_local_datasource.save(auth_dto=auth_dto)
                return True
            except ValueError as e:
                logger.info(e)
                return False
        else:
            return False

    def get(self):
        self._method = hdrs.METH_GET
        return self

    def post(self):
        self._method = hdrs.METH_POST
        return self

    def path(self, path):
        self._path = path
        return self

    def headers(self, headers={}, should_add_token: bool = True):
        self._headers.update(headers)
        if should_add_token:
            auth_dto = self.auth_local_datasource.get()
            access_token = auth_dto.access_token
            authorization_headers = {
                'Authorization': f'Bearer {access_token}',
            }
            self._headers.update(authorization_headers)

        return self

    def params(self, params):
        self._params = params
        return self

    def json(self, json_data):
        self._json = json_data
        return self

    async def request(self):
        try:
            async with self._retry_client.request(
                    method=self._method,
                    headers=self._headers,
                    params=self._params,
                    url=self._path,
                    json=self._json) as response:
                response.raise_for_status()
                result = await response.json()
                return result
        except ClientResponseError as e:
            logger.debug(f"AIOHTTP Client Response Error: {e}")
            raise ResponseError.from_response(response)
        except ConnectionError as e:
            logger.debug(f"AIOHTTP Connection Error: {e}")
            raise ResponseError.network()
        except ClientError as e:
            logger.debug(f"AIOHTTP Client Error: {e}")
            raise ResponseError.input()
        except Exception as e:
            logger.debug(f"Unexpected Error: {e}")
            raise ResponseError.unknown()

    def get_saved_token(self) -> AuthDTO:
        auth_dto = self.auth_local_datasource.get()
        return auth_dto

    def save_token(self, auth_dict: Dict):
        auth_dto = AuthDTO(**auth_dict)
        self.auth_local_datasource.save(auth_dto=auth_dto)
