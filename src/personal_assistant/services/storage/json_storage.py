"""
This module contains the JsonStorage class, which is a subclass of the Storage class.
"""
import json
from .base_storage import Storage

class JsonStorage(Storage):
    """Storage strategy for JSON format."""

    def save(self, data: dict, path: str) -> None:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except IOError as e:
            raise IOError(f"Failed to save data to {path}: {e}")

    def load(self, path: str) -> dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Data in {path} is not valid JSON: {e}")
        except IOError as e:
            raise IOError(f"Failed to load data from {path}: {e}")
