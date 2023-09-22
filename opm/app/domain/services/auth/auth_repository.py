from abc import ABC, abstractmethod
from typing import Optional
from ....domain.entities.auth_entity import AuthEntity


class AuthRepository(ABC):

    @abstractmethod
    def get_auth_info(self) -> Optional[AuthEntity]:
        pass

    @abstractmethod
    def save_auth_info(self, auth_entity: AuthEntity):
        pass
