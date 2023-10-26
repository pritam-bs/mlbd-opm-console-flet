from abc import ABC, abstractmethod
from typing import Callable, Dict, List
from ....data.model.synchronizer.booking_update_dto import BookingUpdateListDTO
from ...entities.booking_update_entity import BookingUpdateListEntity

# Define a type alias for the callable
BookingUpdateFunc = Callable[[BookingUpdateListEntity, List[str]], None]


class BookingSqsRepository(ABC):

    @abstractmethod
    async def start(self, on_booking_update: BookingUpdateFunc):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    async def delete_messages(self, receipt_handle_list: List[str]):
        pass

    @abstractmethod
    def booking_update_callback(self, booking_update_list_dto: BookingUpdateListDTO):
        pass
