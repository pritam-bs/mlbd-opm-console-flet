from abc import ABC, abstractmethod
from typing import Callable, Dict

# Define a type alias for the callable
BookingChangeFunc = Callable[[Dict], None]


class BookingSqsRepository(ABC):

    @abstractmethod
    def start(self, on_booking_change: BookingChangeFunc):
        pass

    @abstractmethod
    def stop(self):
        pass
