from abc import ABC, abstractmethod
from typing import Callable, Dict
from ....data.model.synchronizer.booking_update_dto import BookingUpdateListDTO
from ...entities.booking_update_entity import BookingUpdateListEntity

# Define a type alias for the callable
BookingUpdateFunc = Callable[[BookingUpdateListEntity], None]


class BookingSqsRepository(ABC):

    @abstractmethod
    async def start(self, on_booking_update: BookingUpdateFunc):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def booking_update_callback(self, booking_update_list_dto: BookingUpdateListDTO):
        pass
