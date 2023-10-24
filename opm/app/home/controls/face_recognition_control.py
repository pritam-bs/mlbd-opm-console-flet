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
    ListView,
    Image,
    icons,
    ImageFit,
    ElevatedButton,
    ProgressRing,
)

from ...core.res.fonts import HEADLINE_3_SIZE
from ...home.intent import HomeIntent
from ...home.view_model import HomeState
from ...core.views import Heading, HeadingWithSubheading, FilledButton
from ...core.res.image_paths import camera_img_path
from ...domain.entities.booking_entity import BookingEntity, MealType
from typing import Optional, Tuple
from ...core.res.dimens import DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH
from loguru import logger
from collections import namedtuple

BookingForEmployee = namedtuple(
    'BookingForEmployee', ['booking', 'employee_id'])


class FaceRecognitionControl(UserControl):
    def __init__(
        self,
        intent: HomeIntent
    ):
        super().__init__()
        self.intent = intent
        self.page_width = DEFAULT_WINDOW_WIDTH
        self.page_height = DEFAULT_WINDOW_HEIGHT
        self.is_mounted = False

    async def did_mount_async(self):
        await super().did_mount_async()
        self.is_mounted = True

    async def will_unmount_async(self):
        await super().will_unmount_async()
        self.is_mounted = False

    def build(self):
        self._title = Heading(title="Face Scanner", size=HEADLINE_3_SIZE)
        self._face_preview = Image(
            src=camera_img_path,
            width=300,
            height=300,
            border_radius=10,
            fit=ImageFit.COVER,
        )

        self._booking_info_container = Container(
            content=self._get_booking_info_container(
                booking_for_employee=None, is_in_progress=False),
        )

        _face_recognition_container = Container(
            content=Column(
                controls=[
                    self._title,
                    self._face_preview,
                    self._booking_info_container,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            width=480,
            bgcolor=colors.AMBER
        )

        return _face_recognition_container

    def _get_booking_info_container(self, booking_for_employee: Optional[BookingForEmployee], is_in_progress: bool):
        if booking_for_employee is None:
            info_card = self._get_description_control()
        elif booking_for_employee.booking is not None:
            info_card = self._get_meal_info_control(
                booking=booking_for_employee.booking)
        elif booking_for_employee.employee_id is not None:
            info_card = self._get_booking_not_found_control(
                employee_id=booking_for_employee.employee_id)
        else:
            info_card = self._get_description_control()

        progress_card = Card(
            content=Container(
                content=ProgressRing(
                    width=30,
                    height=30,
                ),
                alignment=alignment.top_center,
                padding=20,
                visible=is_in_progress,
            ),
            color=colors.with_opacity(
                opacity=0.4, color=colors.ON_PRIMARY)
        )

        return Container(
            content=Stack(
                controls=[
                    info_card,
                    progress_card,
                ],
            ),
            height=150,
        )

    def _get_description_control(self):
        return Card(
            content=Container(
                content=HeadingWithSubheading(
                    "Welcome to the office meal service!",
                    "Please face the camera for identity verification. Your meal options will be presented after successful verification. NOTE: Ensure clear visibility and avoid obstructions.",
                ),
                padding=20,
            )
        )

    def _get_booking_not_found_control(self, employee_id: str):
        return Card(
            content=Container(
                content=HeadingWithSubheading(
                    f"Employee ID: {employee_id}",
                    "We apologize for any inconvenience caused, but it appears that you have not booked a meal for today."
                ),
                padding=20,
            )
        )

    def _get_meal_info_control(self, booking: BookingEntity):
        is_breakfast_disabled = True
        is_lunch_disabled = True

        booked_meals = [] if booking.booked_meals is None else booking.booked_meals
        for booked_meal in booked_meals:
            if booked_meal == MealType.BREAKFAST:
                is_breakfast_disabled = booking.is_consumed(
                    meal=MealType.BREAKFAST)
            elif booked_meal == MealType.LUNCH:
                is_lunch_disabled = booking.is_consumed(
                    meal=MealType.LUNCH)

        return Card(
            content=Container(
                content=Column(
                    controls=[
                        HeadingWithSubheading(
                            f"Hello {booking.name}",
                            "What meal do you want to consume?",
                        ),
                        Row(
                            controls=[
                                FilledButton(
                                    text="Breakfast",
                                    width=150,
                                    height=40,
                                    disabled=is_breakfast_disabled,
                                    on_click=self._breakfast_button_on_click,
                                ),
                                FilledButton(
                                    text="Lunch",
                                    width=150,
                                    height=40,
                                    disabled=is_lunch_disabled,
                                    on_click=self._lunch_button_on_click,
                                ),
                            ],
                            alignment=MainAxisAlignment.START,
                            vertical_alignment=CrossAxisAlignment.CENTER,
                            expand=False,
                        )
                    ],
                    expand=False,
                    alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.START,
                ),
                padding=20,
            )
        )

    def _breakfast_button_on_click(self, e):
        self.intent.consume_breakfast()

    def _lunch_button_on_click(self, e):
        self.intent.consume_lunch()

    async def update_control(self, state: HomeState, prev_state: Optional[HomeState]):
        if self.is_mounted == False:
            return

        if state.image:
            self._face_preview.src_base64 = state.image

        compared_state = HomeState.compare(prev_state, state)
        if compared_state.booking_for_employee:
            self._booking_info_container.content = self._get_booking_info_container(
                booking_for_employee=compared_state.booking_for_employee, is_in_progress=False)
        await self.update_async()

    async def on_window_resized_listener(self, width, height):
        self.page_width = width
        self.page_height = height
        if not self.is_mounted:
            return
        await self.update_async()
