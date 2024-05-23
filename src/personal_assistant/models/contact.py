import uuid
from datetime import datetime, timedelta

from email_address import EmailAddress
from address import Address
from birthday import Birthday
from note import Note
from phone_number import PhoneNumber
from tag_manager import TagManager, EntityType


class Contact:
    def __init__(self, name):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.birthday = None
        self.phone_numbers = []
        self.emails: list[EmailAddress] = []
        self.addresses = []
        self.notes = []
        self.tags = set()

    def __str__(self):
        phone_str = ", ".join([str(phone) for phone in self.phone_numbers])
        email_str = ", ".join([str(e) for e in self.emails])
        birthday_info = (
            f", День народження: {self.birthday}, Вік: {self.birthday.calculate_age()}"
            if self.birthday
            else ""
        )
        address_str = ", ".join([str(addr) for addr in self.addresses])
        notes_str = ", ".join([str(note) for note in self.notes])
        tags_str = ", ".join([str(tag) for tag in self.tags])

        return f"ID контакту: {self.uuid}, Ім'я: {self.name}{birthday_info}, Телефони: {phone_str}, Emails: {email_str}, Адреси: {address_str}, Нотатки: {notes_str}, Теги: {tags_str}. "

    # Adding info
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def is_upcoming_bd(self, days: int):
        if not self.birthday:
            return False

        today = datetime.now().date()
        next_birthday = self.birthday.get_next_birthday(today)
        return next_birthday <= today + timedelta(days=days)

    def congratulations_date(self):
        if not self.birthday:
            return None

        today = datetime.now().date()
        next_birthday = self.birthday.get_next_birthday(today)
        if next_birthday.weekday() in (5, 6):  # 5 is Saturday, 6 is Sunday
            next_birthday += timedelta(days=7 - next_birthday.weekday())
        return next_birthday

    def add_phone(self, phone):
        try:
            self.phone_numbers.append(PhoneNumber(phone))
        except ValueError as e:
            print(f"Error: {e}")

    def add_email(self, email):
        try:
            self.emails.append(EmailAddress(email))
        except ValueError as e:
            print(f"Error: {e}")

    def add_address(self, address):
        try:
            self.addresses.append(Address(address))
        except ValueError as e:
            print(f"Error: {e}")

    def add_note(self, note):
        try:
            self.notes.append(Note(note))
        except ValueError as e:
            print(f"Error: {e}")

    def add_tag(self, tag_name):
        try:
            tag_manager = TagManager()
            tag_manager.add_tag(tag_name, EntityType.CONTACT, self.uuid)
            self.tags.add(tag_name)
        except ValueError as e:
            print(f"Error: {e}")

    # Editing info

    def edit_name(self, name):
        try:
            self.name = name
        except ValueError as e:
            print(f"Error: {e}")

    def edit_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(f"Error: {e}")

    def edit_phone(self, old_phone, new_phone):
        try:
            old_phone = PhoneNumber(old_phone)
            new_phone = PhoneNumber(new_phone)
            self.phone_numbers = [
                phone for phone in self.phone_numbers if phone != old_phone
            ]
            self.phone_numbers.append(new_phone)
        except ValueError as e:
            print(f"Error: {e}")

    def edit_email(self, old_email, new_email):
        try:
            old_email = EmailAddress(old_email)
            new_email = EmailAddress(new_email)
            self.emails = [email for email in self.emails if email != old_email]
            self.emails.append(new_email)
        except ValueError as e:
            print(f"Error: {e}")

    def edit_address(self, old_address, new_address):
        try:
            old_address = Address(old_address)
            new_address = Address(new_address)
            self.addresses = [
                address for address in self.addresses if address != old_address
            ]
            self.addresses.append(new_address)
        except ValueError as e:
            print(f"Error: {e}")

    def edit_note(self, old_note, new_note):
        try:
            old_note = Note(old_note)
            new_note = Note(new_note)
            self.notes = [note for note in self.notes if note != old_note]
            self.notes.append(Note(new_note))
        except ValueError as e:
            print(f"Error: {e}")

    # Removing info

    def remove_birthday(self):
        try:
            self.birthday = None
        except ValueError as e:
            print(f"Error: {e}")

    def remove_phone(self, phone):
        try:
            phone = PhoneNumber(phone)
            self.phone_numbers = [p for p in self.phone_numbers if p != phone]
        except ValueError as e:
            print(f"Error: {e}")

    def remove_email(self, email):
        try:
            email = EmailAddress(email)
            self.emails = [e for e in self.emails if e != email]
        except ValueError as e:
            print(f"Error: {e}")

    def remove_address(self, address):
        try:
            address = Address(address)
            self.addresses = [a for a in self.addresses if a != address]
        except ValueError as e:
            print(f"Error: {e}")

    def remove_note(self, note):
        try:
            note = Note(note)
            self.notes = [n for n in self.notes if n != note]
        except ValueError as e:
            print(f"Error: {e}")

    def remove_tag(self, tag_name):
        try:
            tag_manager = TagManager()
            tag_manager.remove_tag(tag_name, EntityType.CONTACT, self.uuid)
            self.tags.discard(tag_name)
        except ValueError as e:
            print(f"Error: {e}")

    # Deleting the contact

    def delete_contact(self):
        for tag_name in self.tags:
            TagManager().remove_tag(tag_name, EntityType.CONTACT, self.uuid)
        self.birthday = None
        self.addresses = []
        self.phone_numbers = []
        self.notes = []
        self.emails = []
        self.tags = set()
