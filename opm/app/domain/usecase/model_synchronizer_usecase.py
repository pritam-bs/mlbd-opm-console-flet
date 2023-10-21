from ...domain.services.synchronizer.model_sqs_repository import ModelSqsRepository, ModelUpdateFunc


class ModelSynchronizerUsecase:
    def __init__(self, model_sqs_repository: ModelSqsRepository) -> None:
        self.model_sqs_repository = model_sqs_repository

    async def start(self, on_model_update: ModelUpdateFunc):
        await self.model_sqs_repository.start(on_model_update=on_model_update)

    def stop(self):
        self.model_sqs_repository.stop()
