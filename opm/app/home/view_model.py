
from dataclasses import dataclass

from ..domain.error.app_error import AppException
from ..dependency_containers.application_container import application_container_provider
from ..core.abstractions import State
from ..domain.entities.booking_entity import BookingEntity
from ..domain.entities.model_change_entity import ModelChangeEntity
from ..domain.entities.booking_change_entity import BookingChangeEntity

from typing import Dict, Optional, List, Union, Callable
from loguru import logger
from ..core.state_driver import StateDriver
import asyncio


@dataclass(frozen=True)
class HomeState(State):
    is_loading: Optional[bool]
    error: Optional[str]
    booking_list: Optional[List[BookingEntity]]
    image: Optional[str]

    @classmethod
    def initial_state(cls) -> 'HomeState':
        return cls(is_loading=None, error=None, booking_list=None, image=None)

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

    def mutate(self, is_loading=None, error=None, booking_list=None, image=None):
        mutated_state = HomeState(
            is_loading=is_loading if is_loading is not None else self.is_loading,
            error=error if error is not None else self.error,
            booking_list=booking_list if booking_list is not None else self.booking_list,
            image=image if image is not None else self.image,
        )
        return mutated_state


StateCallbackFunc = Callable[[HomeState], None]


class HomeViewModel:
    def __init__(self):
        self._state_driver = StateDriver(HomeState)
        application_container = application_container_provider()
        logger.debug(f"application_container id: {id(application_container)}")
        self.get_booking_usecase = application_container.domain.container.booking_usecase()
        self.face_recognition_usecase = application_container.domain.container.face_recognition_usecase()
        self.booking_synchronizer_usecase = application_container.domain.container.booking_synchronizer_usecase()
        self.model_synchronizer_usecase = application_container.domain.container.model_sychronizer_usecase()
        self.model_downloader_usecase = application_container.domain.container.model_downloader_usecase()

    @property
    def current_state(self):
        return self.state_driver.value

    @property
    def state_driver(self):
        return self._state_driver

    def set_state_callback(self, callback: StateCallbackFunc):
        self._state_callback = callback

    async def get_booking(self):
        try:
            booking_list = await self.get_booking_usecase.run()
            new_state = self.current_state.mutate(
                is_loading=False, booking_list=booking_list)
            return new_state
        except AppException as app_exception:
            error = app_exception.error
            status = error.status_code
            if error.content:
                message = error.content.get("message", None)
                code = error.content.get("code", None)
                data = error.content.get("data", None)
            new_state = self.current_state.mutate(
                error=message, is_loading=False)
            return new_state

    def start_face_recognition(self):
        self.face_recognition_usecase.start(
            on_image_receive=self._on_image_received, on_match=self._on_match)

    def stop_face_recognition(self):
        self.face_recognition_usecase.stop()

    async def _on_image_received(self, image: str):
        state = self.current_state.mutate(image=image)
        if self._state_callback:
            await self._state_callback(state)

    async def _on_match(self, booking_or_employee_id: Union[BookingEntity, str]):
        # Check if booking_or_employee_id is of type BookingEntity
        if isinstance(booking_or_employee_id, BookingEntity):
            logger.debug("booking_or_employee_id is a BookingEntity instance")

        # Check if booking_or_employee_id is of type str
        elif isinstance(booking_or_employee_id, str):
            logger.debug("booking_or_employee_id is a string")

    async def _start_model_synchronizer(self):
        await self.model_synchronizer_usecase.start(
            on_model_change=self._on_model_change)

    def _stop_model_synchronizer(self):
        self.model_synchronizer_usecase.stop()

    def _on_model_change(self, model_change_entity: ModelChangeEntity):
        pass

    async def _start_booking_synchronizer(self):
        await self.booking_synchronizer_usecase.start(
            on_booking_change=self._on_booking_change)

    def _stop_booking_synchronizer(self):
        self.booking_synchronizer_usecase.stop()

    def _on_booking_change(self, booking_change_entity: BookingChangeEntity):
        pass

    def start_synchronizers(self):
        self._booking_synchronizer_task = asyncio.create_task(
            self._start_booking_synchronizer())
        self._model_synchronizer_task = asyncio.create_task(
            self._start_model_synchronizer())

    def stop_synchronizers(self):
        if self._booking_synchronizer_task is not None:
            self._stop_booking_synchronizer()
            self._booking_synchronizer_task = None
        if self._model_synchronizer_task is not None:
            self._stop_model_synchronizer()
            self._model_synchronizer_task = None

        self._stop_model_synchronizer()

    def _download_model(self):
        self.model_downloader_usecase.download(
            callback=self._on_model_download)

    def _on_model_download(self, model_name: str, is_successful: bool):
        pass

    def change_loading_state(self, is_loading: bool):
        new_state = self.current_state.mutate(is_loading=is_loading)
        return new_state

    def clear_error(self, state: HomeState):
        new_state = state.mutate(error="")
        return new_state
