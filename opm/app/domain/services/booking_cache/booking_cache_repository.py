from abc import ABC, abstractmethod
from typing import Dict, List
from ....domain.entities.booking_entity import BookingEntity
from ....domain.entities.booking_update_entity import BookingUpdateListEntity


class BookingCacheRepository(ABC):
    @abstractmethod
    def make_cache(self, bookings: List[BookingEntity]):
        pass

    @abstractmethod
    def get_all_bookings(self) -> Dict[str, BookingEntity]:
        pass

    @abstractmethod
    def update_cache(self, booking_updates: BookingUpdateListEntity):
        pass
