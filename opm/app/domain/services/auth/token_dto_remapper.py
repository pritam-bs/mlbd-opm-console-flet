from ....data.model.auth.token_dto import TokenDTO
from ....domain.entities.token_entiry import TokenEntity


class TokenRemapper:
    @staticmethod
    def map_from(token_dto: TokenDTO):
        return TokenEntity(
            access_token=token_dto.access_token,
            refresh_token=token_dto.refresh_token)

    @staticmethod
    def map_to(token_entity: TokenEntity):
        return TokenDTO(
            access_token=token_entity.access_token,
            refresh_token=token_entity.refresh_token)
