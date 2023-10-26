from flet import (
    Card,
    UserControl,
    Container,
    Column,
    colors,
    alignment,
    MainAxisAlignment,
    CrossAxisAlignment,
    Stack,
    ProgressRing,
    OnScrollEvent,
    ListView
)
from typing import List
from loguru import logger

from .....presentation.features.home.intent import HomeIntent
from .....presentation.features.home.controls.booking_list_item_control import BookingListItemControl
from .....core.views import SecondaryButton, BodyText
from .....domain.entities.booking_entity import BookingEntity, MealEntityType
from .....presentation.features.home.view_model import HomeState
from .....core.res.dimens import DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH


class BookingListControl(UserControl):

    def __init__(
        self,
        intent: HomeIntent
    ):
        super().__init__()
        self._booking_list: List[BookingEntity] = []
        self.intent = intent
        self.is_mounted = False
        self.page_height = DEFAULT_WINDOW_HEIGHT
        self.page_width = DEFAULT_WINDOW_WIDTH

    async def did_mount_async(self):
        await super().did_mount_async()
        self.is_mounted = True
        await self.intent.get_bookings()

    async def will_unmount_async(self):
        await super().will_unmount_async()
        self.is_mounted = False

    def build(self):
        self._total_breakfast_text = BodyText(
            text=f"Breakfast: {0}")
        self._total_lunch_text = BodyText(
            text=f"Lunch: {0}")
        self._total_emergench_text = BodyText(
            text=f"Emergency: {0}")
        self.summary_card = Card(
            Container(
                content=Column(
                    controls=[
                        self._total_breakfast_text,
                        self._total_lunch_text,
                        self._total_emergench_text
                    ],
                    alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.STRETCH,
                ),
                padding=10,
            ),
            margin=5,
            height=100,
        )

        self.list_view = ListView(
            on_scroll=self._on_scroll,
            height=self.page_height - self.summary_card.height,
            spacing=5,
            padding=10,
        )

        self._refresh_container = Container(
            SecondaryButton(
                on_click=self._on_refresh_button_pressed,
                label="Refresh",
                width=200,
                disabled=False,
            ),
            alignment=alignment.bottom_center,
            visible=False,
        )
        self._progress_container = Container(
            content=ProgressRing(
                width=30,
                height=30,
            ),
            visible=False,
            alignment=alignment.center,
        )

        self._booking_list_container = Container(
            content=Stack(
                controls=[
                    self.list_view,
                    self._refresh_container,
                    self._progress_container,
                ],
            ),
        )

        self._list_container = Column(
            controls=[
                self.summary_card,
                self._booking_list_container,
            ],
            spacing=0,
            alignment=MainAxisAlignment.END,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            expand=True,
        )

        return self._list_container

    scroll_delta_threshold = 10.0
    is_scroll_delta_exceeded = False
    scroll_direction = None

    async def _on_scroll(self, event: OnScrollEvent):

        if event.event_type == "start":
            self.is_scroll_delta_exceeded = False

        if event.event_type == "user":
            self.scroll_direction = event.direction

        if event.scroll_delta is not None and event.scroll_delta > self.scroll_delta_threshold:
            self.is_scroll_delta_exceeded = True

        if event.event_type == "end" and self.is_scroll_delta_exceeded:
            if self.scroll_direction == "forward":
                logger.debug("Pull To Refresh")
                await self.intent.get_bookings()
            elif self.scroll_direction == "reverse":
                logger.debug("Next Page")

    async def _on_refresh_button_pressed(self, e):
        await self.intent.get_bookings()

    def _update_booking_list(self):
        self.list_view.controls.clear()
        for booking in self._booking_list:
            self.list_view.controls.append(
                BookingListItemControl(booking_entity=booking)
            )

    def _update_progress_view(self, is_in_progress: bool):
        self._progress_container.visible = is_in_progress

    def _update_refresh_view(self):
        if len(self._booking_list) < 1:
            self._refresh_container.visible = True
        else:
            self._refresh_container.visible = False

    def _update_summery_card(self):
        total_booked_breakfast_count = len(
            [booking for booking in self._booking_list if booking.booked_meals and MealEntityType.BREAKFAST in booking.booked_meals])
        total_booked_lunch_count = len(
            [booking for booking in self._booking_list if booking.booked_meals and MealEntityType.LUNCH in booking.booked_meals])
        total_emergency_count = sum(
            booking.is_emergency for booking in self._booking_list)

        self._total_breakfast_text.value = f"Breakfast: {total_booked_breakfast_count}"
        self._total_lunch_text.value = f"Lunch: {total_booked_lunch_count}"
        self._total_emergench_text.value = f"Emergency: {total_emergency_count}"

    async def update_control(self, state: HomeState, prev_state: HomeState):
        if self.is_mounted == False:
            return

        compared_state = HomeState.compare(prev_state, state)
        if compared_state.is_booking_list_request_in_progress:
            self._update_progress_view(
                is_in_progress=True)
        else:
            self._update_progress_view(
                is_in_progress=False)
        if compared_state.booking_list is not None:
            self._booking_list = compared_state.booking_list if compared_state.booking_list is not None else []
            self._update_booking_list()
            self._update_refresh_view()
            self._update_summery_card()

        await self.update_async()

    async def on_window_resized_listener(self, width, height):
        self.page_height = height
        self.page_width = width
        if not self.is_mounted:
            return
        self.list_view.height = self.page_height - self.summary_card.height
        await self.update_async()
