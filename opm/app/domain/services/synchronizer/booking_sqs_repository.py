from abc import ABC, abstractmethod
from typing import Callable, Dict
from ....data.model.synchronizer.booking_change_dto import BookingChangeDTO
from ....domain.entities.booking_change_entity import BookingChangeEntity

# Define a type alias for the callable
BookingChangeFunc = Callable[[BookingChangeEntity], None]


class BookingSqsRepository(ABC):

    @abstractmethod
    async def start(self, on_booking_change: BookingChangeFunc):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def booking_change_callback(self, booking_chnage_dto: BookingChangeDTO):
        pass
