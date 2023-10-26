from ...data.model.synchronizer.booking_update_dto import BookingUpdateListDTO
from ...data.model.synchronizer.model_update_dto import ModelUpdateDTO
from ...settings.settings import settings
from aiobotocore.session import get_session
from aiobotocore.session import AioSession
import botocore.exceptions
from typing import Callable, Dict, List, Optional
from loguru import logger
import json
import asyncio

# Define a type alias for the callable
BookingUpdateFunc = Callable[[BookingUpdateListDTO, List[str]], None]
ModelUpdateFunc = Callable[[ModelUpdateDTO, List[str]], None]


class SqsClient:

    def __init__(self) -> None:
        self.aws_access_key_id = settings.aws_sqs_access_key
        self.aws_secret_access_key = settings.aws_sqs_secret_access_key
        self.region_name = settings.aws_sqs_region_name
        self.model_change_queue_name = settings.knn_model_change_queue_name
        self.booking_change_queue_name = settings.booking_change_queue_name
        self.model_listen_interval = settings.knn_model_listen_interval
        self.booking_listen_interval = settings.booking_listen_interval

    async def start_booking_update_listener(
        self,
        on_booking_update: Optional[BookingUpdateFunc]
    ):

        self.booking_update_listener = BookingUpdateListener(
            on_booking_update=on_booking_update,
            queue_name=self.booking_change_queue_name,
            aws_access_key=self.aws_access_key_id,
            aws_secret_key=self.aws_secret_access_key,
            region_name=self.region_name,
            interval=self.booking_listen_interval
        )
        await self.booking_update_listener.listen()

    async def start_model_update_listener(
        self,
        on_model_update: Optional[ModelUpdateFunc]
    ):
        self.model_update_listener = ModelUpdateListener(
            on_model_update=on_model_update,
            queue_name=self.model_change_queue_name,
            aws_access_key=self.aws_access_key_id,
            aws_secret_key=self.aws_secret_access_key,
            region_name=self.region_name,
            interval=self.model_listen_interval
        )

        await self.model_update_listener.listen()

    def stop_booking_update_listener(self):
        self.booking_update_listener.stop_listening()
        self.booking_update_listener = None

    def stop_model_update_listener(self):
        self.model_update_listener.stop_listening()
        self.model_update_listener = None

    async def delete_booking_update_messages(self, receipt_handle_list: List[str]):
        await self.booking_update_listener.delete_messages(
            receipt_handle_list=receipt_handle_list)

    async def delete_model_update_messages(self, receipt_handle_list: List[str]):
        await self.model_update_listener.delete_messages(
            receipt_handle_list=receipt_handle_list)


class AsyncSqsListener:

    def __init__(
            self, queue_name,
            aws_access_key,
            aws_secret_key,
            region_name,
            interval
    ):
        self.queue_name = queue_name
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region_name = region_name
        self.interval = interval
        self.is_polling = False

    def __del__(self):
        logger.debug("AsyncSqsListener del")
        self.is_polling = False

    async def listen(self):
        session = get_session()
        async with session.create_client('sqs', region_name=self.region_name,
                                         aws_access_key_id=self.aws_access_key,
                                         aws_secret_access_key=self.aws_secret_key) as client:
            try:
                message_response = await client.get_queue_url(QueueName=self.queue_name)
            except botocore.exceptions.ClientError as err:
                if (
                    err.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue'
                ):
                    logger.debug(f"Queue {self.queue_name} does not exist")
                else:
                    logger.debug(err)
                return

            queue_url = message_response['QueueUrl']
            self.is_polling = True
            while self.is_polling:
                message_response = await client.receive_message(
                    QueueUrl=queue_url,
                    AttributeNames=['MessageGroupId'],
                    MaxNumberOfMessages=10
                )
                messages = message_response.get('Messages', [])
                message_bodies = []
                receipt_handle_list = []
                for message in messages:
                    if message.get('Attributes', {}).get('MessageGroupId') == "error-opm-face-registration":
                        continue
                    receipt_handle = message['ReceiptHandle']
                    message_body = message['Body']
                    try:
                        data_dict = json.loads(message_body)
                        message_bodies.append(data_dict)
                        receipt_handle_list.append(receipt_handle)
                    except Exception as err:
                        logger.debug(err)
                if len(message_bodies) > 0:
                    await self.handle_messages(message_bodies, receipt_handle_list)
                await asyncio.sleep(self.interval)

    async def handle_messages(self, messages, receipt_handle_list):
        raise NotImplementedError

    def stop_listening(self):
        self.is_polling = False

    async def delete_messages(self, receipt_handle_list: List[str]):
        session = get_session()
        async with session.create_client('sqs', region_name=self.region_name,
                                         aws_access_key_id=self.aws_access_key,
                                         aws_secret_access_key=self.aws_secret_key) as client:
            try:
                message_response = await client.get_queue_url(QueueName=self.queue_name)
            except botocore.exceptions.ClientError as err:
                if (
                    err.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue'
                ):
                    logger.debug(f"Queue {self.queue_name} does not exist")
                else:
                    logger.debug(err)
                return

            queue_url = message_response['QueueUrl']
            try:
                for receipt_handle in receipt_handle_list:
                    await client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
            except Exception as err:
                logger.debug(err)


class ModelUpdateListener(AsyncSqsListener):
    def __init__(self, on_model_update: Optional[ModelUpdateFunc], **kwargs):
        super().__init__(**kwargs)
        self.on_model_update = on_model_update

    async def handle_messages(self, messages, receipt_handle_list):
        if self.on_model_update:
            model_change_dto = ModelUpdateDTO.from_dict(dict=messages)
            self.on_model_update(model_change_dto, receipt_handle_list)


class BookingUpdateListener(AsyncSqsListener):
    def __init__(self, on_booking_update: Optional[BookingUpdateFunc], **kwargs):
        super().__init__(**kwargs)
        self.on_booking_update = on_booking_update

    async def handle_messages(self, messages, receipt_handle_list):
        if self.on_booking_update:
            booking_change_dto = BookingUpdateListDTO.from_dict(data=messages)
            await self.on_booking_update(booking_change_dto, receipt_handle_list)
