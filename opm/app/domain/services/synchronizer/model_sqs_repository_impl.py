from typing import List
from opm.app.data.model.synchronizer.model_update_dto import ModelUpdateDTO
from ....domain.services.synchronizer.model_sqs_repository import ModelUpdateFunc, ModelSqsRepository
from ....data.services.synchronizer.datasource.remote.model_sqs_remote_datasource import ModelSqsRemoteDatasource
from .model_update_dto_remapper import ModelUpdateRemapper


class ModelSqsRepositoryImpl(ModelSqsRepository):
    def __init__(self, model_sqs_remote_datasource: ModelSqsRemoteDatasource) -> None:
        super().__init__()
        self.model_sqs_remote_datasource = model_sqs_remote_datasource

    async def start(self, on_model_update: ModelUpdateFunc):
        self.on_model_update = on_model_update
        await self.model_sqs_remote_datasource.start(
            on_model_update=self.model_update_callback)

    def stop(self):
        self.model_sqs_remote_datasource.stop()

    async def delete_messages(self, receipt_handle_list: List[str]):
        await self.model_sqs_remote_datasource.delete_messages(
            receipt_handle_list=receipt_handle_list)

    def model_update_callback(self, model_update_dto: ModelUpdateDTO, receipt_handle_list: List[str]):
        model_update_entity = ModelUpdateRemapper.map_sqs_dto(
            model_update_dto=model_update_dto)
        self.on_model_update(model_update_entity, receipt_handle_list)
