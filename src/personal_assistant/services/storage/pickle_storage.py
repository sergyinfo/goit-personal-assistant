"""
Pickle storage strategy.
"""
import pickle
from .base_storage import Storage

class PickleStorage(Storage):
    """Storage strategy for Pickle format."""

    def save(self, data: dict, path: str) -> None:
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load(self, path: str) -> dict:
        with open(path, 'rb') as f:
            return pickle.load(f)
