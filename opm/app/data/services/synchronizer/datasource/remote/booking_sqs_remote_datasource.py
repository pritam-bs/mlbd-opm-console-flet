from typing import Callable, Dict, List
from ......data.synchronizer.sqs_client import SqsClient, BookingUpdateFunc
from ......data.model.synchronizer.booking_update_dto import BookingUpdateListDTO


class BookingSqsRemoteDatasource:
    def __init__(self, sqs_client: SqsClient) -> None:
        self.sqs_client = sqs_client

    async def start(self, on_booking_update: BookingUpdateFunc):
        await self.sqs_client.start_booking_update_listener(
            on_booking_update=on_booking_update)

    async def delete_messages(self, receipt_handle_list: List[str]):
        await self.sqs_client.delete_booking_update_messages(receipt_handle_list=receipt_handle_list)

    def stop(self):
        self.sqs_client.stop_booking_update_listener()
