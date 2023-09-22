from ....data.model.auth.auth_dto import AuthDTO
from ....domain.entities.auth_entity import AuthEntity


class AuthRemapper:
    @staticmethod
    def map_from(auth_dto: AuthDTO):
        return AuthEntity(
            access_token=auth_dto.access_token,
            refresh_token=auth_dto.refresh_token)

    @staticmethod
    def map_to(auth_entity: AuthEntity):
        return AuthDTO(
            access_token=auth_entity.access_token,
            refresh_token=auth_entity.refresh_token)
