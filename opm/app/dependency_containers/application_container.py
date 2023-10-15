from dependency_injector import containers, providers

from .remote_data_container import RemoteDataContainer
from .local_data_container import LocalDataContainer
from ..dependency_containers.domain_container import DomainContainer
from loguru import logger


class ApplicationContainer(containers.DeclarativeContainer):
    remote_data = providers.Container(RemoteDataContainer)
    local_data = providers.Container(LocalDataContainer)
    domain = providers.Container(
        DomainContainer,
        auth_local_datasource_dependency=local_data.container.auth_local_datasource,
        booking_remote_datasource_dependency=remote_data.container.booking_remote_datasource,
        token_remote_datasource_dependency=remote_data.container.token_remote_datasource,
        face_recognition_datasource_dependency=local_data.container.faca_recognition_datasource,
        booking_sqs_remote_datasource_dependency=remote_data.container.booking_sqs_remote_datasource,
        model_sqs_remote_datasource_dependency=remote_data.container.model_sqs_remote_datasource,
        model_downloader_remote_datasource_dependency=remote_data.container.model_downloader_remote_datasource,
    )

    def __del__(self):
        logger.debug("ApplicationContainer deallocated")


# Define a Singleton provider for ApplicationContainer
application_container_provider = providers.Singleton(ApplicationContainer)
