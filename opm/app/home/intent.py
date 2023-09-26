from typing import List

from ..core.abstractions import BaseView
from ..core.state_driver import StateDriver
from ..home.view_model import HomeState, HomeViewModel
from rx.disposable import Disposable


class HomeIntent:
    def __init__(self):
        self._state_driver = StateDriver(HomeState)
        self._view_model = HomeViewModel()
        self._disposables: List[Disposable] = []

    @property
    def current_state(self):
        return self._state_driver.value

    def bind(self, view: BaseView):
        disposable = self._state_driver.bind(view=view)
        self._disposables.append(disposable)

    async def get_bookings(self):
        self.show_loading()
        state = await self._view_model.get_booking(state=self.current_state)
        self._state_driver.accept(event=state)
        self.hide_loading()

    def show_loading(self):
        state = self._view_model.change_loading_state(
            state=self.current_state, is_loading=True)
        self._state_driver.accept(event=state)

    def hide_loading(self):
        state = self._view_model.change_loading_state(
            state=self.current_state, is_loading=False)
        self._state_driver.accept(event=state)

    def dispose_all(self):
        for disposable in self._disposables:
            disposable.dispose()
        self._disposables.clear()
