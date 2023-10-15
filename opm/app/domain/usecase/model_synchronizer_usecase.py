from ...domain.services.synchronizer.model_sqs_repository import ModelSqsRepository, ModelChangeFunc


class ModelSynchronizerUsecase:
    def __init__(self, model_sqs_repository: ModelSqsRepository) -> None:
        self.model_sqs_repository = model_sqs_repository

    async def start(self, on_model_change: ModelChangeFunc):
        await self.model_sqs_repository.start(on_model_change=on_model_change)

    def stop(self):
        self.model_sqs_repository.stop()
