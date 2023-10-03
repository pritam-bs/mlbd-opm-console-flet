from ....domain.services.model_downloader.model_downloader_repository import CallbackFunc, ModelDownloaderRepository
from ....data.services.model_downloader.datasource.remote.model_downloader_remote_datasource import ModelDownloaderRemoteDatasource


class ModelDownloaderRepositoryImpl(ModelDownloaderRepository):
    def __init__(self, model_downloader_remote_datasource: ModelDownloaderRemoteDatasource) -> None:
        super().__init__()
        self.model_downloader_remote_datasource = model_downloader_remote_datasource

    async def download(self, callback: CallbackFunc):
        await self.model_downloader_remote_datasource.download(callback=callback)
