"""
A Contact class that represents a contact in the personal assistant application. 
The class has methods to add, edit, and remove contact information such as 
phone numbers, email addresses, addresses, and tags. It also provides methods 
to check upcoming birthdays and to manage tags associated with the contact.
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from personal_assistant.models import EmailAddress, Address, Birthday, Note, PhoneNumber
from personal_assistant.services import TagManagerService
from personal_assistant.enums import EntityType
from personal_assistant.utils.helpers import to_comma_separated_string

class Contact:
    """
    This is the Contact class for the personal assistant application.
    """
    def __init__(
            self,
            name: str,
            birthday: Optional[Birthday] = None,
            note: Optional[Note] = None,
            tags: Optional[List[str]] = None,
            contact_id: Optional[str] = None
        ) -> None:
        self.tag_manager: TagManagerService = TagManagerService()
        self.id: str = contact_id or str(uuid.uuid4())[:8]
        self.name: str = name
        self.birthday: Birthday = birthday or None
        self.phone_numbers: List[PhoneNumber] = []
        self.emails: List[EmailAddress] = []
        self.addresses: List[Address] = []
        self.note: Note = note or None
        self.tags: List[str] = []

        if tags is not None:
            for tag in tags:
                self.add_tag(tag)

    def __str__(self):
        return (
            f"{self.id:10} {self.name:20} {self.formatted_birthday():20}"
            f"{to_comma_separated_string(self.phone_numbers):30} "
            f"{to_comma_separated_string(self.emails):30} "
            f"{to_comma_separated_string(self.addresses):20} "
            f"{to_comma_separated_string(self.note):20} "
            f"{to_comma_separated_string(self.tags):10}"
        )

    def formatted_birthday(self, no_date: str = "No Birthday") -> str:
        """
        Return the formatted birthday of the contact
        """
        if self.birthday:
            return f"{self.birthday} ({self.birthday.get_age()})"
        return no_date

    def is_upcoming_bd(self, days: int) -> bool:
        """
        Check if the contact's birthday is upcoming in the next `days` days
        """
        if not self.birthday:
            return False

        today = datetime.now().date()
        next_birthday = self.birthday.get_next_birthday(today)
        return next_birthday <= today + timedelta(days=days)

    def congratulations_date(self) -> Optional[datetime.date]:
        """
        Return the date when the contact's birthday is celebrated
        """
        if not self.birthday:
            return None

        today = datetime.now().date()
        next_birthday = self.birthday.get_next_birthday(today)
        if next_birthday.weekday() in (5, 6):  # 5 is Saturday, 6 is Sunday
            next_birthday += timedelta(days=7 - next_birthday.weekday())
        return next_birthday

    def add_phone(self, phone: PhoneNumber) -> None:
        """
        Add phone number to the contact
        """
        self.phone_numbers.append(phone)

    def add_email(self, email: EmailAddress) -> None:
        """
        Add email address to the contact
        """
        self.emails.append(email)

    def add_address(self, address: Address) -> None:
        """
        Add address to the contact
        """
        self.addresses.append(address)

    def add_tag(self, tag_name: str) -> None:
        """
        Add tag to the contact
        """
        if tag_name not in self.tags:
            self.tags.append(tag_name)
            self.tag_manager.add_tag(tag_name, EntityType.CONTACT, self.id)

    def set_name(self, name: str) -> None:
        """
        Edit the name of the contact
        """
        self.name = name

    def set_birthday(self, birthday: Birthday) -> None:
        """
        Edit the birthday of the contact
        """
        self.birthday = birthday

    def edit_phone(self, old_phone: PhoneNumber, new_phone: PhoneNumber) -> None:
        """
        Edit the phone number of the contact
        """
        self.phone_numbers = [
            phone for phone in self.phone_numbers if phone != old_phone
        ]
        self.phone_numbers.append(new_phone)

    def edit_email(self, old_email: EmailAddress, new_email: EmailAddress) -> None:
        """
        Edit the email address of the contact
        """
        self.emails = [email for email in self.emails if email != old_email]
        self.emails.append(new_email)

    def edit_address(self, old_address: Address, new_address: Address) -> None:
        """
        Edit the address of the contact
        """
        self.addresses = [
            address for address in self.addresses if address != old_address
        ]
        self.addresses.append(new_address)

    def set_note(self, note: Note) -> None:
        """
        Edit the note of the contact
        """
        self.note = note

    def remove_phone(self, phone: PhoneNumber):
        """
        Remove the phone number of the contact
        """
        self.phone_numbers = [p for p in self.phone_numbers if p != phone]

    def remove_email(self, email: EmailAddress):
        """
        Remove the email address of the contact
        """
        self.emails = [e for e in self.emails if e != email]

    def remove_address(self, address: Address):
        """
        Remove the address of the contact
        """
        self.addresses = [a for a in self.addresses if a != address]

    def remove_tag(self, tag_name):
        """
        Remove the tag of the contact
        """
        tag_manager = TagManagerService()
        tag_manager.remove_tag(tag_name, EntityType.CONTACT, self.id)
        self.tags = [tag for tag in self.tags if tag != tag_name]

    def to_dict(self):
        """
        Return a dictionary representation of the contact
        """
        return {
            "id": self.id,
            "name": self.name,
            "birthday": self.birthday.to_dict() if self.birthday else None,
            "phone_numbers": [phone.to_dict() for phone in self.phone_numbers],
            "emails": [email.to_dict() for email in self.emails],
            "addresses": [address.to_dict() for address in self.addresses],
            "tags": self.tags,
            "note": self.note.to_dict() if self.note else ""
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Contact object from a dictionary
        """
        obj = cls(name=data["name"], contact_id=data["id"], tags=data.get("tags"))
        obj.birthday = Birthday.from_dict(data["birthday"]) if data["birthday"] else None
        obj.phone_numbers = [PhoneNumber.from_dict(phone) for phone in data["phone_numbers"]]
        obj.emails = [EmailAddress.from_dict(email) for email in data["emails"]]
        obj.addresses = [Address.from_dict(address) for address in data["addresses"]]
        return obj
