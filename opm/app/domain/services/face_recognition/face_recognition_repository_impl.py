import base64
import cv2

from ....domain.entities.booking_entity import BookingEntity
from ....domain.services.booking.booking_repository import BookingRepository
from ....data.services.face_recognition.data_source.local.face_recognition_local_datasource import FacaRecognitionDatasource
from ....domain.services.face_recognition.face_recognition_repository import FaceRecognitionRepository, ImageFunc, MatchFunc
from typing import List, Optional, Union
import numpy as np


class FaceRecognitionRepositoryImpl(FaceRecognitionRepository):
    def __init__(
        self,
        face_recognition_datasource: FacaRecognitionDatasource,
        booking_repository: BookingRepository
    ) -> None:
        super().__init__()
        self._face_recognition_datasource = face_recognition_datasource
        self._booking_repository = booking_repository

    def start(self, on_image_receive: ImageFunc, on_match: MatchFunc):
        self.on_image_receive = on_image_receive
        self.on_match = on_match
        self._face_recognition_datasource.start(
            on_image_receive=self._on_image_receive,
            on_match=self._on_match
        )

    def stop(self):
        self._face_recognition_datasource.stop()

    def reload_model(self):
        self._face_recognition_datasource.reload_model()

    async def _on_image_receive(self, frame: Optional[np.ndarray]):
        jpg_as_text = self._ndarray_to_base64(image=frame)
        await self.on_image_receive(jpg_as_text)

    def _ndarray_to_base64(self, image: np.ndarray, format: str = 'JPEG') -> str:
        # Convert numpy image to bytes
        is_success, buffer = cv2.imencode(f".{format}", image)
        if not is_success:
            raise ValueError("Could not encode image!")

        # Convert bytes to base64 encoded string
        img_str = base64.b64encode(buffer.tobytes()).decode('utf-8')

        return img_str

    async def _on_match(self, employee_id: str):
        booking_list = await self._booking_repository.get_all_bookings()
        matched_employee = self.get_booking_by_employee_id(
            bookings=booking_list, employee_id=employee_id)
        self.on_match(matched_employee)

    def get_booking_by_employee_id(self, bookings: List[BookingEntity], employee_id: str) -> Union[BookingEntity, str]:
        for booking in bookings:
            if booking.employee_id == employee_id:
                return booking
        return employee_id
