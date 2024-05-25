"""
This module contains enums for command types, arguments and help text.
"""
from enum import Enum

class Command(Enum):
    """
    Enum for command types
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
    Enum for argument types
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
    CONTENT = "content"
    SEARCH_CONTENT = "search_content"
    SEARCH_TAG = "search_tag"

class HelpText(Enum):
    """
    Enum for help text
    """
    CONTACT_COMMANDS = 'Команди для керування контактами'
    NOTE_COMMANDS = 'Команди для керування нотатками'
    
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
    ARGUMENT_CONTENT = 'Зміст нотатки'
    ARGUMENT_SEARCH_CONTENT = 'Текст для пошуку в нотатках'
    ARGUMENT_SEARCH_TAG = 'Тег для фільтрації нотаток'

    ADD_NOTE = 'Додати нотатку'
    EDIT_NOTE = 'Редагувати нотатку'
    DELETE_NOTE = 'Видалити нотатку'
    SEARCH_NOTE = 'Пошук нотаток'
    ADD_TAG_NOTE = 'Додати тег до нотатки'
    DELETE_TAG_NOTE = 'Видалити тег з нотатки'
    ARCHIVE_NOTE = 'Заархівувати нотатку'
    RESTORE_NOTE = 'Розархівувати нотатку'
    VIEW_ACTIVE_NOTES = 'Показати всі не заархівовані нотатки'
    VIEW_ARCHIVED_NOTES = 'Показати всі заархівовані нотатки'
    VIEW_HISTORY_NOTE = 'Переглянути історію нотатки'

class Messages(Enum):
    """
    Enum for messages
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

    NOTE_ADDED = "Note added: {0} | ID: {1}"
    NOTE_UPDATED = "Note {0} updated."
    NOTE_DELETED = "Note with ID {0} deleted."
    SEARCHING_NOTES = "Searching notes... Content: {0}, Tag: {1}, ID: {2}"
    FOUND_NOTES = "Found notes:"
    NO_NOTES_FOUND = "No notes found by your request."
    ADDING_TAG = "Adding tag {0} to note {1}"
    TAG_ADDED_TO_NOTE = "Tag {0} added to note {1}."
    DELETING_TAG = "Deleting tag {0} from note {1}"
    TAG_DELETED_FROM_NOTE = "Tag {0} removed from note {1}."
    NOTE_ARCHIVED = "Note {0} archived."
    NOTE_RESTORED = "Note with ID {0} restored."
    ACTIVE_NOTES = "Active notes:"
    NO_ACTIVE_NOTES = "No active notes found."
    ARCHIVED_NOTES = "Archived notes:"
    NO_ARCHIVED_NOTES = "No archived notes found."
    HISTORY_FOR_NOTE = "History for note with ID: {0}:"
    NO_HISTORY_FOR_NOTE = "No history found for note {0}."
    NOTE_NOT_FOUND = "Note {0} not found."
    LOADING_NOTEBOOK = "Loading notebook..."
    NO_NOTEBOOK_FOUND = "No notebook found. Creating a new one."
    ERROR_LOADING_NOTEBOOK = "An error occurred while loading the notebook: {0}"

class Entity(Enum):
    """
    Enum class for entity types as a top level commands
    """
    CONTACT = "contacts"
    NOTE = "notes"
