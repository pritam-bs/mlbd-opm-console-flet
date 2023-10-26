from aiobotocore.session import get_session
from botocore.exceptions import (
    ClientError,
    NoCredentialsError,
    PartialCredentialsError,

)
import aiofiles

from asyncio import TimeoutError, sleep, gather
from pathlib import Path
from ...settings.settings import settings
from loguru import logger
from typing import Callable

CallbackFunc = Callable[[bool], None]


class ModelDownloader:
    MAX_RETRIES = 3
    RETRY_DELAY = 5

    def __init__(self) -> None:
        self.aws_access_key = settings.aws_s3_access_key
        self.aws_secret_key = settings.aws_s3_secret_access_key
        self.region_name = settings.aws_sqs_region_name

    async def _download_file_from_s3(self, bucket_name: str, s3_key: str, local_path: str):
        for attempt in range(self.MAX_RETRIES):
            try:
                session = get_session()
                async with session.create_client('s3', region_name=self.region_name,
                                                 aws_access_key_id=self.aws_access_key,
                                                 aws_secret_access_key=self.aws_secret_key) as s3:

                    response = await s3.get_object(Bucket=bucket_name, Key=s3_key)
                    async with aiofiles.open(local_path, 'wb') as file:
                        async for chunk in response['Body'].iter_chunks():
                            await file.write(chunk)
                return True
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
                return False
            except NoCredentialsError:
                logger.debug("No credentials could be found.")
                return False
            except PartialCredentialsError:
                logger.debug("Incomplete or partial credentials provided.")
                return False
            except IOError:
                logger.debug(
                    f"Failed to write the file to {local_path}. Check if disk is full or check permissions.")
                return False
            except TimeoutError:
                logger.debug(f"Timed out while trying to download {s3_key}.")
                if attempt < self.MAX_RETRIES - 1:  # i.e. not on the last attempt
                    logger.debug(
                        f"Attempt {attempt+1} failed. Retrying in {self.RETRY_DELAY} seconds...")
                    await sleep(self.RETRY_DELAY)
                else:
                    logger.debug(
                        f"Failed to download {s3_key} after {self.MAX_RETRIES} attempts. Last error: {str(e)}")
                    return False
            except Exception as e:
                logger.debug(f"An unexpected error occurred: {str(e)}")
                return False

    def _ensure_model_dir(self) -> Path:
        model_dir = Path.home() / settings.app_directory / settings.knn_directory
        if not model_dir.exists():
            model_dir.mkdir(parents=True)
        return model_dir

    async def download_models(self, callback: CallbackFunc):
        local_model_dir = self._ensure_model_dir()
        bucket_name = settings.aws_s3_bucket_name
        knn_model_s3_key = settings.aws_s3_knn_model_key
        index_map_s3_key = settings.aws_s3_index_map_key
        knn_model_local_path = local_model_dir / settings.local_knn_model
        index_map_local_path = local_model_dir / settings.local_index_map
        files_to_download = {
            knn_model_s3_key: str(knn_model_local_path),
            index_map_s3_key: str(index_map_local_path)
        }

        successful_downloads = []  # Keep track of successful downloads

        async def download_and_track_success(s3_key, local_path):
            nonlocal successful_downloads
            try:
                is_success = await self._download_file_from_s3(bucket_name, s3_key, local_path)
                if is_success:
                    successful_downloads.append(s3_key)
            except Exception as e:
                logger.debug(f"Failed to download {s3_key}: {str(e)}")

        # Use asyncio.gather to concurrently download files and track successful ones
        await gather(
            *[download_and_track_success(s3_key, local_path) for s3_key, local_path in files_to_download.items()]
        )

        # Call the callback function only if all downloads were successful
        if len(successful_downloads) == len(files_to_download):
            await callback(True)
        else:
            await callback(False)
