from dependency_injector import containers, providers

from ..data.services.booking.data_source.remote.booking_remore_datasource import BookingRemoteDatasource
from ..data.api.api_client import APIClient
from ..data.services.auth.data_source.remote.token_remote_datasource import TokenRemoteDatasource
from ..settings.settings import settings


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
