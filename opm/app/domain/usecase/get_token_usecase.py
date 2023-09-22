from typing import Union

from ..entities.token_entiry import TokenEntity
from ..services.auth.token_repository import TokenRepository
from ...domain.error.app_error import AppException


class GetTokenUsecase:
    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository

    async def run(self, client_name: str, password: str) -> Union[TokenEntity, AppException]:
        return await self.token_repository.get_token(client_name=client_name, password=password)
