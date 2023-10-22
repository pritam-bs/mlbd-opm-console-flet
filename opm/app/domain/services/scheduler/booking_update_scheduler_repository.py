from abc import ABC, abstractmethod
from typing import Callable, List

from ....domain.entities.booking_entity import BookingEntity

# Define a type alias for the callable
ScheduledBookingUpdateFunc = Callable[[List[BookingEntity]], None]


class BookingUpdateSchedulerRepository(ABC):
    @abstractmethod
    def start(self, on_booking_update: ScheduledBookingUpdateFunc):
        pass

    @abstractmethod
    def stop(self):
        pass
