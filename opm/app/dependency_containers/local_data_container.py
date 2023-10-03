from dependency_injector import containers, providers

from ..data.face_recognition.face_recognizer import FaceRecognizer
from ..data.services.face_recognition.data_source.local.face_recognition_local_datasource import FacaRecognitionDatasource
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

    # Create a provider for FaceRecognizer
    face_recognizer = providers.Singleton(
        FaceRecognizer,
        capture_interval=1.0/30.0,
        rtspUrl=None
    )

    # Create a provider for FacaRecognitionDatasource
    faca_recognition_datasource = providers.Singleton(
        FacaRecognitionDatasource,
        face_recognizer=face_recognizer
    )
