from abc import ABC, abstractmethod
from typing import Callable, Dict

# Define a type alias for the callable
ModelChangeFunc = Callable[[Dict], None]


class ModelSqsRepository(ABC):

    @abstractmethod
    def start(self, on_model_change: ModelChangeFunc):
        pass

    @abstractmethod
    def stop(self):
        pass
