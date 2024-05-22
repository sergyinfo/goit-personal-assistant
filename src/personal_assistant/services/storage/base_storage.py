"""
Module for the base storage class.
"""
from abc import ABC, abstractmethod

class Storage(ABC):
    """Abstract base class for storage strategies."""

    @abstractmethod
    def save(self, data: dict, path: str) -> None:
        """Save data to the specified path."""
        pass

    @abstractmethod
    def load(self, path: str) -> dict:
        """Load data from the specified path."""
        pass
