from opm.app.data.model.synchronizer.model_change_dto import ModelChangeDTO
from ....domain.services.synchronizer.model_sqs_repository import ModelChangeFunc, ModelSqsRepository
from ....data.services.synchronizer.datasource.remote.model_sqs_remote_datasource import ModelSqsRemoteDatasource
from ....domain.services.synchronizer.model_change_dto_remapper import ModelChangeRemapper


class ModelSqsRepositoryImpl(ModelSqsRepository):
    def __init__(self, model_sqs_remote_datasource: ModelSqsRemoteDatasource) -> None:
        super().__init__()
        self.model_sqs_remote_datasource = model_sqs_remote_datasource

    async def start(self, on_model_change: ModelChangeFunc):
        self.on_model_change = on_model_change
        await self.model_sqs_remote_datasource.start(
            on_model_change=self.model_change_callback)

    def stop(self):
        self.model_sqs_remote_datasource.stop()

    def model_change_callback(self, model_change_dto: ModelChangeDTO):
        model_change_entity = ModelChangeRemapper.map_from(
            model_change_dto=model_change_dto)
        self.on_model_change(model_change_entity)
