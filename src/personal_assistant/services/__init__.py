"""
This module is a package that contains all the services used by the personal assistant.
"""
from personal_assistant.services.storage_service import StorageService
from personal_assistant.services.tag_manager import TagManagerService
from personal_assistant.services.notebook import Notebook
from personal_assistant.services.address_book import AddressBook

__all__ = [ 'StorageService', 'TagManagerService', 'Notebook', 'AddressBook']
