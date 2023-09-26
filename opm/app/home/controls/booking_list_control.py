from flet import (
    Row,
    Card,
    UserControl,
    Container,
    Column,
    Text,
    colors,
    TextThemeStyle,
    border,
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
from rx.subject import Subject
from rx.operators import distinct_until_changed
from enum import Enum

from ...home.intent import HomeIntent
from ...home.controls.booking_list_item_control import BookingListItemControl
from ...core.views import SecondaryButton, BodyText
from ...domain.entities.booking_entity import BookingEntity, MealType
from ...home.view_model import HomeState
from ...core.res.dimens import DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH


class ScrollBehavior(Enum):
    PULL_TO_REFRESH = 1
    PAGINATION = 2
    SCROLL = 3


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

    @property
    def total_booked_breakfast(self) -> int:
        total_booked_breakfast_count = len(
            [booking for booking in self._booking_list if booking.booked_meals and MealType.BREAKFAST in booking.booked_meals])
        return total_booked_breakfast_count

    @property
    def total_booked_lunch(self) -> int:
        total_booked_lunch_count = len(
            [booking for booking in self._booking_list if booking.booked_meals and MealType.LUNCH in booking.booked_meals])
        return total_booked_lunch_count

    @property
    def total_emergency_count(self) -> int:
        total_emergency_count = sum(
            booking.is_emergency for booking in self._booking_list)
        return total_emergency_count

    async def did_mount_async(self):
        await super().did_mount_async()
        self.is_mounted = True
        self._config_scroll_behavior()
        await self.intent.get_bookings()

    async def will_unmount_async(self):
        await super().will_unmount_async()
        self.is_mounted = False
        self.subscription.dispose()

    def build(self):
        self.summary_card = Card(
            Container(
                content=Column(
                    controls=[
                        BodyText(
                            text=f"Breakfast: {self.total_booked_breakfast}"),
                        BodyText(text=f"Lunch: {self.total_booked_lunch}"),
                        BodyText(
                            text=f"Emergency: {self.total_emergency_count}")

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
            bgcolor=colors.with_opacity(
                opacity=0.4, color=colors.ON_PRIMARY),
        )

        self._booking_list_container = Container(
            content=Stack(
                controls=[
                    self.list_view,
                    self._refresh_container,
                    self._progress_container,
                ],
            ),
            bgcolor=colors.RED,
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

    def _on_scroll(self, event: OnScrollEvent):
        pixels = event.pixels
        max_scroll_extent = event.max_scroll_extent
        min_scroll_extent = event.min_scroll_extent

        if (min_scroll_extent - pixels) > 100:
            self.scroll_behavior_subject.on_next(
                ScrollBehavior.PULL_TO_REFRESH)
        elif (pixels - max_scroll_extent) > 100:
            self.scroll_behavior_subject.on_next(ScrollBehavior.PAGINATION)
        else:
            self.scroll_behavior_subject.on_next(ScrollBehavior.SCROLL)

    def _config_scroll_behavior(self):
        def on_next(scroll_behavior):
            logger.debug(scroll_behavior)
            if scroll_behavior == ScrollBehavior.PULL_TO_REFRESH:
                self.intent.get_bookings()

        def on_error(error):
            logger.debug(error)

        def on_completed():
            logger.debug("on_completed")

        self.scroll_behavior_subject = Subject()
        self.subscription = self.scroll_behavior_subject.pipe(
            distinct_until_changed()).subscribe(
            on_next=on_next, on_error=on_error, on_completed=on_completed)

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

    async def update_control(self, state: HomeState, prev_state: HomeState):
        if self.is_mounted == False:
            return

        compared_state = HomeState.compare(prev_state, state)
        if compared_state.is_loading is not None:
            logger.debug(f"_update_progress_view: {compared_state.is_loading}")
            self._update_progress_view(
                is_in_progress=compared_state.is_loading)
        if compared_state.booking_list is not None or compared_state.error is not None:
            self._booking_list = compared_state.booking_list if compared_state.booking_list is not None else []
            self._update_booking_list()
            self._update_refresh_view()

        await self.update_async()

    async def on_window_resized_listener(self, width, height):
        self.page_height = height
        self.page_width = width
        if not self.is_mounted:
            return
        self.list_view.height = self.page_height - self.summary_card.height
        await self.update_async()
