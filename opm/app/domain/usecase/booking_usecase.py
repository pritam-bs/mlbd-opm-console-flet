from ...domain.services.booking.booking_repository import BookingRepository
from typing import List, Union
from ...domain.entities.booking_entity import BookingEntity
from ...domain.error.app_error import AppException


class BookingUsecase:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    async def run(self) -> Union[List[BookingEntity], AppException]:
        return await self.booking_repository.get_all_bookings()
