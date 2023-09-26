from typing import Callable, Optional
from flet import (
    AlertDialog,
    FilePicker,
    RouteChangeEvent,
    Page,
    SnackBar,
    TemplateRoute,
    View,
)
from loguru import logger
from opm.app.auth.view import SplashScreen
from opm.app.core.abstractions import BaseView, ViewParams
from opm.app.core.client_storage_impl import ClientStorageImpl
from opm.app.core.res.colors import BLACK_COLOR_ALT, ERROR_COLOR, PRIMARY_COLOR, WHITE_COLOR
from opm.app.core.res.dimens import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH

from opm.app.core.res.fonts import APP_FONTS, HEADLINE_4_SIZE
from opm.app.core.res.theme import APP_THEME, THEME_MODES, get_theme_mode_from_value
from opm.app.core.route_view import RouteView
from opm.app.core.utils import AlertDialogControls
from opm.app.core.views import Heading
from opm.app.error_views.page_not_found_screen import ErrorScreen
from opm.app.home.view import HomeScreen
from opm.app.routes.route import HOME_SCREEN, SPLASH_SCREEN


class OpmApp:
    """The main application class"""

    def __init__(
        self,
        page: Page,
    ):
        """ """
        self.page = page
        self.page.title = "Op-M Console"
        self.page.fonts = APP_FONTS
        self.page.theme = APP_THEME
        self.client_storage = ClientStorageImpl(page=self.page)
        theme = (THEME_MODES.dark.value)
        self.page.theme_mode = theme
        self.page.window_min_width = MIN_WINDOW_WIDTH
        self.page.window_min_height = MIN_WINDOW_HEIGHT
        self.page.window_width = MIN_WINDOW_WIDTH
        self.page.window_height = MIN_WINDOW_HEIGHT
        self.file_picker = FilePicker()
        self.page.overlay.append(self.file_picker)

        """holds the RouteView object associated with a route
        used in on route change"""
        self.route_to_route_view_cache = {}
        self.page.on_route_change = self.on_route_change
        self.page.on_view_pop = self.on_view_pop
        self.route_parser = OpmRoutes(self)
        self.current_route_view: Optional[RouteView] = None
        self.page.on_resize = self.page_resize

    async def page_resize(self, e):
        if self.current_route_view:
            await self.current_route_view.on_window_resized(
                self.page.width, self.page.height
            )

    def on_theme_mode_changed(self, selected_theme: str):
        """callback function used by views for changing app theme mode"""
        mode = get_theme_mode_from_value(selected_theme)
        self.page.theme_mode = mode.value
        self.page.update_async()

    def show_snack(
        self,
        message: str,
        is_error: bool = False,
        action_label: Optional[str] = None,
        action_callback: Optional[Callable] = None,
    ):
        """callback function used by views to display a snack bar message"""
        if self.page.snack_bar and self.page.snack_bar.open:
            self.page.snack_bar.open = False
            self.page.update_async()
        self.page.snack_bar = SnackBar(
            Heading(
                title=message,
                size=HEADLINE_4_SIZE,
                color=ERROR_COLOR if is_error else WHITE_COLOR,
            ),
            bgcolor=WHITE_COLOR if is_error else BLACK_COLOR_ALT,
            action=action_label,
            action_color=PRIMARY_COLOR,
            on_action=action_callback,
        )
        self.page.snack_bar.open = True
        self.page.update_async()

    def control_alert_dialog(
        self,
        dialog: Optional[AlertDialog] = None,
        control: AlertDialogControls = AlertDialogControls.CLOSE,
    ):
        """handles adding, opening and closing of page alert dialogs"""
        if control.value == AlertDialogControls.ADD_AND_OPEN.value:
            if self.page.dialog:
                # make sure no two dialogs attempt to open at once
                self.page.dialog.open = False
                self.page.update_async()
            if dialog:
                self.page.dialog = dialog
                dialog.open = True
                self.page.update_async()

        if control.value == AlertDialogControls.CLOSE.value:
            if self.page.dialog:
                dialog.open = False
                self.page.update_async()

    async def change_route(self, to_route: str, data: Optional[any] = None):
        """navigates to a new route"""
        newRoute = to_route if data is None else f"{to_route}/{data}"
        await self.page.go_async(newRoute)

    async def on_view_pop(self, view: Optional[View] = None):
        """invoked on back pressed"""
        if len(self.page.views) == 1:
            return
        self.page.views.pop()
        current_page_view: View = self.page.views[-1]
        self.page.go_async(current_page_view.route)
        if current_page_view.controls:
            try:
                # the controls should contain a BaseView as first control
                view: BaseView = current_page_view.controls[0]
                # notify view that it has been resumed
                view.on_resume_after_back_pressed()
            except Exception as e:
                logger.error(
                    f"Exception raised @OpmApp.on_view_pop {e.__class__.__name__}"
                )
                logger.exception(e)

    async def on_route_change(self, event: RouteChangeEvent):
        """auto invoked when the route changes

        parses the new destination route
        then appends the new page to page views
        """

        # if route is already in stack, get it's view
        # this happens when the user presses back
        view_for_route = None
        for view in self.page.views:
            if view.route == event.route:
                view_for_route = view
                break

        # get a new view if no view found in stack
        if not view_for_route:
            route_view_wrapper = self.route_parser.parse_route(
                page_route=event.route)
            if not route_view_wrapper.keep_back_stack:
                """clear previous views"""
                self.route_to_route_view_cache.clear()
                self.page.views.clear()
            view_for_route = route_view_wrapper.view
            self.route_to_route_view_cache[event.route] = route_view_wrapper
            self.page.views.append(view_for_route)

        self.current_route_view: RouteView = self.route_to_route_view_cache[event.route]
        await self.page.update_async()
        await self.current_route_view.on_window_resized(
            self.page.width, self.page.height
        )

    async def build(self):
        await self.page.go_async(self.page.route)

    def close(self):
        """Closes the application."""
        self.page.window_close_async()

    def reset_and_quit(self):
        """Resets the application and quits."""
        self.close()


class OpmRoutes:
    """Utility class for parsing of routes to destination views"""

    def __init__(self, app: OpmApp):
        # init callbacks for some views
        self.on_theme_changed = app.on_theme_mode_changed
        self.on_reset_and_quit = app.reset_and_quit
        # init common params for views
        self.view_params = ViewParams(
            navigate_to_route=app.change_route,
            show_snack=app.show_snack,
            dialog_controller=app.control_alert_dialog,
            on_navigate_back=app.on_view_pop,
            client_storage=app.client_storage,
        )

    def get_page_route_view(
        self,
        route_name: str,
        view: BaseView,
    ) -> RouteView:
        """Constructs the view with a given route"""
        view_container = View(
            padding=0,
            spacing=0,
            route=route_name,
            scroll=view.page_scroll_type,
            controls=[view],
            vertical_alignment=view.vertical_alignment_in_parent,
            horizontal_alignment=view.horizontal_alignment_in_parent,
        )

        return RouteView(
            view=view_container,
            on_window_resized=view.on_window_resized_listener,
            keep_back_stack=view.keep_back_stack,
        )

    def parse_route(self, page_route: str):
        """parses a given route path and returns it's view"""

        routePath = TemplateRoute(page_route)
        screen = None
        if routePath.match(SPLASH_SCREEN):
            screen = SplashScreen(
                params=self.view_params,
            )
        elif routePath.match(HOME_SCREEN):
            screen = HomeScreen(
                params=self.view_params,
            )
        else:
            screen = ErrorScreen(params=self.view_params)

        return self.get_page_route_view(routePath.route, view=screen)
