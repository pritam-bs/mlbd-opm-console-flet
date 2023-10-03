from ...domain.services.synchronizer.booking_sqs_repository import BookingSqsRepository, BookingChangeFunc


class BookingSynchronizerUsecase:
    def __init__(self, booking_sqs_repository: BookingSqsRepository) -> None:
        self.booking_sqs_repository = booking_sqs_repository

    def start(self, on_booking_change: BookingChangeFunc):
        self.booking_sqs_repository.start(on_booking_change=on_booking_change)

    def stop(self):
        self.booking_sqs_repository.stop()
