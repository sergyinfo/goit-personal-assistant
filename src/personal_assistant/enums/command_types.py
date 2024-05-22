"""
This module contains the enums for the command types and entity types.
"""
from enum import Enum

class Command(Enum):
    """
    Enum class for command types
    """
    ADD = "плюс"
    EDIT = "плюс_плюс"
    DELETE = "мінус"
    SEARCH = "search"
    LIST = "list"
    ADD_PHONE = "add-phone"
    DELETE_PHONE = "delete-phone"
    ADD_EMAIL = "add-email"
    DELETE_EMAIL = "delete-email"
    UPCOMING_BIRTHDAY = "upcoming-birthday"
    ADD_TAG = "add-tag"
    DELETE_TAG = "delete-tag"

class Entity(Enum):
    """
    Enum class for entity types as a top level commands
    """
    CONTACT = "contacts"
    NOTE = "notes"
