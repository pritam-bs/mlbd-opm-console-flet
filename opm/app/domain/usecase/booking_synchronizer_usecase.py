from typing import List
from ...domain.services.synchronizer.booking_sqs_repository import BookingSqsRepository, BookingUpdateFunc


class BookingSynchronizerUsecase:
    def __init__(self, booking_sqs_repository: BookingSqsRepository) -> None:
        self.booking_sqs_repository = booking_sqs_repository

    async def start(self, on_booking_update: BookingUpdateFunc):
        await self.booking_sqs_repository.start(on_booking_update=on_booking_update)

    async def delete_message(self, receipt_handle_list: List[str]):
        await self.booking_sqs_repository.delete_messages(receipt_handle_list=receipt_handle_list)

    def stop(self):
        self.booking_sqs_repository.stop()
