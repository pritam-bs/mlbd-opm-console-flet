
from typing import Callable, Optional
import numpy as np
from ......data.face_recognition.face_recognizer import FaceRecognizer

# Define a type alias for the callable
ImageFunc = Callable[[Optional[np.ndarray]], None]
MatchFunc = Callable[[str], None]


class FacaRecognitionDatasource:
    def __init__(self, face_recognizer: FaceRecognizer) -> None:
        self._face_recognizer = face_recognizer

    def start(self, on_image_receive: ImageFunc, on_match: MatchFunc):
        self._face_recognizer.load_knn_model()
        self._face_recognizer.start(
            on_image_receive=on_image_receive, on_match=on_match)

    def stop(self):
        self._face_recognizer.stop()

    def reload_model(self):
        self._face_recognizer.load_knn_model()
