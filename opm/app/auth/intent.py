from ..core.state_driver import StateDriver
from ..auth.view_model import SplashState
from ..core.abstractions import BaseView
from ..auth.view_model import SplashViewModel
from rx.disposable import Disposable
from typing import List


class SplashIntent:
    def __init__(self):
        self._state_driver = StateDriver(SplashState)
        self._view_model = SplashViewModel()
        self._disposables: List[Disposable] = []

    @property
    def current_state(self):
        return self._state_driver.value

    def bind(self, view: BaseView):
        disposable = self._state_driver.bind(view=view)
        self._disposables.append(disposable)

    def check_auth(self):
        state = self._view_model.check_authentication(
            prev_state=self.current_state)
        self._state_driver.accept(event=state)

    def change_user_id(self, user_id: str):
        state = self._view_model.validate_input(
            prev_state=self.current_state, client_name=user_id)
        self._state_driver.accept(event=state)

    def change_password(self, password: str):
        state = self._view_model.validate_input(
            prev_state=self.current_state, password=password)
        self._state_driver.accept(event=state)

    async def submit(self):
        self.clear_error()
        self.show_loading()
        state = await self._view_model.submit(state=self.current_state)
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

    def clear_error(self):
        state = self._view_model.clear_error(state=self.current_state)
        self._state_driver.accept(event=state)

    def dispose_all(self):
        for disposable in self._disposables:
            disposable.dispose()
        self._disposables.clear()
