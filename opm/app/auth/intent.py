from ..core.state_driver import StateDriver
from ..auth.view_model import SplashState
from ..core.abstractions import BaseView
from ..auth.view_model import SplashViewModel
from rx.disposable import Disposable
from typing import List


class SplashIntent:
    def __init__(self):
        self._view_model = SplashViewModel()

    @property
    def current_state(self):
        return self._view_model.current_state

    def bind(self, view: BaseView):
        self._view_model.state_driver.bind(view=view)

    async def check_auth(self):
        state = self._view_model.check_authentication()
        await self._view_model.state_driver.accept(new_state=state)

    async def change_user_id(self, user_id: str):
        state = self._view_model.validate_input(
            prev_state=self.current_state, client_name=user_id)
        await self._view_model.state_driver.accept(new_state=state)

    async def change_password(self, password: str):
        state = self._view_model.validate_input(
            prev_state=self.current_state, password=password)
        await self._view_model.state_driver.accept(new_state=state)

    async def submit(self):
        self.clear_error()
        self.show_loading()
        state = await self._view_model.submit(state=self.current_state)
        await self._view_model.state_driver.accept(new_state=state)
        self.hide_loading()

    async def show_loading(self):
        state = self._view_model.change_loading_state(
            state=self.current_state, is_loading=True)
        await self._view_model.state_driver.accept(new_state=state)

    async def hide_loading(self):
        state = self._view_model.change_loading_state(
            state=self.current_state, is_loading=False)
        await self._view_model.state_driver.accept(new_state=state)

    async def clear_error(self):
        state = self._view_model.clear_error(state=self.current_state)
        await self._view_model.state_driver.accept(new_state=state)
