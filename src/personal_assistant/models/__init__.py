"""
A package that contains the models used in the personal assistant application.
"""
from personal_assistant.models.note import Note
from personal_assistant.models.note_history_entry import NoteHistoryEntry
from personal_assistant.models.tag import Tag
from personal_assistant.models.email_address import EmailAddress
from personal_assistant.models.birthday import Birthday
from personal_assistant.models.address import Address
from personal_assistant.models.phone_number import PhoneNumber

__all__ = [ 
    "Note", 
    "NoteHistoryEntry",
    "Tag",
    "EmailAddress",
    "Birthday",
    "Address",
    "PhoneNumber"
]