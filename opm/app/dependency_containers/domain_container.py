from dependency_injector import containers, providers

from ..domain.usecase.get_auth_usecase import GetAuthUsecase
from ..domain.usecase.save_auth_usecase import SaveAuthUsecase
from ..domain.services.auth.auth_repository_impl import AuthRepositoryImpl
from ..domain.services.auth.auth_dto_remapper import AuthRemapper
from ..domain.usecase.booking_usecase import BookingUsecase
from ..domain.services.booking.booking_dto_remapper import BookingRemapper
from ..domain.services.booking.booking_repository_impl import BookingRepositoryImpl
from ..domain.services.auth.token_repository_impl import TokenRepositoryImpl
from ..domain.services.auth.token_dto_remapper import TokenRemapper
from ..domain.usecase.get_token_usecase import GetTokenUsecase


class DomainContainer(containers.DeclarativeContainer):

    # Create a provider for AuthRemapper since it doesn't have any dependencies
    auth_remapper = providers.Singleton(AuthRemapper)

    # Crate a provert for BookingRemapper since it doesn't have any dependencies
    booking_remapper = providers.Singleton(BookingRemapper)

    # Crate a provert for TokenRemapper since it doesn't have any dependencies
    token_remapper = providers.Singleton(TokenRemapper)

    # Create a dependency provider since it depends on data_container
    auth_local_datasource_dependency = providers.Dependency()

    # Create a dependency provider since it depends on data_container
    booking_remote_datasource_dependency = providers.Dependency()

    # Crate a dependency provider since it depends on data_container
    token_remote_datasource_dependency = providers.Dependency()

    # Create a provider for AuthRepositoryImpl. Dependencies will be injected from the DataContainer.
    auth_repository_impl = providers.Singleton(
        AuthRepositoryImpl,
        auth_local_datasource=auth_local_datasource_dependency,
        auth_remapper=auth_remapper
    )

    # Create a provider for BookingRepositoryImpl. Dependencies will be injected from the DataContainer.
    booking_repository_impl = providers.Singleton(
        BookingRepositoryImpl,
        booking_remote_datasource=booking_remote_datasource_dependency,
        booking_remapper=booking_remapper
    )

    # Create a provider for TokenRepositoryImpl. Dependencies will be injected from the DataContainer.
    token_repository_impl = providers.Singleton(
        TokenRepositoryImpl,
        token_remote_datasource=token_remote_datasource_dependency,
        token_remapper=token_remapper
    )

    # Create a provider for GetAuthUsecase
    get_auth_usecase = providers.Factory(
        GetAuthUsecase,
        auth_repository=auth_repository_impl
    )

    # Create a provider for SaveAuthUsecase
    save_auth_usecase = providers.Factory(
        SaveAuthUsecase,
        auth_repository=auth_repository_impl
    )

    # Create a provider for BookingUsecase
    booking_usecase = providers.Factory(
        BookingUsecase,
        booking_repository=booking_repository_impl
    )

    # Create a provider for GetTokenUsecase
    get_token_usecase = providers.Factory(
        GetTokenUsecase,
        token_repository=token_repository_impl

    )
