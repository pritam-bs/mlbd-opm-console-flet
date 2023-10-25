from flet import (
    Row,
    Container,
    Column,
    colors,
    MainAxisAlignment,
    CrossAxisAlignment,
)
from typing import Optional

from loguru import logger

from opm.app.core.views import BodyText
from ....presentation.features.home.view_model import HomeState
from ....presentation.features.home.intent import HomeIntent
from ....core.abstractions import BaseView, ViewParams
from ....presentation.features.home.controls.booking_list_control import BookingListControl
from ....presentation.features.home.controls.face_recognition_control import FaceRecognitionControl
from ....core.res.dimens import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT


class HomeScreen(BaseView):
    def __init__(
        self,
        params: ViewParams,
    ):
        super().__init__(params=params)
        self.keep_back_stack = False  # User cannot go back from this screen
        self.intent = HomeIntent()
        self.page_height = DEFAULT_WINDOW_HEIGHT
        self.page_width = DEFAULT_WINDOW_WIDTH

    async def update_control(self, state: HomeState, prev_state: Optional[HomeState]):
        await self._face_recognition_control.update_control(
            state=state, prev_state=prev_state)
        await self._booking_list_control.update_control(
            state=state, prev_state=prev_state)
        await super().update_control(state, prev_state)

    async def did_mount_async(self):
        await super().did_mount_async()
        self.mounted = True
        self.intent.bind(view=self)
        self.intent.start_face_recognition()
        self.intent.start_synchronizer()
        self.intent.start_booking_update_scheduler()
        logger.info("Home view did mount")

    async def will_unmount_async(self):
        await super().will_unmount_async()
        self.mounted = False
        self.intent.stop_face_recognition()
        self.intent.stop_model_synchronizer()
        self.intent.stop_booking_update_scheduler()
        logger.debug("Home view did unmount")

    def build(self):
        logger.info("Building Home view")
        self._booking_list_control = BookingListControl(intent=self.intent)
        snack = self.show_snack
        self._face_recognition_control = FaceRecognitionControl(
            intent=self.intent, show_snack=self.show_snack)

        self._list_container = Container(
            content=self._booking_list_control,
            width=300,
            bgcolor=colors.BLUE,
        )

        self._face_recognition_container = Column(
            controls=[
                self._face_recognition_control
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            expand=True,
        )

        return Row(
            controls=[
                self._list_container,
                self._face_recognition_container,

            ],
            vertical_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
        )

    async def on_window_resized_listener(self, width, height):
        await super().on_window_resized_listener(width, height)
        if not self.mounted:
            return
        await self._booking_list_control.on_window_resized_listener(width=width, height=height)
        await self._face_recognition_control.on_window_resized_listener(width=width, height=height)
        await self.update_async()
