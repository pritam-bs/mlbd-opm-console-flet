from opm.app.data.model.synchronizer.booking_change_dto import BookingChangeDTO
from ....domain.services.synchronizer.booking_sqs_repository import BookingChangeFunc, BookingSqsRepository
from ....data.services.synchronizer.datasource.remote.booking_sqs_remote_datasource import BookingSqsRemoteDatasource
from ....domain.services.synchronizer.booking_change_dto_remapper import BookingChangeRemapper


class BookingSqsRepositoryImpl(BookingSqsRepository):
    def __init__(self, booking_sqs_remote_datasource: BookingSqsRemoteDatasource) -> None:
        super().__init__()
        self.booking_sqs_remote_datasource = booking_sqs_remote_datasource

    async def start(self, on_booking_change: BookingChangeFunc):
        self.on_booking_change = on_booking_change
        await self.booking_sqs_remote_datasource.start(
            on_booking_change=self.booking_change_callback)

    def stop(self):
        self.booking_sqs_remote_datasource.stop()

    def booking_change_callback(self, booking_chnage_dto: BookingChangeDTO):
        booking_chnage_entity = BookingChangeRemapper.map_from(
            booking_change_dto=booking_chnage_dto)
        self.on_booking_change(booking_chnage_entity)
