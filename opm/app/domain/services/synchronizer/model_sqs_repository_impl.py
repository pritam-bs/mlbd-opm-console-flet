from ....domain.services.synchronizer.model_sqs_repository import ModelChangeFunc, ModelSqsRepository
from ....data.services.synchronizer.datasource.remote.model_sqs_remote_datasource import ModelSqsRemoteDatasource


class ModelSqsRepositoryImpl(ModelSqsRepository):
    def __init__(self, model_sqs_remote_datasource: ModelSqsRemoteDatasource) -> None:
        super().__init__()
        self.model_sqs_remote_datasource = model_sqs_remote_datasource

    def start(self, on_model_change: ModelChangeFunc):
        self.model_sqs_remote_datasource.start(on_model_change=on_model_change)

    def stop(self):
        self.model_sqs_remote_datasource.stop()
