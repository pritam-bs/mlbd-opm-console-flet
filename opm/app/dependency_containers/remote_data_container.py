from dependency_injector import containers, providers

from ..data.services.booking.data_source.remote.booking_remore_datasource import BookingRemoteDatasource
from ..data.api.api_client import APIClient
from ..data.services.auth.data_source.remote.token_remote_datasource import TokenRemoteDatasource
from ..settings.settings import settings
from ..data.synchronizer.sqs_client import SqsClient
from ..data.services.synchronizer.datasource.remote.booking_sqs_remote_datasource import BookingSqsRemoteDatasource
from ..data.services.synchronizer.datasource.remote.model_sqs_remote_datasource import ModelSqsRemoteDatasource
from ..data.model_downloader.model_downloader import ModelDownloader
from ..data.services.model_downloader.datasource.remote.model_downloader_remote_datasource import ModelDownloaderRemoteDatasource
from ..data.services.meal.consume_meal_service import ConsumeMealService
from ..data.services.employee_onboard_notify.employee_onboard_notify_service import EmployeeOnboardNotifyService


class RemoteDataContainer(containers.DeclarativeContainer):
    # Create a provider for APIClient
    api_client = providers.Singleton(
        APIClient,
        base_url=settings.opm_base_url
    )

    # Create a provider for BookingRemoteDatasource
    booking_remote_datasource = providers.Singleton(
        BookingRemoteDatasource,
        api_client=api_client
    )

    token_remote_datasource = providers.Singleton(
        TokenRemoteDatasource,
        api_client=api_client
    )

    # Create a provider for SqsClient
    sqs_client = providers.Singleton(
        SqsClient
    )

    # Create a provider for BookingSqsRemoteDatasource
    booking_sqs_remote_datasource = providers.Singleton(
        BookingSqsRemoteDatasource,
        sqs_client=sqs_client
    )

    # Create a provider for ModelSqsRemoteDatasource
    model_sqs_remote_datasource = providers.Singleton(
        ModelSqsRemoteDatasource,
        sqs_client=sqs_client
    )

    # Create a provider for ModelDownloader
    model_downloader = providers.Singleton(
        ModelDownloader
    )

    # Create a provider for ModelDownloaderRemoteDatasource
    model_downloader_remote_datasource = providers.Singleton(
        ModelDownloaderRemoteDatasource,
        model_downloader=model_downloader
    )

    # Create a provider for ConsumeMealService
    comsume_meal_service = providers.Singleton(
        ConsumeMealService,
        api_client=api_client
    )

    # Create a provider for EmployeeOnboardNotifyService
    employee_onboard_notify_service = providers.Singleton(
        EmployeeOnboardNotifyService,
        api_client=api_client
    )
