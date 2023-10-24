import asyncio
from typing import Callable, Optional
import cv2
import numpy as np

from ...data.face_recognition.feature_generator.arc_face_feature_generator import ArcFaceGenerator
from ...data.face_recognition.knn_search.knn_search import KnnSearch
from ...data.face_recognition.fas.fas_detector import FasDetector
from ...data.face_recognition.face_detector.cascade_face_detector import CascadeDetector
from ...data.face_recognition.image_capture.capture_image import CaptureImage
from ...data.utils.repetitive_timer import RepetitiveTimer
from loguru import logger

# Define a type alias for the callable
ImageFunc = Callable[[Optional[np.ndarray]], None]
MatchFunc = Callable[[str], None]


class FaceRecognizer:
    def __init__(self, capture_interval: float = 1.0/30.0, rtspUrl: Optional[str] = None):
        self._capture_interval = capture_interval
        self._capture_image = CaptureImage(rtspUrl=rtspUrl)
        self._cascade_detector = CascadeDetector(image_size=(112, 112))
        self._fas_detector = FasDetector()
        self._arc_face_generator = ArcFaceGenerator()
        self._knn_search = KnnSearch()

    def __del__(self):
        self._repetitive_timer.stop_timer()

    def start(self, on_image_receive: ImageFunc, on_match: MatchFunc):
        self._on_image_receive = on_image_receive
        self._on_match = on_match
        self._repetitive_timer = RepetitiveTimer(
            self._capture_interval, self._recognizer)
        self._repetitive_timer.start_timer()

    def stop(self):
        if self._repetitive_timer:
            self._repetitive_timer.stop_timer()

    def load_knn_model(self):
        self._knn_search.load_models()

    async def _recognizer(self):
        frame = self._capture_image.getFrame()
        if frame is None:
            return

        face_image, bbox = self._face_extractor(frame=frame)
        # is_live = self._fas_detector.liveness_detector(
        #     face_image=face_image)
        is_live = True
        await self._update_image_for_viewing(frame=frame, bbox=bbox, is_live=is_live)

        if face_image is not None and is_live is not None and is_live:
            embeddings = self._face_embedding_generator(
                face_image_list=[face_image])
            matched_id = self._knn_search.search(embeddings=embeddings)
            if matched_id is not None:
                await self._on_match(matched_id)

    def _face_extractor(self, frame):
        face_image = None
        bbox = None
        if frame is not None:
            face_image, bbox = self._cascade_detector.extract_face(
                frame=frame)
        return face_image, bbox

    async def _update_image_for_viewing(self, frame, bbox, is_live):
        if bbox:
            color = (0, 0, 255)
            if is_live:
                color = (0, 255, 0)
            x, y, w, h = bbox
            left = x
            up = y
            right = x + w
            down = y + h
            cv2.line(frame, (left, up), (right, up), color, 1, cv2.LINE_AA)
            cv2.line(frame, (right, up), (right, down),
                     color, 1, cv2.LINE_AA)
            cv2.line(frame, (right, down), (left, down),
                     color, 1, cv2.LINE_AA)
            cv2.line(frame, (left, down), (left, up),
                     color, 1, cv2.LINE_AA)

        await self._on_image_receive(frame)

    def _face_embedding_generator(self, face_image_list):
        if face_image_list is not None:
            embeddings = self._arc_face_generator.get_feature_vectors(
                face_image_list)
        return embeddings
