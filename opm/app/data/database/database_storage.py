from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict


class DatabaseStorage(ABC):
    """Abstract class for database storage"""

    def __init__(
        self,
    ):
        super().__init__()

    @abstractmethod
    def initialize_database(self):
        """Initialize database"""
        pass

    @abstractmethod
    def reset_database(self):
        """
        Delete the database.
        """
        pass

    @abstractmethod
    def insert(self, data: Dict) -> Dict:
        """Insert data to database"""
        pass

    @abstractmethod
    def update(self, data: Dict, updated_data: Dict) -> Dict:
        """Update data"""
        pass

    @abstractmethod
    def delete(self, data: Dict) -> Dict:
        """Delete data from database"""
        pass

    @abstractmethod
    def exists(self, data: Dict) -> bool:
        """Check data exists or not"""
        pass

    @abstractmethod
    def find(self, data: Dict) -> Dict:
        """Find data in database"""
        pass
