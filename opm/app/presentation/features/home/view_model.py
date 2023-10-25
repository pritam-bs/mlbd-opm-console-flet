
from dataclasses import dataclass

from ....domain.error.app_error import AppException
from ....dependency_containers.application_container import application_container_provider
from ....core.abstractions import State
from ....domain.entities.booking_entity import BookingEntity
from ....domain.entities.model_update_entity import ModelUpdateEntity
from ....domain.entities.booking_update_entity import BookingUpdateListEntity
from ....domain.entities.meal_entity_type import MealEntityType

from typing import Dict, NamedTuple, Optional, List, Callable
from loguru import logger
from ....core.state_driver import StateDriver
import asyncio
from ....settings.settings import settings
from enum import Enum


class BookingForEmployee(NamedTuple):
    booking: Optional[BookingEntity]
    employee_id: Optional[str]


class MealConsumeRequestStatus(NamedTuple):
    meal: Optional[MealEntityType]
    is_success: Optional[bool]


class RequestType(Enum):
    meal_consume_request = "meal_consume_request",
    booking_request = "booking_request"


@dataclass(frozen=True)
class HomeState(State):
    is_meal_consume_request_in_progress: Optional[bool]
    meal_consume_request_error: Optional[str]
    is_booking_list_request_in_progress: Optional[bool]
    booking_list_request_error: Optional[str]
    booking_list: Optional[List[BookingEntity]]
    image: Optional[str]
    booking_for_employee: Optional[BookingForEmployee]
    meal_consume_request_status: Optional[MealConsumeRequestStatus]

    @classmethod
    def initial_state(cls) -> 'HomeState':
        return cls(
            is_meal_consume_request_in_progress=None,
            meal_consume_request_error=None,
            is_booking_list_request_in_progress=None,
            booking_list_request_error=None,
            booking_list=None,
            image=None,
            booking_for_employee=None,
            meal_consume_request_status=None
        )

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

    def mutate(
        self,
        is_meal_consume_request_in_progress=None,
        meal_consume_request_error=None,
        is_booking_list_request_in_progress=None,
        booking_list_request_error=None,
        booking_list=None,
        image=None,
        booking_for_employee=None,
        meal_consume_request_status=None
    ):
        mutated_state = HomeState(
            is_meal_consume_request_in_progress=is_meal_consume_request_in_progress if is_meal_consume_request_in_progress is not None else self.is_meal_consume_request_in_progress,
            meal_consume_request_error=meal_consume_request_error if meal_consume_request_error is not None else self.meal_consume_request_error,
            is_booking_list_request_in_progress=is_booking_list_request_in_progress if is_booking_list_request_in_progress is not None else self.is_booking_list_request_in_progress,
            booking_list_request_error=booking_list_request_error if booking_list_request_error is not None else self.booking_list_request_error,
            booking_list=booking_list if booking_list is not None else self.booking_list,
            image=image if image is not None else self.image,
            booking_for_employee=booking_for_employee if booking_for_employee is not None else self.booking_for_employee,
            meal_consume_request_status=meal_consume_request_status if meal_consume_request_status is not None else self.meal_consume_request_status,
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
        self.booking_cache_usecase = application_container.domain.container.booking_cache_usecase()
        self.booking_update_scheduler_usecase = application_container.domain.container.booking_update_scheduler_usecase()
        self.consume_meal_usecase = application_container.domain.container.consume_meal_usecase()
        self.employee_onboard_notify_usecase = application_container.domain.container.employee_onboard_notify_usecase()
        self._action_timeout_task = None

    def __del__(self):
        self.stop_face_recognition()
        self.stop_synchronizers()

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
                booking_list=booking_list, is_booking_list_request_in_progress=False, booking_list_request_error="")
            return new_state
        except AppException as app_exception:
            error = app_exception.error
            status = error.status_code
            if error.content:
                message = error.content.get("message", None)
                code = error.content.get("code", None)
                data = error.content.get("data", None)
            new_state = self.current_state.mutate(booking_list=[],
                                                  booking_list_request_error=message, is_booking_list_request_in_progress=False)
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

    async def _on_match(self, employee_id: str):
        if self.current_state.booking_for_employee is not None and self.current_state.booking_for_employee.employee_id == employee_id:
            return

        booking = self._find_bookings(employee_id=employee_id)
        booking_for_employee = BookingForEmployee(
            booking=booking, employee_id=employee_id)
        meal_consume_request_status = MealConsumeRequestStatus(
            meal=None, is_success=None)
        state = self.current_state.mutate(
            booking_for_employee=booking_for_employee, meal_consume_request_status=meal_consume_request_status)
        if self._state_callback:
            await self._state_callback(state)
            await self._start_meal_consume_action_timeout(
                timeout=settings.meal_select_action_timeout)

    async def _start_meal_consume_action_timeout(self, timeout):
        async def delayed_execution(timeout):
            try:
                await asyncio.sleep(timeout)
                booking_for_employee = BookingForEmployee(
                    booking=None, employee_id=None)
                meal_consume_request_status = MealConsumeRequestStatus(
                    meal=None, is_success=None)
                state = self.current_state.mutate(
                    booking_for_employee=booking_for_employee, meal_consume_request_status=meal_consume_request_status)
                if self._state_callback:
                    await self._state_callback(state)
            except asyncio.CancelledError:
                logger.debug("The delayed_execution was cancelled!")

        if self._action_timeout_task is not None:
            self._action_timeout_task.cancel()
        self._action_timeout_task = asyncio.create_task(
            delayed_execution(timeout=timeout))

    def _find_bookings(self, employee_id: str) -> Optional[BookingEntity]:
        booking_map = self.booking_cache_usecase.get_cached_booking()
        try:
            booking = booking_map[employee_id]
        except KeyError:
            logger.debug(
                f"No bookin for employee_id {employee_id} found in the list.")
            booking = None

        return booking

    async def _start_model_synchronizer(self):
        await self.model_synchronizer_usecase.start(
            on_model_update=self._on_model_update)

    def _stop_model_synchronizer(self):
        self.model_synchronizer_usecase.stop()

    def _on_model_update(self, model_update_entity: ModelUpdateEntity):
        self.onboarded_employee_list = model_update_entity.new_employee_list
        self._model_downloader_task = asyncio.create_task(
            self._download_model())

    async def _start_booking_synchronizer(self):
        await self.booking_synchronizer_usecase.start(
            on_booking_update=self._on_booking_update)

    def _stop_booking_synchronizer(self):
        self.booking_synchronizer_usecase.stop()

    async def _on_booking_update(self, booking_update_list_entity: BookingUpdateListEntity):
        booking_update_list = booking_update_list_entity.booking_update_list
        logger.debug(
            f"Newly booking update count: {len(booking_update_list)}")
        current_booking = self.booking_cache_usecase.get_cached_booking()
        logger.debug(f"Current booking count: {len(current_booking)}")
        self.booking_cache_usecase.update_cached_booking(
            booking_updates=booking_update_list_entity)
        updated_booking = self.booking_cache_usecase.get_cached_booking()
        logger.debug(f"Updated booking count: {len(updated_booking)}")

        booking_list = list(updated_booking.values())
        state = self.current_state.mutate(booking_list=booking_list)
        if self._state_callback:
            await self._state_callback(state)

    def start_synchronizers(self):
        self._booking_synchronizer_task = asyncio.create_task(
            self._start_booking_synchronizer())
        self._model_synchronizer_task = asyncio.create_task(
            self._start_model_synchronizer())

    def stop_synchronizers(self):
        if self._booking_synchronizer_task is not None:
            self._stop_booking_synchronizer()
            self._booking_synchronizer_task.cancel()
            self._booking_synchronizer_task = None
        if self._model_synchronizer_task is not None:
            self._stop_model_synchronizer()
            self._model_synchronizer_task.cancel()
            self._model_synchronizer_task = None
        if self._model_downloader_task is not None:
            self._model_downloader_task.cancel()
            self._model_downloader_task = None

    def start_booking_update_scheduler(self):
        self.booking_update_scheduler_usecase.start(
            on_scheduled_booking_update=self.on_scheduled_booking_update)

    def stop_booking_update_scheduler(self):
        self.booking_update_scheduler_usecase.stop()

    async def on_scheduled_booking_update(self, booking_list: List[BookingEntity]):
        state = self.current_state.mutate(booking_list=booking_list)
        if self._state_callback:
            await self._state_callback(state)

    async def _download_model(self):
        await self.model_downloader_usecase.download(
            callback=self._on_model_download)

    def _on_model_download(self, is_successful: bool):
        if is_successful:
            self.face_recognition_usecase.reload_model()
            self.notify_onboarding_successful()

    def notify_onboarding_successful(self):
        employee_list = self.onboarded_employee_list

    async def consume_breakfast(self):
        employee_id = self.current_state.booking_for_employee.employee_id
        try:
            is_success = await self.consume_meal_usecase.run(employee_id=employee_id, meals=[MealEntityType.BREAKFAST])
            meal_consume_request_status = MealConsumeRequestStatus(
                meal=MealEntityType.BREAKFAST, is_success=is_success)
            booking_for_employee = BookingForEmployee(
                booking=None, employee_id=None)
            new_state = self.current_state.mutate(booking_for_employee=booking_for_employee,
                                                  meal_consume_request_status=meal_consume_request_status, is_meal_consume_request_in_progress=False)
            return new_state
        except AppException as app_exception:
            error = app_exception.error
            status = error.status_code
            if error.content:
                message = error.content.get("message", None)
                code = error.content.get("code", None)
                data = error.content.get("data", None)
            meal_consume_request_status = MealConsumeRequestStatus(
                meal=MealEntityType.BREAKFAST, is_success=False)
            booking_for_employee = BookingForEmployee(
                booking=None, employee_id=None)
            new_state = self.current_state.mutate(booking_for_employee=booking_for_employee,
                                                  meal_consume_request_error=message, is_meal_consume_request_in_progress=False, meal_consume_request_status=meal_consume_request_status)
            return new_state

    async def consume_lunch(self):
        employee_id = self.current_state.booking_for_employee.employee_id
        try:
            is_success = await self.consume_meal_usecase.run(employee_id=employee_id, meals=[MealEntityType.LUNCH])
            meal_consume_request_status = MealConsumeRequestStatus(
                meal=MealEntityType.LUNCH, is_success=is_success)
            booking_for_employee = BookingForEmployee(
                booking=None, employee_id=None)
            new_state = self.current_state.mutate(booking_for_employee=booking_for_employee,
                                                  meal_consume_request_status=meal_consume_request_status, is_meal_consume_request_in_progress=False)
            return new_state
        except AppException as app_exception:
            error = app_exception.error
            status = error.status_code
            if error.content:
                message = error.content.get("message", None)
                code = error.content.get("code", None)
                data = error.content.get("data", None)
            meal_consume_request_status = MealConsumeRequestStatus(
                meal=MealEntityType.LUNCH, is_success=False)
            booking_for_employee = BookingForEmployee(
                booking=None, employee_id=None)
            new_state = self.current_state.mutate(booking_for_employee=booking_for_employee,
                                                  meal_consume_request_error=message, is_meal_consume_request_in_progress=False, meal_consume_request_status=meal_consume_request_status)
            return new_state

    def change_loading_state(self, is_loading: bool, request: RequestType):
        if request is RequestType.booking_request:
            new_state = self.current_state.mutate(
                is_booking_list_request_in_progress=is_loading)
        elif request is RequestType.meal_consume_request:
            new_state = self.current_state.mutate(
                is_meal_consume_request_in_progress=is_loading)
        return new_state

    def clear_error(self, request: RequestType):
        if request is RequestType.booking_request:
            new_state = self.current_state.mutate(
                booking_list_request_error="")
        elif request is RequestType.meal_consume_request:
            new_state = self.current_state.mutate(
                meal_consume_request_error="")
        return new_state
