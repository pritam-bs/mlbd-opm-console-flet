from ..core.abstractions import State
from ..domain.entities.auth_entity import AuthEntity
from ..domain.error.app_error import AppException
from typing import Union, Optional
from dataclasses import dataclass
from ..dependency_containers.application_container import ApplicationContainer
from loguru import logger


@dataclass(frozen=True)
class SplashState(State):
    is_loading: Optional[bool]
    is_authenticated: Optional[bool]
    client_name: Optional[str]
    password: Optional[str]
    error: Optional[str]
    can_submit: Optional[bool]

    @classmethod
    def initial_state(cls) -> 'SplashState':
        return cls(is_loading=None, is_authenticated=None, client_name=None, password=None, error=None, can_submit=None)

    @classmethod
    def compare(cls, obj1, obj2):
        """Compare two SplashState objects and return a new SplashState object with the differences."""
        kwargs = {}
        for field in cls.__dataclass_fields__:
            if getattr(obj1, field) != getattr(obj2, field):
                kwargs[field] = getattr(obj2, field)
            else:
                kwargs[field] = None
        return cls(**kwargs)

    def mutate(self, is_loading=None, is_authenticated=None, client_name=None, password=None, error=None, can_submit=None):
        mutated_state = SplashState(
            is_loading=is_loading if is_loading is not None else self.is_loading,
            is_authenticated=is_authenticated if is_authenticated is not None else self.is_authenticated,
            client_name=client_name if client_name is not None else self.client_name,
            password=password if password is not None else self.password,
            error=error if error is not None else self.error,
            can_submit=can_submit if can_submit is not None else self.can_submit
        )
        return mutated_state


class SplashViewModel:
    def __init__(self):
        container = ApplicationContainer()
        self.get_auth_usecase = container.domain.container.get_auth_usecase()
        self.save_auth_usecase = container.domain.container.save_auth_usecase()
        self.get_token_usecase = container.domain.container.get_token_usecase()

    def validate_input(self, prev_state: SplashState, client_name: Optional[str] = None, password: Optional[str] = None):
        current_state: SplashState = prev_state.mutate(
            client_name=client_name, password=password)
        if current_state.password is not None and current_state.client_name is not None:
            current_state = current_state.mutate(can_submit=True)
        return current_state

    def check_authentication(self, prev_state: SplashState):
        auth_entity = self.get_auth_usecase.run()
        current_state = prev_state.mutate(is_authenticated=False)
        return current_state

    async def submit(self, state: SplashState):
        client_name = state.client_name
        password = state.password
        try:
            token = await self.get_token_usecase.run(client_name=client_name, password=password)
            self._save_auth_info(
                access_token=token.access_token,
                refresh_token=token.refresh_token)
            new_state = state.mutate(is_authenticated=True, is_loading=False)
            return new_state
        except AppException as app_exception:
            error = app_exception.error
            status = error.status_code
            if error.content:
                message = error.content.get("message", None)
                code = error.content.get("code", None)
                data = error.content.get("data", None)
            new_state = state.mutate(error=message, is_loading=False)
            return new_state

    def _save_auth_info(self, access_token: str, refresh_token: str):
        auth_entity = AuthEntity(
            access_token=access_token, refresh_token=refresh_token)
        self.save_auth_usecase.run(auth_entity=auth_entity)
        auth_entity = self.get_auth_usecase.run()
        logger.debug(f"Saved auth info: {auth_entity}")

    def change_loading_state(self, state: SplashState, is_loading: bool):
        new_state = state.mutate(is_loading=is_loading)
        return new_state

    def clear_error(self, state: SplashState):
        new_state = state.mutate(error="")
        return new_state
