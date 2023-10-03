from ....domain.services.synchronizer.booking_sqs_repository import BookingChangeFunc, BookingSqsRepository
from ....data.services.synchronizer.datasource.remote.booking_sqs_remote_datasource import BookingSqsRemoteDatasource


class BookingSqsRepositoryImpl(BookingSqsRepository):
    def __init__(self, booking_sqs_remote_datasource: BookingSqsRemoteDatasource) -> None:
        super().__init__()
        self.booking_sqs_remote_datasource = booking_sqs_remote_datasource

    def start(self, on_booking_change: BookingChangeFunc):
        self.booking_sqs_remote_datasource.start(
            on_booking_change=on_booking_change)

    def stop(self):
        self.booking_sqs_remote_datasource.stop()
