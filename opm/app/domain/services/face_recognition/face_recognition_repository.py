from abc import ABC, abstractmethod
from typing import Callable, Optional, Union
from ....domain.entities.booking_entity import BookingEntity

# Define a type alias for the callable
ImageFunc = Callable[[Optional[str]], None]
MatchFunc = Callable[[Union[BookingEntity, str]], None]


class FaceRecognitionRepository(ABC):

    @abstractmethod
    def start(self, on_image_receive: ImageFunc, on_match: MatchFunc):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def reload_model(self):
        pass
