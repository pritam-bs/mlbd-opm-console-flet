from abc import ABC, abstractmethod
from ....domain.entities.booking_entity import BookingEntity
from typing import Union, List
from ....domain.error.app_error import AppException


class BookingRepository(ABC):

    @abstractmethod
    def get_all_bookings() -> List[BookingEntity]:
        pass
