from typing import Type, TypeVar, Generic
from ..core.abstractions import State, BaseView
from rx.subject import BehaviorSubject
from rx import operators as ops
from loguru import logger
import asyncio
from rx.scheduler.eventloop import AsyncIOScheduler


S = TypeVar('S', bound=State)


class StateDriver(Generic[S]):
    def __init__(self, state_type: Type[S]):
        self._relay = BehaviorSubject(state_type.initial_state())

    @property
    def value(self) -> S:
        return self._relay.value

    def accept(self, event: S):
        self._relay.on_next(event)

    def bind(self, view: BaseView):
        logger.debug("Binding view to state")

        async def update_callback(pair):
            await view.update_control(pair[1], pair[0])

        def subscription_callback(pair):
            asyncio.ensure_future(update_callback(pair))

        disposable = self._relay.pipe(
            ops.observe_on(AsyncIOScheduler(asyncio.get_event_loop())),
            ops.pairwise(),
            # ops.start_with((None, self._relay.value))
        ).subscribe(subscription_callback)

        return disposable
