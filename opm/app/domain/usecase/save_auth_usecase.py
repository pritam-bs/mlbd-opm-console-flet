from typing import Union

from ..entities.auth_entity import AuthEntity
from ..services.auth.auth_repository import AuthRepository


class SaveAuthUsecase:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def run(self, auth_entity: AuthEntity):
        return self.auth_repository.save_auth_info(auth_entity=auth_entity)
