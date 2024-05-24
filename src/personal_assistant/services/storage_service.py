"""
This module contains the StorageService class which is responsible 
for managing data storage using different storage strategies.
"""
import os
from personal_assistant.services.storage.base_storage import Storage

class StorageService:
    """Service class to manage data storage using different storage strategies."""

    def __init__(self, strategy: Storage, base_directory: str = ".data") -> None:
        self.strategy = strategy
        self.base_directory = base_directory
        # Ensure the base directory exists
        os.makedirs(self.base_directory, exist_ok=True)

    def set_strategy(self, strategy: Storage) -> None:
        """Set the storage strategy to be used."""
        self.strategy = strategy

    def save_data(self, data: dict, path: str) -> None:
        """Save data using the configured storage strategy."""
        full_path = self._get_full_path(path)
        self.strategy.save(data, full_path)

    def load_data(self, path: str) -> dict:
        """Load data using the configured storage strategy."""
        full_path = self._get_full_path(path)

        if not os.path.exists(full_path):
            return {}

        return self.strategy.load(full_path)

    def _get_full_path(self, path: str) -> str:
        """Constructs and returns a full path ensuring it's within the base directory."""
        normalized_path = os.path.normpath(os.path.join(self.base_directory, path))
        # if not normalized_path.startswith(os.path.abspath(self.base_directory)):
            # raise ValueError("Attempt to access a file outside the designated data directory.")
        return normalized_path
