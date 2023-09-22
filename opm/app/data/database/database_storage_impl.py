from ...data.database.database_storage import DatabaseStorage
from loguru import logger
from pathlib import Path
from datagoose import Datagoose
from typing import Dict
from ...settings.settings import settings


class DatabaseStorageImpl(DatabaseStorage):
    """Database storage implementation."""

    def __init__(self):
        # database config
        super().__init__()
        self.initialize_database()

    def initialize_database(self):
        logger.info("Initializing database")
        path = settings.db_directory
        name = settings.db_name
        pin = settings.db_pin
        self.database = Datagoose(name, {
            "PATH": path,
            "AUTO_SAVE": True,
            "USE_REGEX": True,
            "ENCRYPTED": True,
            "PIN": pin,
        })

    def reset_database(self):
        logger.info("Clearing database")
        self.database.clear()

    def insert(self, data: Dict) -> Dict:
        result = self.database.insert_one(data=data)
        return result

    def update(self, data: Dict, updated_data: Dict) -> Dict:
        return self.database.update_one(data=data, new_data=updated_data)

    def delete(self, data: Dict) -> Dict:
        return self.database.delete_one(data=data)

    def exists(self, data: Dict) -> bool:
        return self.database.exists(data=data)

    def find(self, data: Dict) -> Dict:
        return self.database.find_one(data=data)
