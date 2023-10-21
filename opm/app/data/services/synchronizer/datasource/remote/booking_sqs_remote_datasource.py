from typing import Callable, Dict
from ......data.synchronizer.sqs_client import SqsClient
from ......data.model.synchronizer.booking_update_dto import BookingUpdateListDTO

# Define a type alias for the callable
BookingUpdateFunc = Callable[[BookingUpdateListDTO], None]


class BookingSqsRemoteDatasource:
    def __init__(self, sqs_client: SqsClient) -> None:
        self.sqs_client = sqs_client

    async def start(self, on_booking_update: BookingUpdateFunc):
        await self.sqs_client.start_booking_update_listener(
            on_booking_update=on_booking_update)

    def stop(self):
        self.sqs_client.stop_booking_update_listener()
