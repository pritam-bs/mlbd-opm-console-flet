from ...domain.services.face_recognition.face_recognition_repository import FaceRecognitionRepository, ImageFunc, MatchFunc


class FaceRecognitionUsecase:
    def __init__(self, face_recognition_repository: FaceRecognitionRepository) -> None:
        self._face_recognition_repository = face_recognition_repository

    def start(self, on_image_receive: ImageFunc, on_match: MatchFunc):
        self._face_recognition_repository.start(
            on_image_receive=on_image_receive, on_match=on_match)

    def stop(self):
        self._face_recognition_repository.stop()

    def reload_model(self):
        self._face_recognition_repository.reload_model()
