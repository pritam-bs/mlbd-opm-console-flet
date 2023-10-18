from ......data.model_downloader.model_downloader import ModelDownloader, CallbackFunc


class ModelDownloaderRemoteDatasource:
    def __init__(self, model_downloader: ModelDownloader) -> None:
        self.model_downloader = model_downloader

    async def download(self, callback: CallbackFunc):
        await self.model_downloader.download_models(callback=callback)
