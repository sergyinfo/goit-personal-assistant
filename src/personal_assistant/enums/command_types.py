"""
This module contains the enums for the command types and entity types.
"""
from enum import Enum

class Command(Enum):
    """
    Enum class for command types
    """
    ADD = "add"
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
    ARCHIVE = "archive"
    RESTORE = "restore"
    VIEW_ACTIVE = "view_active"
    VIEW_ARCHIVED = "view_archived"
    VIEW_HISTORY = "view_history"

class Argument(Enum):
    """
    Enum class for argument types
    """
    ID = "id"
    NAME = "name"
    BIRTHDAY = "birthday"
    NOTE = "note"
    QUERY = "q"
    BY = "by"
    PHONE = "phone"
    EMAIL = "email"
    ADDRESS = "address"
    TAG = "tag"
    DAYS = "days"

class HelpText(Enum):
    """
    Enum class for help text strings
    """
    CONTACT_COMMANDS = 'Команди для керування контактами'
    LIST = 'Показати всі контакти'
    ADD = 'Додати контакт'
    EDIT = 'Редагувати контакт'
    DELETE = 'Видалити контакт'
    SEARCH = 'Пошук контактів'
    ADD_PHONE = 'Додати телефонний номер'
    DELETE_PHONE = 'Видалити телефонний номер'
    ADD_EMAIL = 'Додати електронну адресу'
    DELETE_EMAIL = 'Видалити електронну адресу'
    ADD_ADDRESS = 'Додати адресу'
    DELETE_ADDRESS = 'Видалити адресу'
    ADD_TAG = 'Додати тег до контакта'
    DELETE_TAG = 'Видалити тег з контакта'
    ANIVERSARIES = 'Показати наближені дні народження'
    
    ARGUMENT_ID = 'ID контакта для редагування'
    ARGUMENT_NAME = 'Ім\'я контакту'
    ARGUMENT_BIRTHDAY = 'Дата народження'
    ARGUMENT_NOTE = 'Примітка'
    ARGUMENT_QUERY = 'Фраза для пошуку'
    ARGUMENT_BY = 'Поле для пошуку (name, email, phone, address, tag, birthday, any)'
    ARGUMENT_PHONE = 'Телефонний номер'
    ARGUMENT_EMAIL = 'Електронна адреса'
    ARGUMENT_ADDRESS = 'Адреса'
    ARGUMENT_TAG = 'Тег для додавання'
    ARGUMENT_DAYS = 'Період в днях (7 за замовчуванням)'

class Messages(Enum):
    """
    Enum class for messages
    """
    CONTACT_ADDED = "Контакт {0} успішно додано з ID {1}"
    CONTACT_UPDATED = "Контакт {0} успішно оновлено"
    CONTACT_DELETED = "Контакт {0} успішно видалено"
    CONTACT_NOT_FOUND = "Контакт з ID {0} не знайдено"
    NO_PARAMETERS_FOR_EDITING = "Не вказано жодного параметру для редагування"
    CONTACTS_NOT_FOUND = "Контакти не знайдено"
    PHONE_ADDED = "Телефонний номер {0} успішно додано до контакту {1}"
    PHONE_DELETED = "Телефонний номер {0} успішно видалено з контакту {1}"
    EMAIL_ADDED = "Електронну адресу {0} успішно додано до контакту {1}"
    EMAIL_DELETED = "Електронну адресу {0} успішно видалено з контакту {1}"
    TAG_ADDED = "Тег {0} успішно додано до контакту {1}"
    TAG_DELETED = "Тег {0} успішно видалено з контакту {1}"
    ADDRESS_ADDED = "Адреса {0} успішно додано до контакту {1}"
    ADDRESS_DELETED = "Адреса {0} успішно видалено з контакту {1}"
    NO_ADDRESS_BOOK_FOUND = "No address book found. Creating a new one."
    ERROR_LOADING_ADDRESS_BOOK = "An error occurred while loading the address book: {0}"


class Entity(Enum):
    """
    Enum class for entity types as a top level commands
    """
    CONTACT = "contacts"
    NOTE = "notes"
