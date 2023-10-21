from typing import Callable, Dict
from ......data.synchronizer.sqs_client import SqsClient
from ......data.model.synchronizer.model_update_dto import ModelUpdateDTO
# Define a type alias for the callable
ModelUpdateFunc = Callable[[ModelUpdateDTO], None]


class ModelSqsRemoteDatasource:
    def __init__(self, sqs_client: SqsClient) -> None:
        self.sqs_client = sqs_client

    async def start(self, on_model_update: ModelUpdateFunc):
        await self.sqs_client.start_model_update_listener(
            on_model_update=on_model_update)

    def stop(self):
        self.sqs_client.stop_model_update_listener()
