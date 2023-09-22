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
