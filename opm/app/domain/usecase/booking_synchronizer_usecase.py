from ...domain.services.synchronizer.booking_sqs_repository import BookingSqsRepository, BookingUpdateFunc


class BookingSynchronizerUsecase:
    def __init__(self, booking_sqs_repository: BookingSqsRepository) -> None:
        self.booking_sqs_repository = booking_sqs_repository

    async def start(self, on_booking_update: BookingUpdateFunc):
        await self.booking_sqs_repository.start(on_booking_update=on_booking_update)

    def stop(self):
        self.booking_sqs_repository.stop()
