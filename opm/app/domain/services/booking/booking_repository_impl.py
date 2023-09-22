from ....domain.entities.booking_entity import BookingEntity
from ....domain.services.booking.booking_repository import BookingRepository
from ....data.services.booking.data_source.remote.booking_remore_datasource import BookingRemoteDatasource
from ....data.model.error.response_error import ResponseError
from ....domain.services.booking.booking_dto_remapper import BookingRemapper
from typing import Union, List
from ....domain.error.app_error import AppException


class BookingRepositoryImpl(BookingRepository):
    def __init__(self, booking_remote_datasource: BookingRemoteDatasource, booking_remapper: BookingRemapper):
        self.booking_remote_datasource = booking_remote_datasource
        self.booking_remapper = booking_remapper

    def get_all_bookings(self) -> List[BookingEntity]:
        try:
            response = self.booking_remote_datasource.get_all_bookings()
            booking_entities = BookingRemapper.map_network_dto(
                booking_dto=response)
            return booking_entities
        except ResponseError as response_error:
            raise AppException.from_response_error(response_error)
