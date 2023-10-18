from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8', extra="ignore")
    opm_base_url: str = Field(alias="OPM_BASE_URL")
    app_directory: str = Field(alias="APP_DIR")
    db_directory: str = Field(alias="DB_DIR")
    db_pin: int = Field(alias="DB_PIN")
    db_name: str = Field(alias="DB_NAME")
    log_file_name: str = Field(alias="LOG_FILE_NAME")
    knn_directory: str = Field(alias="KNN_DIR")
    local_knn_model: str = Field(alias="LOCAL_KNN_MODEL")
    local_index_map: str = Field(alias="LOCAL_INDEX_MAP")
    aws_sqs_access_key: str = Field(alias="AWS_SQS_ACCESS_KEY")
    aws_sqs_secret_access_key: str = Field(alias="AWS_SQS_SECRET_ACCESS_KEY")
    aws_sqs_region_name: str = Field(alias="AWS_SQS_REGION_NAME")
    booking_change_queue_name: str = Field(alias="BOOKING_CHANGE_QUEUE_NAME")
    knn_model_change_queue_name: str = Field(alias="MODEL_CHANGE_QUEUE_NAME")
    booking_change_wait_seconds: int = Field(
        alias="BOOKING_CHANGE_WAIT_SECONDS")
    knn_model_change_wait_seconds: int = Field(
        alias="MODEL_CHANGE_WAIT_SECONDS")

    aws_s3_access_key: str = Field(alias="AWS_S3_ACCESS_KEY")
    aws_s3_secret_access_key: str = Field(alias="AWS_S3_SECRET_KEY")
    aws_s3_bucket_name: str = Field(alias="AWS_S3_BUCKET_NAME")
    aws_s3_knn_model_key: str = Field(alias="AWS_S3_KNN_MODEL_KEY")
    aws_s3_index_map_key: str = Field(alias="AWS_S3_INDEX_MAP_KEY")


environment = os.getenv("APP_ENV")

settings = None
if environment == "dev":
    # Create an instance of Settings for dev
    settings = Settings(
        _env_file='opm/app/settings/dev.env')
elif environment == "prod":
    # Create an instance of Settings for prod
    settings = Settings(
        _env_file='opm/app/settings/prod.env')
else:
    raise ValueError("Invalid environment specified")
