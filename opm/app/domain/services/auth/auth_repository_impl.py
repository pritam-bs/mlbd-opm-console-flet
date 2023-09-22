from ....domain.services.auth.auth_repository import AuthRepository
from ....domain.services.auth.auth_dto_remapper import AuthRemapper
from ....data.services.auth.data_source.local.auth_local_datasource import AuthLocalDatasouce
from ....domain.entities.auth_entity import AuthEntity
from typing import Optional
from loguru import logger


class AuthRepositoryImpl(AuthRepository):
    def __init__(self, auth_local_datasource: AuthLocalDatasouce, auth_remapper: AuthRemapper):
        logger.info("Init AuthRepositoryImpl")
        self.auth_local_datasource = auth_local_datasource
        self.auth_remapper = auth_remapper

    def get_auth_info(self) -> Optional[AuthEntity]:
        response = self.auth_local_datasource.get()
        if response is not None:
            auth_entities = AuthRemapper.map_from(auth_dto=response)
            return auth_entities
        else:
            return None

    def save_auth_info(self, auth_entity: AuthEntity):
        auth_dto = AuthRemapper.map_to(auth_entity=auth_entity)
        self.auth_local_datasource.save(auth_dto=auth_dto)
