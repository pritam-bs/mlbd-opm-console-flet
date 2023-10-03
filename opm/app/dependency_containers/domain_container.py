from dependency_injector import containers, providers

from ..domain.usecase.face_recognition_usecase import FaceRecognitionUsecase
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
from ..domain.services.face_recognition.face_recognition_repository_impl import FaceRecognitionRepositoryImpl
from ..domain.services.synchronizer.booking_sqs_repository_impl import BookingSqsRepositoryImpl
from ..domain.services.synchronizer.model_sqs_repository_impl import ModelSqsRepositoryImpl
from ..domain.services.model_downloader.model_downloader_repository_impl import ModelDownloaderRepositoryImpl
from ..domain.usecase.booking_synchronizer_usecase import BookingSynchronizerUsecase
from ..domain.usecase.model_synchronizer_usecase import ModelSynchronizerUsecase
from ..domain.usecase.model_downloader_usecase import ModelDownloaderUsecase


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

    # Crate a dependency provider since it depends on data_container
    booking_sqs_remote_datasource_dependency = providers.Dependency()

    # Crate a dependency provider since it depends on data_container
    model_sqs_remote_datasource_dependency = providers.Dependency()

    # Crate a dependency provider since it depends on data_container
    model_downloader_remote_datasource_dependency = providers.Dependency()

    # Crate a dependency provider since it depends on data_container
    face_recognition_datasource_dependency = providers.Dependency()

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

    # Create a provider for FaceRecognitionRepositoryImpl. Dependencies will be injected from the DataContainer.
    face_recognition_repository_impl = providers.Singleton(
        FaceRecognitionRepositoryImpl,
        face_recognition_datasource=face_recognition_datasource_dependency,
        booking_repository=booking_repository_impl
    )

    # Create a provider for BookingSqsRepositoryImpl. Dependencies will be injected from the DataContainer.
    bookin_sqs_repository_impl = providers.Singleton(
        BookingSqsRepositoryImpl,
        booking_sqs_remote_datasource=booking_sqs_remote_datasource_dependency
    )

    # Create a provider for ModelSqsRepositoryImpl. Dependencies will be injected from the DataContainer.
    model_sqs_repository_impl = providers.Singleton(
        ModelSqsRepositoryImpl,
        model_sqs_remote_datasource=model_sqs_remote_datasource_dependency,
    )

    # Create a provider for ModelDownloaderRepositoryImpl. Dependencies will be injected from the DataContainer.
    model_downloader_repository_impl = providers.Singleton(
        ModelDownloaderRepositoryImpl,
        model_downloader_remote_datasource=model_downloader_remote_datasource_dependency,
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

    # Create a provider for FaceRecognitionUsecase
    face_recognition_usecase = providers.Factory(
        FaceRecognitionUsecase,
        face_recognition_repository=face_recognition_repository_impl
    )

    # Create a provider for BookingSynchronizerUsecase
    booking_synchronizer_usecase = providers.Factory(
        BookingSynchronizerUsecase,
        booking_sqs_repository=bookin_sqs_repository_impl
    )

    # Create a provider for ModelSynchronizerUsecase
    model_sychronizer_usecase = providers.Factory(
        ModelSynchronizerUsecase,
        model_sqs_repository=model_sqs_repository_impl
    )

    # Create a provider for ModelDownloaderUsecase
    model_downloader_usecase = providers.Factory(
        ModelDownloaderUsecase,
        model_downloader_repository=model_downloader_repository_impl
    )
