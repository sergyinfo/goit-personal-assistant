"""
This module contains enums for command types, arguments and help text.
"""
from enum import Enum

class Command(Enum):
    """
    Enum for command types
    """
    ADD = "+"
    EDIT = "змінити"
    DELETE = "мінус"
    SEARCH = "розвідка"
    LIST = "інфа"
    ADD_PHONE = "+радійка"
    DELETE_PHONE = "мінус_радійка"
    ADD_EMAIL = "+пошта"
    DELETE_EMAIL = "мінус_пошта"
    ADD_ADDRESS = "+база"
    DELETE_ADDRESS = "мінус_база"
    ADD_TAG = "+патч"
    DELETE_TAG = "мінус_патч"
    ANIVERSARIES = "днюхі"
    ARCHIVE = "схрон"
    RESTORE = "розкопати"
    VIEW_ACTIVE = "інфа"
    VIEW_ARCHIVED = "схованка"
    VIEW_HISTORY = "зміни"

class Argument(Enum):
    """
    Enum for argument types
    """
    ID = "жетон"
    NAME = "позивний"
    BIRTHDAY = "днюха"
    NOTE = "нотатки"
    QUERY = "q"
    BY = "по"
    PHONE = "радійка"
    EMAIL = "пошта"
    ADDRESS = "база"
    TAG = "патч"
    DAYS = "дні"
    CONTENT = "текст"
    SEARCH_CONTENT = "текст"
    SEARCH_TAG = "патч"

class HelpText(Enum):
    """
    Enum for help text
    """
    CONTACT_COMMANDS = 'Команди для керування побратимами'
    NOTE_COMMANDS = 'Команди для керування нотатками'
    
    LIST = 'Показати всіх побратимів'
    ADD = 'Додати побратима'
    EDIT = 'Редагувати побратима'
    DELETE = 'Видалити побратима'
    SEARCH = 'Пошук побратимів'
    ADD_PHONE = 'Додати телефонний номер'
    DELETE_PHONE = 'Видалити телефонний номер'
    ADD_EMAIL = 'Додати електронну адресу'
    DELETE_EMAIL = 'Видалити електронну адресу'
    ADD_ADDRESS = 'Додати адресу'
    DELETE_ADDRESS = 'Видалити адресу'
    ADD_TAG = 'Додати патч до побратима'
    DELETE_TAG = 'Видалити патч з побратима'
    ANIVERSARIES = 'Показати наближені дні народження'

    ARGUMENT_ID = 'Жетон побратима для редагування'
    ARGUMENT_NAME = 'Позивний побратима'
    ARGUMENT_BIRTHDAY = 'Дата народження'
    ARGUMENT_NOTE = 'Примітка'
    ARGUMENT_QUERY = 'Фраза для пошуку'
    ARGUMENT_BY = 'Поле для пошуку (name, email, phone, address, tag, birthday, any)'
    ARGUMENT_PHONE = 'Телефонний номер'
    ARGUMENT_EMAIL = 'Електронна адреса'
    ARGUMENT_ADDRESS = 'Адреса'
    ARGUMENT_TAG = 'Патч для додавання'
    ARGUMENT_DAYS = 'Період в днях (7 за замовчуванням)'
    ARGUMENT_CONTENT = 'Зміст нотатки'
    ARGUMENT_SEARCH_CONTENT = 'Текст для пошуку в нотатках'
    ARGUMENT_SEARCH_TAG = 'Патч для фільтрації нотаток'

    ADD_NOTE = 'Додати нотатку'
    EDIT_NOTE = 'Редагувати нотатку'
    DELETE_NOTE = 'Видалити нотатку'
    SEARCH_NOTE = 'Пошук нотаток'
    ADD_TAG_NOTE = 'Додати патч до нотатки'
    DELETE_TAG_NOTE = 'Видалити патч з нотатки'
    ARCHIVE_NOTE = 'Заархівувати нотатку'
    RESTORE_NOTE = 'Розархівувати нотатку'
    VIEW_ACTIVE_NOTES = 'Показати всі не заархівовані нотатки'
    VIEW_ARCHIVED_NOTES = 'Показати всі заархівовані нотатки'
    VIEW_HISTORY_NOTE = 'Переглянути історію нотатки'

class Messages(Enum):
    """
    Enum for messages
    """
    CONTACT_ADDED = "Побратима {0} успішно додано з жетоном {1}"
    CONTACT_UPDATED = "Побратима {0} успішно оновлено"
    CONTACT_DELETED = "Побратима {0} успішно видалено"
    CONTACT_NOT_FOUND = "Побратим з жетоном {0} не знайдено"
    NO_PARAMETERS_FOR_EDITING = "Не вказано жодного параметру для редагування"
    CONTACTS_NOT_FOUND = "Побратимів не знайдено"
    PHONE_ADDED = "Радійку {0} успішно додано до побратима {1}"
    PHONE_DELETED = "Радійку {0} успішно видалено з побратима {1}"
    EMAIL_ADDED = "Пошту {0} успішно додано до побратима {1}"
    EMAIL_DELETED = "Пошту {0} успішно видалено з побратима {1}"
    TAG_ADDED = "Патч {0} успішно додано до побратима {1}"
    TAG_DELETED = "Патч {0} успішно видалено з побратима {1}"
    ADDRESS_ADDED = "Базу {0} успішно додано до побратима {1}"
    ADDRESS_DELETED = "Базу {0} успішно видалено з побратима {1}"
    NO_ADDRESS_BOOK_FOUND = "No address book found. Creating a new one."
    ERROR_LOADING_ADDRESS_BOOK = "An error occurred while loading the address book: {0}"

    NOTE_ADDED = "Нотатку додано: {0} | Жетон: {1}"
    NOTE_UPDATED = "Нотатку {0} змінено."
    NOTE_DELETED = "Нотатку з жетоном {0} видалено."
    SEARCHING_NOTES = "Розвідка нотаток... Текст: {0}, Патч: {1}, Жетон: {2}"
    FOUND_NOTES = "Результати розвідка:"
    NO_NOTES_FOUND = "Розвідка не дала результатів."
    ADDING_TAG = "Додавання патчу {0} до нотатки {1}"
    TAG_ADDED_TO_NOTE = "Патч {0} додано до нотатки {1}."
    DELETING_TAG = "Видалення патчу {0} з нотаток {1}"
    TAG_DELETED_FROM_NOTE = "Патч {0} видалено з нотаток {1}."
    NOTE_ARCHIVED = "Нотатка {0} в схроні."
    NOTE_RESTORED = "Нотатка з жетоном {0} розкопана."
    ACTIVE_NOTES = "Інфа по нотаткам:"
    NO_ACTIVE_NOTES = "Нема інфи."
    ARCHIVED_NOTES = "Схованка нотаток:"
    NO_ARCHIVED_NOTES = "Нема нотаток в схованці."
    HISTORY_FOR_NOTE = "Зміни для нотатки з жетоном: {0}:"
    NO_HISTORY_FOR_NOTE = "Нема змін в цій нотатці {0}."
    NOTE_NOT_FOUND = "Нотатку {0} не знайдено."
    LOADING_NOTEBOOK = "Loading notebook..."
    NO_NOTEBOOK_FOUND = "No notebook found. Creating a new one."
    ERROR_LOADING_NOTEBOOK = "An error occurred while loading the notebook: {0}"

class Entity(Enum):
    """
    Enum class for entity types as a top level commands
    """
    CONTACT = "побратими"
    NOTE = "нотатки"
