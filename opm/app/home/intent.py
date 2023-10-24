from ..core.abstractions import BaseView
from ..home.view_model import HomeState, HomeViewModel


class HomeIntent:
    def __init__(self):
        self._view_model = HomeViewModel()
        self._view_model.set_state_callback(self._on_state_received)

    @property
    def current_state(self):
        return self._view_model.current_state

    def bind(self, view: BaseView):
        self._view_model.state_driver.bind(view=view)

    async def get_bookings(self):
        await self.show_loading()
        state = await self._view_model.get_booking()
        await self._view_model.state_driver.accept(new_state=state)
        await self.hide_loading()

    async def show_loading(self):
        state = self._view_model.change_loading_state(is_loading=True)
        await self._view_model.state_driver.accept(new_state=state)

    async def hide_loading(self):
        state = self._view_model.change_loading_state(is_loading=False)
        await self._view_model.state_driver.accept(new_state=state)

    def start_face_recognition(self):
        self._view_model.start_face_recognition()

    async def _on_state_received(self, state: HomeState):
        await self._view_model.state_driver.accept(new_state=state)

    def stop_face_recognition(self):
        self._view_model.stop_face_recognition()

    def start_synchronizer(self):
        self._view_model.start_synchronizers()

    def stop_model_synchronizer(self):
        self._view_model.stop_synchronizers()

    def start_booking_update_scheduler(self):
        self._view_model.start_booking_update_scheduler()

    def stop_booking_update_scheduler(self):
        self._view_model.stop_booking_update_scheduler()

    async def consume_breakfast(self):
        await self._view_model.consume_breakfast()

    async def consume_lunch(self):
        await self._view_model.consume_lunch()
