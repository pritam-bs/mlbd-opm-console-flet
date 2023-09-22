import asyncio
from dataclasses import dataclass
from types import TracebackType
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generator,
    Optional,
    Type,
    Union,
)

from aiohttp import ClientResponse, ClientSession, hdrs
from aiohttp.typedefs import StrOrURL
from yarl import URL as YARL_URL
from loguru import logger
from ...data.api.retry_options import ExponentialRetry, RetryOptionsBase
from ..model.error.response_code import ResponseCode

# url itself or list of urls for changing between retries
_URL_TYPE = Union[StrOrURL, YARL_URL]
RequestFunc = Callable[..., Awaitable[ClientResponse]]


@dataclass
class RequestParams:
    method: str
    url: _URL_TYPE
    headers: Optional[Dict[str, Any]] = None
    trace_request_ctx: Optional[Dict[str, Any]] = None
    kwargs: Optional[Dict[str, Any]] = None


class _RequestContext:
    def __init__(
        self,
        request_func: RequestFunc,
        params: RequestParams,
        retry_options: RetryOptionsBase,
    ) -> None:

        self._request_func = request_func
        self._params = params
        self._retry_options = retry_options
        self._response: Optional[ClientResponse] = None

    async def _should_retry(self, current_attempt: int, response: ClientResponse) -> bool:
        if ResponseCode.is_successful(status_code=response.status):
            return False

        if current_attempt == self._retry_options.attempts:
            return False

        if response.status >= ResponseCode.INTERNAL_SERVER_ERROR.value and self._retry_options.retry_all_server_errors:
            return True

        if response.status in self._retry_options.statuses:
            assert self._retry_options.evaluate_response_callback is not None, "evaluate_response_callback is not set"
            return await self._retry_options.evaluate_response_callback(response)

    async def _do_request(self) -> ClientResponse:
        current_attempt = 0

        while True:
            logger.debug(
                f"Attempt {current_attempt+1} out of {self._retry_options.attempts}")

            current_attempt += 1
            try:
                response: ClientResponse = await self._request_func(
                    self._params.method,
                    self._params.url,
                    headers=self._params.headers,
                    trace_request_ctx={
                        'current_attempt': current_attempt,
                        **(self._params.trace_request_ctx or {}),
                    },
                    **(self._params.kwargs or {}),
                )

                debug_message = f"Retrying after response code: {response.status}"
                should_retry = await self._should_retry(current_attempt, response)

                if not should_retry:
                    self._response = response
                    return self._response
                else:
                    retry_wait = self._retry_options.get_delay(
                        attempt=current_attempt, response=response)

            except Exception as e:
                if current_attempt >= self._retry_options.attempts:
                    raise e

                is_exc_valid = any([isinstance(e, exc)
                                   for exc in self._retry_options.exceptions])
                if not is_exc_valid:
                    raise e

                debug_message = f"Retrying after exception: {repr(e)}"
                retry_wait = self._retry_options.get_delay(
                    attempt=current_attempt, response=None)

            logger.debug(debug_message)
            await asyncio.sleep(retry_wait)

    def __await__(self) -> Generator[Any, None, ClientResponse]:
        return self.__aenter__().__await__()

    async def __aenter__(self) -> ClientResponse:
        return await self._do_request()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self._response is not None:
            if not self._response.closed:
                self._response.close()


class RetryClient:
    def __init__(
        self,
        client_session: Optional[ClientSession] = None,
        retry_options: Optional[RetryOptionsBase] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if client_session is not None:
            client = client_session
            closed = None
        else:
            client = ClientSession(*args, **kwargs)
            closed = False

        self._client = client
        self._closed = closed
        self._retry_options: RetryOptionsBase = retry_options or ExponentialRetry()

    @property
    def retry_options(self) -> RetryOptionsBase:
        return self._retry_options

    def request(
        self,
        method: str,
        url: StrOrURL,
        retry_options: Optional[RetryOptionsBase] = None,
        **kwargs: Any,
    ) -> _RequestContext:
        if retry_options is None:
            retry_options = self._retry_options
        return self._make_request(
            method=method,
            url=url,
            retry_options=retry_options,
            **kwargs,
        )

    async def close(self) -> None:
        await self._client.close()
        self._closed = True

    def _make_request(
        self,
        method: str,
        url: _URL_TYPE,
        retry_options: Optional[RetryOptionsBase] = None,
        **kwargs: Any,
    ) -> _RequestContext:
        params = RequestParams(
            method=method,
            url=url,
            headers=kwargs.pop('headers', {}),
            trace_request_ctx=kwargs.pop('trace_request_ctx', None),
            kwargs=kwargs,
        )

        return _RequestContext(
            request_func=self._client.request,
            params=params,
            retry_options=retry_options,
        )

    async def __aenter__(self) -> 'RetryClient':
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    def __del__(self) -> None:
        if getattr(self, '_closed', None) is None:
            # in case object was not initialized (__init__ raised an exception)
            return

        if not self._closed:
            logger.warning("Aiohttp retry client was not closed")
