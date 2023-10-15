from typing import Callable, Dict
from ......data.synchronizer.sqs_client import SqsClient

# Define a type alias for the callable
BookingChangeFunc = Callable[[Dict], None]


class BookingSqsRemoteDatasource:
    def __init__(self, sqs_client: SqsClient) -> None:
        self.sqs_client = sqs_client

    async def start(self, on_booking_change: BookingChangeFunc):
        await self.sqs_client.start_booking_change_listener(
            on_booking_change=on_booking_change)

    def stop(self):
        self.sqs_client.stop_booking_change_listener()
