import abc
import random
from typing import Any, Awaitable, Callable, Iterable, List, Optional, Set, Type
from warnings import warn

from aiohttp import ClientResponse

EvaluateResponseCallbackType = Callable[[ClientResponse], Awaitable[bool]]


class RetryOptionsBase:
    def __init__(
        self,
        attempts: int = 3,  # How many times we should retry
        # On which statuses we should retry
        statuses: Optional[Iterable[int]] = None,
        # On which exceptions we should retry
        exceptions: Optional[Iterable[Type[Exception]]] = None,
        # If should retry all 500 errors or not
        retry_all_server_errors: bool = True,
        # a callback that will run on response to decide if retry
        evaluate_response_callback: Optional[EvaluateResponseCallbackType] = None,
    ):
        self.attempts: int = attempts
        if statuses is None:
            statuses = set()
        self.statuses: Iterable[int] = statuses

        if exceptions is None:
            exceptions = set()
        self.exceptions: Iterable[Type[Exception]] = exceptions

        self.retry_all_server_errors = retry_all_server_errors
        self.evaluate_response_callback = evaluate_response_callback

    @abc.abstractmethod
    def get_delay(self, attempt: int, response: Optional[ClientResponse] = None) -> float:
        raise NotImplementedError


class ExponentialRetry(RetryOptionsBase):
    def __init__(
        self,
        attempts: int = 3,  # How many times we should retry
        start_delay: float = 0.1,  # Base timeout time, then it exponentially grow
        max_delay: float = 30.0,  # Max possible timeout between tries
        factor: float = 2.0,  # How much we increase timeout each time
        # On which statuses we should retry
        statuses: Optional[Set[int]] = None,
        # On which exceptions we should retry
        exceptions: Optional[Set[Type[Exception]]] = None,
        retry_all_server_errors: bool = True,
        evaluate_response_callback: Optional[EvaluateResponseCallbackType] = None,
    ):
        super().__init__(
            attempts=attempts,
            statuses=statuses,
            exceptions=exceptions,
            retry_all_server_errors=retry_all_server_errors,
            evaluate_response_callback=evaluate_response_callback,
        )

        self._start_delay: float = start_delay
        self._max_delay: float = max_delay
        self._factor: float = factor

    def get_delay(self, attempt: int, response: Optional[ClientResponse] = None) -> float:
        """Return delay with exponential backoff."""
        timeout = self._start_delay * (self._factor ** attempt)
        return min(timeout, self._max_delay)


def RetryOptions(*args: Any, **kwargs: Any) -> ExponentialRetry:
    warn("RetryOptions is deprecated, use ExponentialRetry")
    return ExponentialRetry(*args, **kwargs)


class RandomRetry(RetryOptionsBase):
    def __init__(
        self,
        attempts: int = 3,  # How many times we should retry
        # On which statuses we should retry
        statuses: Optional[Iterable[int]] = None,
        # On which exceptions we should retry
        exceptions: Optional[Iterable[Type[Exception]]] = None,
        min_delay: float = 0.1,  # Minimum possible timeout
        max_delay: float = 3.0,  # Maximum possible timeout between tries
        # Random number generator
        random_func: Callable[[], float] = random.random,
        retry_all_server_errors: bool = True,
        evaluate_response_callback: Optional[EvaluateResponseCallbackType] = None,
    ):
        super().__init__(
            attempts=attempts,
            statuses=statuses,
            exceptions=exceptions,
            retry_all_server_errors=retry_all_server_errors,
            evaluate_response_callback=evaluate_response_callback,
        )

        self.attempts: int = attempts
        self.min_delay: float = min_delay
        self.max_delay: float = max_delay
        self.random = random_func

    def get_delay(self, attempt: int, response: Optional[ClientResponse] = None) -> float:
        """Generate random timeouts."""
        return self.min_delay + self.random() * (self.max_delay - self.min_delay)


class ListRetry(RetryOptionsBase):
    def __init__(
        self,
        delays: List[float],
        # On which statuses we should retry
        statuses: Optional[Iterable[int]] = None,
        # On which exceptions we should retry
        exceptions: Optional[Iterable[Type[Exception]]] = None,
        retry_all_server_errors: bool = True,
        evaluate_response_callback: Optional[EvaluateResponseCallbackType] = None,
    ):
        super().__init__(
            attempts=len(delays),
            statuses=statuses,
            exceptions=exceptions,
            retry_all_server_errors=retry_all_server_errors,
            evaluate_response_callback=evaluate_response_callback,
        )
        self.delays = delays

    def get_delay(self, attempt: int, response: Optional[ClientResponse] = None) -> float:
        """delays from a defined list."""
        return self.delays[attempt]


class FibonacciRetry(RetryOptionsBase):
    def __init__(
        self,
        attempts: int = 3,
        multiplier: float = 1.0,
        statuses: Optional[Iterable[int]] = None,
        exceptions: Optional[Iterable[Type[Exception]]] = None,
        max_delay: float = 3.0,  # Maximum possible timeout between tries
        retry_all_server_errors: bool = True,
        evaluate_response_callback: Optional[EvaluateResponseCallbackType] = None,
    ):
        super().__init__(
            attempts=attempts,
            statuses=statuses,
            exceptions=exceptions,
            retry_all_server_errors=retry_all_server_errors,
            evaluate_response_callback=evaluate_response_callback,
        )

        self.max_delay = max_delay
        self.multiplier = multiplier
        self.prev_step = 1.0
        self.current_step = 1.0

    def get_delay(self, attempt: int, response: Optional[ClientResponse] = None) -> float:
        new_current_step = self.prev_step + self.current_step
        self.prev_step = self.current_step
        self.current_step = new_current_step

        return min(self.multiplier * new_current_step, self.max_delay)


class JitterRetry(ExponentialRetry):
    """https://github.com/inyutin/aiohttp_retry/issues/44"""

    def __init__(
        self,
        attempts: int = 3,  # How many times we should retry
        start_delay: float = 0.1,  # Base timeout time, then it exponentially grow
        max_delay: float = 30.0,  # Max possible timeout between tries
        factor: float = 2.0,  # How much we increase timeout each time
        # On which statuses we should retry
        statuses: Optional[Set[int]] = None,
        # On which exceptions we should retry
        exceptions: Optional[Set[Type[Exception]]] = None,
        random_interval_size: float = 2.0,  # size of interval for random component
        retry_all_server_errors: bool = True,
        evaluate_response_callback: Optional[EvaluateResponseCallbackType] = None,
    ):
        super().__init__(
            attempts=attempts,
            start_delay=start_delay,
            max_delay=max_delay,
            factor=factor,
            statuses=statuses,
            exceptions=exceptions,
            retry_all_server_errors=retry_all_server_errors,
            evaluate_response_callback=evaluate_response_callback,
        )

        self._start_delay: float = start_delay
        self._max_delay: float = max_delay
        self._factor: float = factor
        self._random_interval_size = random_interval_size

    def get_delay(self, attempt: int, response: Optional[ClientResponse] = None) -> float:
        delay: float = super().get_delay(attempt) + random.uniform(0,
                                                                   self._random_interval_size) ** self._factor
        return delay
