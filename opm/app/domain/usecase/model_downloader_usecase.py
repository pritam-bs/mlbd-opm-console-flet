from ...domain.services.model_downloader.model_downloader_repository import ModelDownloaderRepository, CallbackFunc


class ModelDownloaderUsecase:
    def __init__(self, model_downloader_repository: ModelDownloaderRepository) -> None:
        self.model_downloader_repository = model_downloader_repository

    async def download(self, callback: CallbackFunc):
        await self.model_downloader_repository.download(callback=callback)
