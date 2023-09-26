
from dataclasses import dataclass

from ..domain.error.app_error import AppException
from ..dependency_containers.application_container import ApplicationContainer
from ..core.abstractions import State
from ..domain.entities.booking_entity import BookingEntity

from typing import Optional, List


@dataclass(frozen=True)
class HomeState(State):
    is_loading: Optional[bool]
    error: Optional[str]
    booking_list: Optional[List[BookingEntity]]

    @classmethod
    def initial_state(cls) -> 'HomeState':
        return cls(is_loading=None, error=None, booking_list=None)

    @classmethod
    def compare(cls, obj1, obj2):
        """Compare two SplashState objects and return a new SplashState object with the differences."""
        kwargs = {}
        for field in cls.__dataclass_fields__:
            if getattr(obj1, field) != getattr(obj2, field):
                kwargs[field] = getattr(obj2, field)
            else:
                kwargs[field] = None
        return cls(**kwargs)

    def mutate(self, is_loading=None, error=None, booking_list=None):
        mutated_state = HomeState(
            is_loading=is_loading if is_loading is not None else self.is_loading,
            error=error if error is not None else self.error,
            booking_list=booking_list if booking_list is not None else self.booking_list,
        )
        return mutated_state


class HomeViewModel:
    def __init__(self):
        container = ApplicationContainer()
        self.get_booking_usecase = container.domain.container.booking_usecase()

    async def get_booking(self, state: HomeState):
        try:
            booking_list = await self.get_booking_usecase.run()
            new_state = state.mutate(
                is_loading=False, booking_list=booking_list)
            return new_state
        except AppException as app_exception:
            error = app_exception.error
            status = error.status_code
            if error.content:
                message = error.content.get("message", None)
                code = error.content.get("code", None)
                data = error.content.get("data", None)
            new_state = state.mutate(error=message, is_loading=False)
            return new_state

    def change_loading_state(self, state: HomeState, is_loading: bool):
        new_state = state.mutate(is_loading=is_loading)
        return new_state

    def clear_error(self, state: HomeState):
        new_state = state.mutate(error="")
        return new_state
