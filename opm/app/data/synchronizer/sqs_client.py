import asyncio
from ...data.model.synchronizer.booking_change_dto import BookingChangeDTO
from ...data.model.synchronizer.model_change_dto import ModelChangeDTO
from ...settings.settings import settings
from aiobotocore.session import get_session
from aiobotocore.session import AioSession
import botocore.exceptions
from typing import Callable, Dict, Optional
from loguru import logger
import datetime

# Define a type alias for the callable
BookingChangeFunc = Callable[[Dict], None]
ModelChangeFunc = Callable[[Dict], None]


class SqsClient:

    def __init__(self) -> None:
        self.aws_access_key_id = settings.aws_access_key_id
        self.aws_secret_access_key = settings.aws_secret_access_key
        self.region_name = settings.region_name
        self.model_change_queue_name = settings.knn_model_change_queue_name
        self.booking_change_queue_name = settings.booking_change_queue_name
        self.model_wait_time_seconds = settings.knn_model_change_wait_seconds
        self.booking_wait_time_seconds = settings.booking_change_wait_seconds

    async def start_booking_change_listener(
        self,
        on_booking_change: Optional[BookingChangeFunc]
    ):

        self.booking_change_listener = BookingChangeListener(
            queue_name=self.booking_change_queue_name,
            on_booking_change=on_booking_change,
            aws_access_key=self.aws_access_key_id,
            aws_secret_key=self.aws_secret_access_key,
            region_name=self.region_name,
            wait_time_seconds=self.booking_wait_time_seconds
        )
        await self.booking_change_listener.listen()

    async def start_model_change_listener(
        self,
        on_model_change: Optional[ModelChangeFunc]
    ):
        self.model_change_listener = ModelChangeListener(
            queue_name=self.model_change_queue_name,
            on_model_change=on_model_change,
            aws_access_key=self.aws_access_key_id,
            aws_secret_key=self.aws_secret_access_key,
            region_name=self.region_name,
            wait_time_seconds=self.model_wait_time_seconds
        )

        await self.model_change_listener.listen()

    def stop_booking_change_listener(self):
        self.booking_change_listener.stop_listening()
        self.booking_change_listener = None

    def stop_model_change_listener(self):
        self.model_change_listener.stop_listening()
        self.model_change_listener = None


class AsyncSqsListener:

    def __init__(
            self, queue_name,
            aws_access_key,
            aws_secret_key,
            region_name,
            wait_time_seconds
    ):
        self.queue_name = queue_name
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region_name = region_name
        self.wait_time_seconds = wait_time_seconds
        self.is_polling = False

    async def listen(self):
        session = get_session()
        async with session.create_client('sqs', region_name=self.region_name,
                                         aws_access_key_id=self.aws_access_key,
                                         aws_secret_access_key=self.aws_secret_key) as client:
            try:
                response = await client.get_queue_url(QueueName=self.queue_name)
            except botocore.exceptions.ClientError as err:
                if (
                    err.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue'
                ):
                    logger.debug(f"Queue {self.queue_name} does not exist")
                else:
                    logger.debug(err)
                return

            queue_url = response['QueueUrl']
            self.is_polling = True
            while self.is_polling:  # Continuous polling
                response = await client.receive_message(
                    QueueUrl=queue_url,
                    WaitTimeSeconds=self.wait_time_seconds)
                messages = response.get('Messages', [])
                for message in messages:
                    receipt_handle = message['ReceiptHandle']
                    message_body = message['Body']

                    await self.handle_message(message_body)
                    try:
                        await client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
                    except Exception as err:
                        logger.debug(err)

    async def handle_message(self, message):
        raise NotImplementedError

    def stop_listening(self):
        self.is_polling = False


class ModelChangeListener(AsyncSqsListener):
    def __init__(self, on_model_change: Optional[ModelChangeFunc], **kwargs):
        super().__init__(**kwargs)
        self.on_model_change = on_model_change

    async def handle_message(self, message):
        if self.on_model_change:
            model_change_dto = ModelChangeDTO.from_json(json_data=message)
            self.on_model_change(model_change_dto)


class BookingChangeListener(AsyncSqsListener):
    def __init__(self, on_booking_change: Optional[BookingChangeFunc], **kwargs):
        super().__init__(**kwargs)
        self.on_booking_change = on_booking_change

    async def handle_message(self, message):
        if self.on_booking_change:
            booking_change_dto = BookingChangeDTO.from_json(json_data=message)
            self.on_booking_change(booking_change_dto)
