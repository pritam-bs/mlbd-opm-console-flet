from opm.app.core.res import fonts, image_paths
from ..auth.view_model import SplashState
from ..core.abstractions import BaseView, ViewParams
from typing import Callable, Optional
from ..routes.route import HOME_SCREEN
from ..core import views
from ..core import utils
from ..core.res import dimens
from ..core.intent_result import IntentResult
from ..auth.intent import SplashIntent
from loguru import logger

from flet import (
    Column,
    Container,
    ResponsiveRow,
    UserControl,
    padding,
    ControlEvent,
)


class AuthDataForm(UserControl):
    """Form view for setting the user info"""

    def __init__(
        self,
        intent: SplashIntent
    ):
        super().__init__()
        self.is_mounted = False
        self.intent = intent

    async def did_mount_async(self):
        self.is_mounted = True
        await super().did_mount_async()

    async def will_unmount_async(self):
        self.is_mounted = False
        await super().will_unmount_async()

    def toggle_form_error_view(self, error: Optional[str] = None):
        """hides or displays the form error

        *a form error is not tied to a single specific field
        """
        self.form_err_control.value = error
        self.form_err_control.visible = error is not None or error != ""

    def on_change_user_id_field(self, event: ControlEvent):
        self.intent.change_user_id(user_id=event.data)

    def on_change_password_field(self, event: ControlEvent):
        self.intent.change_password(password=event.data)

    async def on_submit_btn_clicked(self, e):
        await self.intent.submit()

    async def update_control(self, state: SplashState, prev_state: SplashState):
        if self.is_mounted == False:
            return

        compared_state = SplashState.compare(prev_state, state)
        self.submit_btn.disabled = not state.can_submit or compared_state.is_loading
        self.toggle_form_error_view(error=state.error)

        await self.update_async()

    def build(self):
        """Called when form is built"""
        self.user_id_field = views.SinglelineTextField(
            label="User ID",
            hint="User ID",
            on_change=self.on_change_user_id_field,
            keyboard_type=utils.KEYBOARD_NAME,
        )
        self.password_field = views.SinglelineTextField(
            label="Password",
            hint="Password",
            on_change=self.on_change_password_field,
            keyboard_type=utils.KEYBOARD_PASSWORD,
        )
        self.form_err_control = views.ErrorText("")
        self.submit_btn = views.SecondaryButton(
            on_click=self.on_submit_btn_clicked,
            label="Submit",
            width=200,
            disabled=True,
        )
        return Column(
            spacing=dimens.SPACE_MD,
            controls=[
                self.user_id_field,
                self.password_field,
                self.form_err_control,
                self.submit_btn,
            ],
        )


class SplashScreen(BaseView):
    """Displayed the first time the app loads

    Checks if auth has been successful
    If successful, redirects user to the homepage
    If not successful, displays an auth form
    """

    def __init__(
        self,
        params: ViewParams,
    ):
        super().__init__(params=params)
        self.keep_back_stack = False  # User cannot go back from this screen
        self.intent = SplashIntent()
        self.client_storage = params.client_storage

    async def update_control(self, state: SplashState, prev_state: Optional[SplashState]):
        compared_state = SplashState.compare(prev_state, state)
        if compared_state.is_authenticated == False:
            await self.client_storage.clear_preferences()
            self.set_login_form()
        elif compared_state.is_authenticated == True:
            # self.navigate_to_route(HOME_SCREEN)
            logger.debug("navigate_to_route(HOME_SCREEN)")

        if compared_state.is_loading == True:
            logger.debug("loading True")
        elif compared_state.is_loading == False:
            logger.debug("loading False")
        if compared_state.error:
            logger.debug(f"Error: {state.error}")

        if hasattr(self, 'login_form'):
            await self.login_form.update_control(state=state, prev_state=prev_state)

        await super().update_control(state, prev_state)

    def set_login_form(self):
        logger.info("Setting up login form")
        self.login_form = AuthDataForm(intent=self.intent)
        self.form_container.controls.remove(self.loading_indicator)
        self.form_container.controls.append(self.login_form)

    async def did_mount_async(self):
        logger.info("Splash view did mount")
        self.mounted = True
        self.intent.bind(view=self)
        self.intent.check_auth()
        await super().did_mount_async()

    def build(self):
        logger.info("Building Splash view")
        self.loading_indicator = views.ProgressBar()
        self.form_container = Column(
            controls=[
                # views.TAppLogoWithLabel(),
                views.HeadingWithSubheading(
                    "Welcome to Op-M",
                    "Let's get you started: Please enter your user id and password below.",
                ),
                self.loading_indicator,
                views.Spacer(),
            ]
        )
        page_view = ResponsiveRow(
            spacing=0,
            run_spacing=0,
            alignment=utils.CENTER_ALIGNMENT,
            vertical_alignment=utils.CENTER_ALIGNMENT,
            controls=[
                Container(
                    col={"xs": 12, "sm": 5},
                    padding=padding.all(dimens.SPACE_XS),
                    content=Column(
                        alignment=utils.START_ALIGNMENT,
                        horizontal_alignment=utils.CENTER_ALIGNMENT,
                        expand=True,
                        controls=[
                            views.Spacer(md_space=True),
                            views.ImageView(
                                image_paths.splashImgPath,
                                "welcome screen image",
                                width=300,
                            ),
                            views.HeadingWithSubheading(
                                "Op-M",
                                "Food booking management system for Monstars",
                                alignment_in_container=utils.CENTER_ALIGNMENT,
                                txt_alignment=utils.TXT_ALIGN_CENTER,
                                title_size=fonts.HEADLINE_3_SIZE,
                                subtitle_size=fonts.HEADLINE_4_SIZE,
                            ),
                        ],
                    ),
                ),
                Container(
                    col={"xs": 12, "sm": 7},
                    padding=padding.all(dimens.SPACE_XL),
                    content=Column(
                        [
                            self.form_container,
                        ]
                    ),
                ),
            ],
        )
        return page_view

    async def will_unmount_async(self):
        logger.debug("Splash view did unmount")
        self.mounted = False
        await super().will_unmount_async()
