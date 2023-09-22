from abc import ABC, abstractmethod
from typing import Optional
from ....domain.entities.token_entiry import TokenEntity


class TokenRepository(ABC):

    @abstractmethod
    async def get_token(self, client_name: str, password: str) -> TokenEntity:
        pass
