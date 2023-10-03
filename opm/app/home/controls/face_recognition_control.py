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
from typing import Optional
from ...core.res.dimens import DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH
from loguru import logger


class FaceRecognitionControl(UserControl):
    def __init__(
        self,
        intent: HomeIntent
    ):
        super().__init__()
        self.intent = intent
        self._booking = BookingEntity(name="Pritam Biswas", email="pritam.biswas@monstar-lab.com", employee_id="BD00054",
                                      is_emergency=True, booked_meals=[MealType.BREAKFAST, MealType.LUNCH], consumed_meals=[MealType.BREAKFAST])
        self._error_for_employe_id = None
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
        _title = Heading(title="Face Scanner", size=HEADLINE_3_SIZE)
        self.face_preview = Image(
            src=camera_img_path,
            width=300,
            height=300,
            border_radius=10,
            fit=ImageFit.COVER,
        )

        self._progress_container = Container(
            content=ProgressRing(
                width=30,
                height=30,
            ),
            alignment=alignment.top_center,
            padding=20,
            visible=False,
        )

        self.booking_info_container = Container(
            content=Stack(
                controls=[
                    Card(
                        content=self._get_booking_info(
                            booking=self._booking,
                            error_for_employee_id=self._error_for_employe_id
                        ),
                    ),
                    Card(
                        content=self._progress_container,
                        color=colors.with_opacity(
                            opacity=0.4, color=colors.ON_PRIMARY)
                    ),
                ],
            ),
            width=self.page_width / 2.0,
            height=self.page_width / 6.0,
        )

        self._face_recognition_container = Container(
            content=Column(
                controls=[
                    _title,
                    self.face_preview,
                    self.booking_info_container,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=colors.AMBER
        )

        return self._face_recognition_container

    def _get_booking_info(self, booking: Optional[BookingEntity], error_for_employee_id: Optional[str]):
        if error_for_employee_id:
            return self._get_booking_not_found_control(employee_id=error_for_employee_id)
        elif booking:
            return self._get_meal_info_control(booking=booking)
        else:
            return self._get_description_control()

    def _get_description_control(self):
        return Container(
            content=HeadingWithSubheading(
                "Welcome to office meal service!",
                "Please scan your face to access the meal options.",
            ),
            padding=20,
        )

    def _get_booking_not_found_control(self, employee_id: str):
        return Container(
            content=HeadingWithSubheading(
                f"Employee ID: {employee_id}",
                "We apologize for any inconvenience caused, but it appears that you have not booked a meal for today."
            ),
            padding=20,
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

        return Container(
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

    def _breakfast_button_on_click(self, e):
        pass

    def _lunch_button_on_click(self, e):
        pass

    async def update_control(self, state: HomeState, prev_state: Optional[HomeState]):
        if state.image:
            self.face_preview.src_base64 = state.image
        await self.update_async()

    async def on_window_resized_listener(self, width, height):
        self.page_width = width
        self.page_height = height
        if not self.is_mounted:
            return
        await self.update_async()
