from typing import List
from ...domain.services.synchronizer.model_sqs_repository import ModelSqsRepository, ModelUpdateFunc


class ModelSynchronizerUsecase:
    def __init__(self, model_sqs_repository: ModelSqsRepository) -> None:
        self.model_sqs_repository = model_sqs_repository

    async def start(self, on_model_update: ModelUpdateFunc):
        await self.model_sqs_repository.start(on_model_update=on_model_update)

    async def delete_message(self, receipt_handle_list: List[str]):
        await self.model_sqs_repository.delete_messages(
            receipt_handle_list=receipt_handle_list)

    def stop(self):
        self.model_sqs_repository.stop()
