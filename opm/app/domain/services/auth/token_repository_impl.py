from ....domain.error.app_error import AppException
from ....domain.services.auth.token_repository import TokenRepository
from ....domain.services.auth.token_dto_remapper import TokenRemapper
from ....data.services.auth.data_source.remote.token_remote_datasource import TokenRemoteDatasource
from ....data.model.error.response_error import ResponseError
from ....domain.entities.token_entiry import TokenEntity
from loguru import logger


class TokenRepositoryImpl(TokenRepository):
    def __init__(self, token_remote_datasource: TokenRemoteDatasource):
        logger.info("Init TokenRepositoryImpl")
        self.token_remote_datasource = token_remote_datasource

    async def get_token(self, client_name: str, password: str) -> TokenEntity:
        try:
            token_dto = await self.token_remote_datasource.login(
                client_name=client_name, password=password)
            token_entity = TokenRemapper.map_from(token_dto=token_dto)
            return token_entity
        except ResponseError as response_error:
            raise AppException.from_response_error(response_error)
