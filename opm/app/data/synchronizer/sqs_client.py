from ...settings.settings import settings
from sqs_listener import SqsListener
from typing import Callable, Dict, Optional

from loguru import logger

# Define a type alias for the callable
BookingChangeFunc = Callable[[Dict], None]
ModelChangeFunc = Callable[[Dict], None]


class SqsClient:

    def __init__(self) -> None:
        self.aws_access_key_id = settings.aws_access_key_id
        self.aws_secret_access_key = settings.aws_secret_access_key
        self.region_name = settings.region_name
        self.queue_name = settings.queue_name
        self.on_booking_change = None
        self.on_model_change = None

    def start_booking_change_listener(
        self,
        on_booking_change: Optional[BookingChangeFunc]
    ):

        self.booking_change_listener = BookingChangeListener(
            queue=self.queue_name,
            on_booking_change=self.on_booking_change,
            aws_access_key=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )
        self.on_booking_change = on_booking_change
        self.booking_change_listener.listen()

    def start_model_change_listener(
        self,
        on_model_change: Optional[ModelChangeFunc]
    ):
        self.model_change_listener = ModelChangeListener(
            queue=self.queue_name,
            on_model_change=self.on_model_change,
            aws_access_key=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )

        self.on_model_change = on_model_change
        self.model_change_listener.listen()

    def stop_booking_change_listener(self):
        self.on_booking_change = None
        self.booking_change_listener = None

    def stop_model_change_listener(self):
        self.on_model_change = None
        self.model_change_listener = None


class ModelChangeListener(SqsListener):
    def __init__(self, queue, on_model_change: Optional[ModelChangeFunc], **kwargs):
        super().__init__(queue, **kwargs)
        self.on_model_change = on_model_change

    def handle_message(self, body, attributes, messages_attributes):
        if self.on_model_change:
            self.on_model_change(body)


class BookingChangeListener(SqsListener):
    def __init__(self, queue, on_booking_change: Optional[ModelChangeFunc], **kwargs):
        super().__init__(queue, **kwargs)
        self.on_booking_change = on_booking_change

    def handle_message(self, body, attributes, messages_attributes):
        if self.on_booking_change:
            self.on_booking_change(body)
