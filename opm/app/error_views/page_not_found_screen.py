from typing import Callable

from flet import Column, Container, UserControl, padding

from ..core.abstractions import BaseView, ViewParams
from ..core.utils import CENTER_ALIGNMENT
from ..core.views import ErrorText, PrimaryButton
from ..core.res.dimens import SPACE_MD, SPACE_STD


class ErrorScreen(BaseView, UserControl):
    def __init__(self, params: ViewParams):
        super().__init__(params)
        self.vertical_alignment_in_parent = CENTER_ALIGNMENT
        self.horizontal_alignment_in_parent = CENTER_ALIGNMENT

    def build(self):
        view = Container(
            Column(
                expand=True,
                spacing=SPACE_STD,
                run_spacing=SPACE_STD,
                controls=[
                    ErrorText("OOps! Looks like you took a wrong turn"),
                    PrimaryButton(
                        label="Go Back".upper(), on_click=self.navigate_back
                    ),
                ],
            ),
            padding=padding.all(SPACE_MD),
        )

        return view
