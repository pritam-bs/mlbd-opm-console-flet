from typing import Callable, Dict
from ......data.synchronizer.sqs_client import SqsClient
# Define a type alias for the callable
ModelChangeFunc = Callable[[Dict], None]


class ModelSqsRemoteDatasource:
    def __init__(self, sqs_client: SqsClient) -> None:
        self.sqs_client = sqs_client

    async def start(self, on_model_change: ModelChangeFunc):
        await self.sqs_client.start_model_change_listener(
            on_model_change=on_model_change)

    def stop(self):
        self.sqs_client.stop_model_change_listener()
