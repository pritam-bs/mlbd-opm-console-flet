from typing import Type, TypeVar, Generic
from ..core.abstractions import State, BaseView
from loguru import logger
import asyncio
from typing import List, Callable, Optional

S = TypeVar('S', bound=State)


class StateDriver(Generic[S]):
    def __init__(self, state_type: Type[S]):
        self._state = state_type.initial_state()
        self._listeners: List[Callable[[Optional[S], S], None]] = []

    @property
    def value(self) -> S:
        return self._state

    async def accept(self, new_state: S):
        old_state, self._state = self._state, new_state
        for listener in self._listeners:
            await listener(old_state, new_state)

    def bind(self, view: BaseView):
        async def callback(old_state: Optional[S], new_state: S):
            await view.update_control(new_state, old_state)

        self._listeners.append(callback)
