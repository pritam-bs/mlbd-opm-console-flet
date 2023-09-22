from typing import Union

from ..entities.auth_entity import AuthEntity
from ..services.auth.auth_repository import AuthRepository


class GetAuthUsecase:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def run(self) -> Union[AuthEntity, None]:
        return self.auth_repository.get_auth_info()
