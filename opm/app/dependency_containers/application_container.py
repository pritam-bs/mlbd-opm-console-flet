from dependency_injector import containers, providers

from .remote_data_container import RemoteDataContainer
from .local_data_container import LocalDataContainer
from ..dependency_containers.domain_container import DomainContainer


class ApplicationContainer(containers.DeclarativeContainer):
    remote_data = providers.Container(RemoteDataContainer)
    local_data = providers.Container(LocalDataContainer)
    domain = providers.Container(
        DomainContainer,
        auth_local_datasource_dependency=local_data.container.auth_local_datasource,
        booking_remote_datasource_dependency=remote_data.container.booking_remote_datasource,
        token_remote_datasource_dependency=remote_data.container.token_remote_datasource,
    )
