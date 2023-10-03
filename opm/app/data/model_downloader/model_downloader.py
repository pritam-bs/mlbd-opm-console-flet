from aiobotocore.session import get_session
from botocore.exceptions import (
    ClientError,
    NoCredentialsError,
    PartialCredentialsError,

)

from asyncio import TimeoutError, sleep, gather
from pathlib import Path
from ...settings.settings import settings
from loguru import logger
from typing import Callable

CallbackFunc = Callable[[str, bool], None]


class ModelDownloader:
    MAX_RETRIES = 3
    RETRY_DELAY = 5

    def __init__(self) -> None:
        self.aws_access_key_id = settings.aws_access_key_id
        self.aws_secret_access_key = settings.aws_secret_access_key
        self.region_name = settings.region_name

    async def _download_file_from_s3(self, bucket_name: str, s3_key: str, local_path: str, callback: CallbackFunc):
        for attempt in range(self.MAX_RETRIES):
            try:
                session = get_session()
                async with session.create_client('s3') as s3:
                    response = await s3.get_object(Bucket=bucket_name, Key=s3_key)
                    async with response['Body'] as stream:
                        with open(local_path, 'wb') as file:
                            while True:
                                # reading 1MB chunk
                                chunk = await stream.read(1024*1024)
                                if not chunk:
                                    break
                                file.write(chunk)

                callback(s3_key, True)
                return
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'NoSuchBucket':
                    logger.debug(
                        f"The specified bucket {bucket_name} does not exist.")
                elif error_code == 'NoSuchKey':
                    logger.debug(f"The specified key {s3_key} does not exist.")
                elif error_code in ['InvalidAccessKeyId', 'SignatureDoesNotMatch']:
                    logger.debug("Invalid AWS credentials provided.")
                elif error_code == 'AccessDenied':
                    logger.debug("Access denied for the given bucket/key.")
                else:
                    logger.debug(f"An S3 error occurred: {e}")
            except NoCredentialsError:
                logger.debug("No credentials could be found.")
            except PartialCredentialsError:
                logger.debug("Incomplete or partial credentials provided.")
            except IOError:
                logger.debug(
                    f"Failed to write the file to {local_path}. Check if disk is full or check permissions.")
            except TimeoutError:
                logger.debug(f"Timed out while trying to download {s3_key}.")
                if attempt < self.MAX_RETRIES - 1:  # i.e. not on the last attempt
                    logger.debug(
                        f"Attempt {attempt+1} failed. Retrying in {self.RETRY_DELAY} seconds...")
                    await sleep(self.RETRY_DELAY)
                else:
                    logger.debug(
                        f"Failed to download {s3_key} after {self.MAX_RETRIES} attempts. Last error: {str(e)}")
                    callback(s3_key, False)
            except Exception as e:
                logger.debug(f"An unexpected error occurred: {str(e)}")

    def _ensure_model_dir(self) -> Path:
        model_dir = Path.home() / settings.app_directory / settings.knn_directory
        if not model_dir.exists():
            model_dir.mkdir(parents=True)
        return model_dir

    async def download_models(self, callback: CallbackFunc):
        local_model_dir = self._ensure_model_dir()
        bucket_name = settings.bucket_name
        knn_model_s3_key = settings.knn_model
        index_map_s3_key = settings.index_map
        knn_model_local_path = local_model_dir / knn_model_s3_key
        index_map_local_path = local_model_dir / index_map_s3_key
        files_to_download = {
            knn_model_s3_key: str(knn_model_local_path),
            index_map_s3_key: str(index_map_local_path)
        }

        await gather(
            *[self._download_file_from_s3(bucket_name, s3_key, local_path, callback)
              for s3_key, local_path in files_to_download.items()]
        )
