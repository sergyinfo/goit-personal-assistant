"""
A module that contains the AddressBook class, which is responsible for managing contacts and tags.
"""
import collections
from typing import Dict, List
from tabulate import tabulate
from personal_assistant.models.contact import Contact
from personal_assistant.services import StorageService
from personal_assistant.services import TagManagerService
from personal_assistant.enums import EntityType

class AddressBook:
    """
    A class that represents an address book, which is responsible for managing contacts and tags.
    """
    def __init__(self, storage_service: StorageService) -> None:
        self.storage_service: StorageService = storage_service
        self.tag_manager: TagManagerService = TagManagerService()
        self.contacts: Dict[str, Contact] = {}

    def get_contact(self, contact_id: str) -> Contact:
        """
        Retrieves a contact by its ID.
        """
        return self.contacts.get(contact_id) or None

    def set_contact(self, contact: Contact) -> None:
        """
        Adds a new contact to the address book.
        """
        if isinstance(contact, Contact):
            self.contacts[contact.id] = contact
        else:
            raise ValueError("Invalid contact type. Please provide an instance of Contact.")

    def remove_contact(self, contact_id: str) -> None:
        """
        Removes a contact from the address book.
        """
        if contact_id in self.contacts:
            contact = self.contacts.pop(contact_id)
            for tag in contact.tags:
                self.tag_manager.remove_tag(tag, EntityType.CONTACT, contact_id)

    def find(self, keyword: str, field: str = 'any') -> List[Contact]:
        """
        Finds contacts that match the given keyword.
        """
        found_contacts = []
        for contact in self.contacts.values():
            if self._matches_contact(contact, keyword, field):
                found_contacts.append(contact)
        return found_contacts

    def _matches_contact(self, contact: Contact, keyword: str, field: str) -> bool:
        """
        Checks if a contact matches the given keyword.
        """
        is_any = field == 'any'
        keyword = keyword.lower()
        if ('name' == field or is_any) and keyword in contact.name.lower():
            return True
        if ('phone' == field or is_any) and any(keyword in str(phone).lower() for phone in contact.phone_numbers):
            return True
        if ('email' == field or is_any) and any(keyword in str(email).lower() for email in contact.emails):
            return True
        if ('address' == field or is_any) and any(keyword in str(address).lower() for address in contact.addresses):
            return True
        if ('note' == field or is_any) and contact.note and keyword in str(contact.note).lower():
            return True
        if ('tag' == field or is_any) and any(keyword in tag.lower() for tag in contact.tags):
            return True
        if ('birthdate' == field or is_any) and contact.birthday and keyword in str(contact.birthday).lower():
            return True
        return False

    def save(self) -> None:
        """
        Serialize the contacts data and save it to the storage service.
        """
        data = {contact_id: contact.to_dict() for contact_id, contact in self.contacts.items()}
        self.storage_service.save_data(data, "contacts_data")

    def load(self) -> None:
        """
        Deserialize the contacts data and load it from the storage service.
        """
        data = self.storage_service.load_data("contacts_data")
        self.contacts = {contact_id: Contact.from_dict(contact_data) for contact_id, contact_data in data.items()}

    def print_contacts_table(self, contacts: List[Contact] = None, headers: Dict[str, str] = None):
        """
        Print a table with all the contacts in the address book.
        """
        if contacts is None:
            contacts = self.contacts.values()

        # Gather data from all contacts
        contacts_data = [contact.to_dict(True) for contact in contacts]

        if headers is None:
            headers = {
                "id": "ID",
                "name": "Ім'я",
                "birthday": "Дата народження",
                "age": "Дата народження",
                "phone_numbers": "Телефони",
                "emails": "Email",
                "addresses": "Адреси",
                "note": "Примітка",
                "tags": "Теги"
            }

        # Reorder or alter data according to custom headers
        reformatted_data = [
            {headers[key]: value for key, value in contact.items() if key in headers}
            for contact in contacts_data
        ]

        # Use tabulate to print the table with headers specified in the desired order
        print(tabulate(reformatted_data, headers="keys", tablefmt="grid"))

    def print_aniversaries_table(self, days: int = 7):
        """
        Print a table with contacts that have an upcoming birthday.
        """
        headers = {
            "id": "ID",
            "name": "Ім'я",
            "birthday": "Дата народження",
            "age": "Вік",
            "congratulations_date": "Дата привітання"
        }

        contacts = [contact for contact in self.contacts.values() if contact.is_upcoming_bd(days)]

        #keep only headers that are relevant
        aniversaries = {}
        for contact in contacts:
            aniversaries[contact.id] = {
                "id": contact.id,
                "name": contact.name,
                "birthday": contact.formatted_birthday(),
                "age": contact.birthday.get_age() + 1,
                "congratulations_date": contact.congratulations_date().strftime("%d.%m.%Y")
            }

        # sort by congratulations and keep the dictionary
        aniversaries = collections.OrderedDict(
            sorted(aniversaries.items(), key=lambda item: item[1]["congratulations_date"])
        )

        # reformat data
        reformatted_data = []
        for contact in aniversaries.values():
            reformatted_data.append({
                headers[key]: value for key, value in contact.items() if key in headers
            })

        # Use tabulate to print the table with headers specified in the desired order
        print(tabulate(reformatted_data, headers="keys", tablefmt="grid"))

    def __str__(self):
        return '\n'.join(str(contact) for contact in self.contacts.values())
