from abc import ABC, abstractmethod
from typing import Callable, Dict
from ....data.model.synchronizer.model_change_dto import ModelChangeDTO
from ....domain.entities.model_change_entity import ModelChangeEntity

# Define a type alias for the callable
ModelChangeFunc = Callable[[ModelChangeEntity], None]


class ModelSqsRepository(ABC):

    @abstractmethod
    async def start(self, on_model_change: ModelChangeFunc):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def model_change_callback(self, model_change_dto: ModelChangeDTO):
        pass
