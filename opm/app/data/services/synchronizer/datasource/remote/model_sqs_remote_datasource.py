from typing import Callable, Dict, List
from ......data.synchronizer.sqs_client import SqsClient, ModelUpdateFunc
from ......data.model.synchronizer.model_update_dto import ModelUpdateDTO


class ModelSqsRemoteDatasource:
    def __init__(self, sqs_client: SqsClient) -> None:
        self.sqs_client = sqs_client

    async def start(self, on_model_update: ModelUpdateFunc):
        await self.sqs_client.start_model_update_listener(
            on_model_update=on_model_update)

    async def delete_messages(self, receipt_handle_list: List[str]):
        await self.sqs_client.delete_model_update_messages(receipt_handle_list=receipt_handle_list)

    def stop(self):
        self.sqs_client.stop_model_update_listener()
