from abc import ABC, abstractmethod, abstractproperty, abstractstaticmethod
from dataclasses import dataclass
import functools
from typing import Callable, Optional, TypeVar
from loguru import logger
from flet import AlertDialog, UserControl
from .utils import AUTO_SCROLL, START_ALIGNMENT, AlertDialogControls
from pathlib import Path


class ClientStorage(ABC):
    """Abstract class for client storage"""

    def __init__(
        self,
    ):
        super().__init__()
        self.keys_prefix = "tuttle_app_"

    @abstractmethod
    async def set_value(self, key: str, value: any):
        """appends an identifier prefix to the key and stores the key-value pair
        value can be a string, number, boolean or list
        """
        pass

    @abstractmethod
    async def get_value(self, key: str) -> Optional[any]:
        """appends an identifier prefix to the key and gets the value if exists"""
        pass

    @abstractmethod
    async def remove_value(self, key: str):
        """appends an identifier prefix to the key and removes associated key-value pair if exists"""
        pass

    @abstractmethod
    async def clear_preferences(
        self,
    ):
        """Deletes all of preferences permanently"""
        pass


@dataclass
class ViewParams:
    """Parameters for Views"""

    navigate_to_route: Callable
    show_snack: Callable
    dialog_controller: Callable
    client_storage: ClientStorage
    vertical_alignment_in_parent: str = START_ALIGNMENT
    horizontal_alignment_in_parent: str = START_ALIGNMENT
    keep_back_stack: bool = True
    on_navigate_back: Optional[Callable] = None
    page_scroll_type: Optional[str] = AUTO_SCROLL


class State(ABC):
    @classmethod
    @abstractmethod
    def initial_state(cls) -> 'State':
        pass


S = TypeVar('S', bound=State)


class BaseView(ABC, UserControl):
    """Abstract class for all UI screens"""

    def __init__(self, params: ViewParams):
        super().__init__()
        self.navigate_to_route = params.navigate_to_route
        self.show_snack: Callable[[str, bool], None] = params.show_snack
        self.dialog_controller = params.dialog_controller
        self.vertical_alignment_in_parent = params.vertical_alignment_in_parent
        self.horizontal_alignment_in_parent = params.horizontal_alignment_in_parent
        self.keep_back_stack = params.keep_back_stack
        self.navigate_back = params.on_navigate_back
        self.page_scroll_type = params.page_scroll_type
        self.client_storage = params.client_storage
        self.mounted = False

    def parent_intent_listener(self, intent: str, data: any):
        """listens for an intent from parent view"""
        return

    def on_resume_after_back_pressed(
        self,
    ):
        """listener for when a view has been resumed after user pressed back from another view
        used by views whose self.keep_back_stack parameter is set to True
        """
        return

    async def on_window_resized_listener(self, width, height):
        """sets the page width and height"""
        self.page_width = width
        self.page_height = height

    async def update_control(
        self,
        state: S,
        prevState: Optional[S],
    ):
        """Triggers an update to the view only if the view is mounted"""
        try:
            if self.mounted:
                await self.update_async()
        except Exception as e:
            logger.error(
                f"A view update caused an exception to be thrown {e.__class__.__name__}"
            )
            logger.exception(e)


class DialogHandler(ABC):
    """Used by views to set, open, and dismiss dialogs"""

    def __init__(
        self,
        dialog: AlertDialog,
        dialog_controller: Callable[[any, AlertDialogControls], None],
    ):
        super().__init__()
        self.dialog_controller = dialog_controller
        self.dialog: AlertDialog = dialog

    def close_dialog(self, e: Optional[any] = None):
        self.dialog_controller(self.dialog, AlertDialogControls.CLOSE)

    def open_dialog(self, e: Optional[any] = None):
        self.dialog_controller(self.dialog, AlertDialogControls.ADD_AND_OPEN)

    def dimiss_open_dialogs(self):
        if self.dialog is not None and self.dialog.open:
            self.close_dialog()


class Intent(ABC):
    """Abstract base class for intent classes."""

    def __getattribute__(self, name):
        """Logs all calls to methods of this class""" ""
        attr = object.__getattribute__(self, name)
        if callable(attr):

            @functools.wraps(attr)
            def wrapped(*args, **kwargs):
                class_name = self.__class__.__name__
                # Mask password argument if exists
                kwargs = {
                    k: "******" if k == "password" else v for k, v in kwargs.items()
                }
                logger.debug(
                    f"Intent: {class_name}:{name} called with: {kwargs}")
                return attr(*args, **kwargs)

            return wrapped
        return attr
