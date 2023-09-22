from ......data.database.database_storage import DatabaseStorage
from ......data.model.auth.auth_dto import AuthDTO
from typing import Optional
from loguru import logger


class AuthLocalDatasouce:
    def __init__(self, database_storage: DatabaseStorage):
        logger.info("Init AuthLocalDatasouce")
        self.database_storage = database_storage

    def save(self, auth_dto: AuthDTO):
        result = self.database_storage.exists(data=AuthDTO.key())
        if result:
            dict = self.database_storage.update(
                data=AuthDTO.key(), updated_data=auth_dto.to_dict())
        else:
            dict = self.database_storage.insert(data=auth_dto.to_dict())
            logger.debug(dict)

    def get(self) -> Optional[AuthDTO]:
        key = AuthDTO.key()
        result = self.database_storage.exists(data=key)
        if result:
            data_dict = self.database_storage.find(data=AuthDTO.key())
            auth_dto = AuthDTO.from_dict(data_dict=data_dict)
            return auth_dto
        else:
            return None
