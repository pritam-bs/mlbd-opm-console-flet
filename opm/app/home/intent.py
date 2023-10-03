from typing import List

from ..core.abstractions import BaseView
from ..home.view_model import HomeState, HomeViewModel
from rx.disposable import Disposable


class HomeIntent:
    def __init__(self):
        self._view_model = HomeViewModel()
        self._view_model.set_state_callback(self._on_state_received)
        self._disposables: List[Disposable] = []

    @property
    def current_state(self):
        return self._view_model.current_state

    def bind(self, view: BaseView):
        disposable = self._view_model.state_driver.bind(view=view)
        self._disposables.append(disposable)

    async def get_bookings(self):
        self.show_loading()
        state = await self._view_model.get_booking()
        self._view_model.state_driver.accept(event=state)
        self.hide_loading()

    def show_loading(self):
        state = self._view_model.change_loading_state(is_loading=True)
        self._view_model.state_driver.accept(event=state)

    def hide_loading(self):
        state = self._view_model.change_loading_state(is_loading=False)
        self._view_model.state_driver.accept(event=state)

    def start_face_recognition(self):
        self._view_model.start_face_recognition()

    def _on_state_received(self, state: HomeState):
        self._view_model.state_driver.accept(event=state)

    def stop_face_recognition(self):
        self._view_model.stop_face_recognition()

    def dispose_all(self):
        for disposable in self._disposables:
            disposable.dispose()
        self._disposables.clear()
