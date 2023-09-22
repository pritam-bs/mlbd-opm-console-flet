from dependency_injector import containers, providers

from ..data.services.auth.data_source.local.auth_local_datasource import AuthLocalDatasouce
from ..data.database.database_storage_impl import DatabaseStorageImpl


class LocalDataContainer(containers.DeclarativeContainer):

    # Create a provider for DatabaseStorageImpl
    database_storage_impl = providers.Singleton(
        DatabaseStorageImpl,
    )

    # Create a provider for AuthLocalDatasouce
    auth_local_datasource = providers.Singleton(
        AuthLocalDatasouce,
        database_storage=database_storage_impl
    )
