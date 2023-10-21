from abc import ABC, abstractmethod
from typing import Callable, Dict
from ....data.model.synchronizer.model_update_dto import ModelUpdateDTO
from ...entities.model_update_entity import ModelUpdateEntity

# Define a type alias for the callable
ModelUpdateFunc = Callable[[ModelUpdateEntity], None]


class ModelSqsRepository(ABC):

    @abstractmethod
    async def start(self, on_model_update: ModelUpdateFunc):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def model_update_callback(self, model_update_dto: ModelUpdateDTO):
        pass
