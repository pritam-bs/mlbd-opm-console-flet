from flet import View
from typing import Callable
from dataclasses import dataclass

@dataclass
class RouteView:
    """A utility class that defines a route view"""

    view: View
    keep_back_stack: bool
    on_window_resized: Callable