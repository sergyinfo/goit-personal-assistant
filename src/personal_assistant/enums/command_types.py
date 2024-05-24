"""
This module contains the enums for the command types and entity types.
"""
from enum import Enum

class Command(Enum):
    """
    Enum class for command types
    """
    ADD = "+"
    EDIT = "edit"
    DELETE = "delete"
    SEARCH = "search"
    LIST = "list"
    ADD_PHONE = "add_phone"
    DELETE_PHONE = "delete_phone"
    ADD_EMAIL = "add_email"
    DELETE_EMAIL = "delete_email"
    ADD_ADDRESS = "add_address"
    DELETE_ADDRESS = "delete_address"
    UPCOMING_BIRTHDAY = "upcoming_birthday"
    ADD_TAG = "add_tag"
    DELETE_TAG = "delete_tag"
    ANIVERSARIES = "aniversaries"

class Entity(Enum):
    """
    Enum class for entity types as a top level commands
    """
    CONTACT = "contacts"
    NOTE = "notes"
