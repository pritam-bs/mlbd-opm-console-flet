from opm.app.data.model.synchronizer.booking_update_dto import BookingUpdateListDTO
from ....domain.services.synchronizer.booking_sqs_repository import BookingUpdateFunc, BookingSqsRepository
from ....data.services.synchronizer.datasource.remote.booking_sqs_remote_datasource import BookingSqsRemoteDatasource
from .booking_update_dto_remapper import BookingUpdateRemapper


class BookingSqsRepositoryImpl(BookingSqsRepository):
    def __init__(self, booking_sqs_remote_datasource: BookingSqsRemoteDatasource) -> None:
        super().__init__()
        self.booking_sqs_remote_datasource = booking_sqs_remote_datasource

    async def start(self, on_booking_update: BookingUpdateFunc):
        self.on_booking_update = on_booking_update
        await self.booking_sqs_remote_datasource.start(
            on_booking_update=self.booking_update_callback)

    def stop(self):
        self.booking_sqs_remote_datasource.stop()

    async def booking_update_callback(self, booking_update_list_dto: BookingUpdateListDTO):
        booking_update_entity = BookingUpdateRemapper.map_sqs_dto(
            booking_update_list_dto=booking_update_list_dto)
        await self.on_booking_update(booking_update_entity)
