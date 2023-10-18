from abc import ABC, abstractmethod
from typing import Callable
CallbackFunc = Callable[[bool], None]


class ModelDownloaderRepository(ABC):

    @abstractmethod
    async def download(self, callback: CallbackFunc):
        pass
