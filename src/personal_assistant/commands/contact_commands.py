"""
Module for contact commands
"""
import argparse
from personal_assistant.enums.command_types import Command, Argument
from personal_assistant.models.contact import Contact
from personal_assistant.models import PhoneNumber, Birthday, Note, EmailAddress, Address
from personal_assistant.services import AddressBook, StorageService
from personal_assistant.services.storage.secure_json_storage import SecureJsonStorage
from personal_assistant.utils.decorators import input_error

def handle_contact_commands(parser: argparse.ArgumentParser) -> None:
    """
    Add subparsers for contact commands
    """
    subparsers = parser.add_subparsers(
        dest='contact_command', help='Команди для керування контактами'
    )

    # Contact list
    list_parser = subparsers.add_parser(Command.LIST.value, help='Показати всі контакти')
    list_parser.set_defaults(func=contact_list)

    # Contact add
    add_parser = subparsers.add_parser(Command.ADD.value, help='Додати контакт')
    add_parser.add_argument('--' + Argument.NAME.value, required=True, help='Ім\'я контакту')
    add_parser.add_argument('--' + Argument.BIRTHDAY.value, help='Дата народження')
    add_parser.add_argument('--' + Argument.NOTE.value, help='Примітка')
    add_parser.set_defaults(func=add_contact)

    # Contact edit
    edit_parser = subparsers.add_parser(Command.EDIT.value, help='Редагувати контакт')
    edit_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта для редагування')
    edit_parser.add_argument('--' + Argument.NAME.value, help='Ім\'я контакту')
    edit_parser.add_argument('--' + Argument.BIRTHDAY.value, help='Дата народження')
    edit_parser.add_argument('--' + Argument.NOTE.value, help='Примітка')
    edit_parser.set_defaults(func=edit_contact)

    # Contact delete
    delete_parser = subparsers.add_parser(Command.DELETE.value, help='Видалити контакт')
    delete_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта для видалення')
    delete_parser.set_defaults(func=delete_contact)

    # Contact search
    search_parser = subparsers.add_parser(Command.SEARCH.value, help='Пошук контактів')
    search_parser.add_argument('--' + Argument.QUERY.value, required=True, help='Фраза для пошуку')
    search_parser.add_argument('--' + Argument.BY.value, help='Поле для пошуку (name, email, phone, address, tag, birthday, any)')
    search_parser.set_defaults(func=search_contacts)

    # Phone add
    add_phone_parser = subparsers.add_parser(
        Command.ADD_PHONE.value, help='Додати телефонний номер'
    )
    add_phone_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта')
    add_phone_parser.add_argument('--' + Argument.PHONE.value, required=True, help='Телефонний номер')
    add_phone_parser.set_defaults(func=add_phone)

    # Phone delete
    delete_phone_parser = subparsers.add_parser(
        Command.DELETE_PHONE.value, help='Видалити телефонний номер'
    )
    delete_phone_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта')
    delete_phone_parser.add_argument('--' + Argument.PHONE.value, required=True, help='Телефонний номер')
    delete_phone_parser.set_defaults(func=delete_phone)

    # E-mail add
    add_email_parser = subparsers.add_parser(
        Command.ADD_EMAIL.value, help='Додати електронну адресу'
    )
    add_email_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта')
    add_email_parser.add_argument('--' + Argument.EMAIL.value, required=True, help='Електронна адреса')
    add_email_parser.set_defaults(func=add_email)

    # E-mail remove
    delete_email_parser = subparsers.add_parser(
        Command.DELETE_EMAIL.value, help='Видалити електронну адресу'
    )
    delete_email_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта')
    delete_email_parser.add_argument('--' + Argument.EMAIL.value, required=True, help='Електронна адреса')
    delete_email_parser.set_defaults(func=delete_email)

    # Address add
    add_address_parser = subparsers.add_parser(
        Command.ADD_ADDRESS.value, help='Додати адресу'
    )
    add_address_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта')
    add_address_parser.add_argument('--' + Argument.ADDRESS.value, required=True, help='Адреса')
    add_address_parser.set_defaults(func=add_address)

    # Address remove
    delete_address_parser = subparsers.add_parser(
        Command.DELETE_ADDRESS.value, help='Видалити адресу'
    )
    delete_address_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта')
    delete_address_parser.add_argument('--' + Argument.ADDRESS.value, required=True, help='Адреса')
    delete_address_parser.set_defaults(func=delete_address)

    # Tag add
    add_tag_parser = subparsers.add_parser(
        Command.ADD_TAG.value, help='Додати тег до контакта'
    )
    add_tag_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта')
    add_tag_parser.add_argument('--' + Argument.TAG.value, required=True, help='Тег для додавання')
    add_tag_parser.set_defaults(func=add_tag_to_contact)

    # Tag delete
    delete_tag_parser = subparsers.add_parser(
        Command.DELETE_TAG.value, help='Видалити тег з контакта'
    )
    delete_tag_parser.add_argument('--' + Argument.ID.value, required=True, help='ID контакта')
    delete_tag_parser.add_argument('--' + Argument.TAG.value, required=True, help='Тег для видалення')
    delete_tag_parser.set_defaults(func=delete_tag_from_contact)

    # Closest aniversary
    aniversaries_parser = subparsers.add_parser(
        Command.ANIVERSARIES.value, help='Показати наближені дні народження'
    )
    aniversaries_parser.add_argument('--' + Argument.DAYS.value, help='Період в днях (7 за замовчуванням)')
    aniversaries_parser.set_defaults(func=congratulations_date)

storage_service = StorageService(SecureJsonStorage())
address_book = AddressBook(storage_service)
try:
    address_book.load()
except FileNotFoundError:
    print("No address book found. Creating a new one.")
except Exception as e:
    print(f"An error occurred while loading the address book: {e}")


def contact_list(args: argparse.Namespace) -> None:
    """
    List all contacts in the address book
    """
    address_book.print_contacts_table()

@input_error
def add_contact(args: argparse.Namespace) -> None:
    """
    Add a new contact to the address book
    """

    birthday = getattr(args, Argument.BIRTHDAY.value, None)
    note = getattr(args, Argument.NOTE.value, None)
    name = getattr(args, Argument.NAME.value)

    contact = Contact(name, birthday, note)
    address_book.set_contact(contact)
    print(f"Контакт {name} успішно додано з ID {contact.id}")
    address_book.save()

@input_error
def edit_contact(args: argparse.Namespace) -> None:
    """
    Edit an existing contact in the address book
    """
    name = getattr(args, Argument.NAME.value, None)
    birthday = getattr(args, Argument.BIRTHDAY.value, None)
    note = getattr(args, Argument.NOTE.value, None)

    if not name and not birthday and not note:
        print("Не вказано жодного параметру для редагування")
        return

    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(f"Контакт з ID {getattr(args, Argument.ID.value)} не знайдено")
        return

    if name:
        contact.set_name(name)

    if birthday is not None:
        contact.set_birthday(Birthday(birthday))

    if note is not None:
        contact.set_note(Note(note, address_book.tag_manager))

    address_book.set_contact(contact)
    print(f"Контакт {getattr(args, Argument.ID.value)} успішно оновлено")
    address_book.save()

@input_error
def delete_contact(args: argparse.Namespace) -> None:
    """
    Delete a contact from the address book
    """
    address_book.remove_contact(getattr(args, Argument.ID.value))
    print(f"Контакт {getattr(args, Argument.ID.value)} успішно видалено")
    address_book.save()

@input_error
def search_contacts(args: argparse.Namespace) -> None:
    """
    Search for contacts in the address book
    """
    results = address_book.find(getattr(args, Argument.QUERY.value), getattr(args, Argument.BY.value, 'any'))
    if results:
        address_book.print_contacts_table(results)
    else:
        print("Контакти не знайдено")

@input_error
def add_phone(args: argparse.Namespace) -> None:
    """
    Add a phone number to an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(f"Контакт з ID {getattr(args, Argument.ID.value)} не знайдено")
        return

    phone = PhoneNumber(getattr(args, Argument.PHONE.value))
    contact.add_phone(phone)
    address_book.set_contact(contact)
    print(f"Телефонний номер {getattr(args, Argument.PHONE.value)} успішно додано до контакту {getattr(args, Argument.ID.value)}")
    address_book.save()

@input_error
def delete_phone(args: argparse.Namespace) -> None:
    """
    Delete a phone number from an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(f"Контакт з ID {getattr(args, Argument.ID.value)} не знайдено")
        return
    phone = PhoneNumber(getattr(args, Argument.PHONE.value))
    contact.remove_phone(phone)
    address_book.set_contact(contact)
    print(f"Телефонний номер {getattr(args, Argument.PHONE.value)} успішно видалено з контакту {getattr(args, Argument.ID.value)}")
    address_book.save()

@input_error
def add_email(args: argparse.Namespace) -> None:
    """
    Add an email to an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(f"Контакт з ID {getattr(args, Argument.ID.value)} не знайдено")
        return

    email = EmailAddress(getattr(args, Argument.EMAIL.value))
    contact.add_email(email)
    address_book.set_contact(contact)
    print(f"Електронну адресу {getattr(args, Argument.EMAIL.value)} успішно додано до контакту {getattr(args, Argument.ID.value)}")
    address_book.save()

@input_error
def delete_email(args: argparse.Namespace) -> None:
    """
    Delete an email from an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(f"Контакт з ID {getattr(args, Argument.ID.value)} не знайдено")
        return

    email = EmailAddress(getattr(args, Argument.EMAIL.value))
    contact.remove_email(email)
    address_book.set_contact(contact)
    print(f"Електронну адресу {getattr(args, Argument.EMAIL.value)} успішно видалено з контакту {getattr(args, Argument.ID.value)}")
    address_book.save()

@input_error
def add_tag_to_contact(args: argparse.Namespace) -> None:
    """
    Add a tag to an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(f"Контакт з ID {getattr(args, Argument.ID.value)} не знайдено")
        return

    contact.add_tag(getattr(args, Argument.TAG.value))
    address_book.set_contact(contact)
    print(f"Тег {getattr(args, Argument.TAG.value)} успішно додано до контакту {getattr(args, Argument.ID.value)}")
    address_book.save()

@input_error
def delete_tag_from_contact(args: argparse.Namespace) -> None:
    """
    Delete a tag from an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(f"Контакт з ID {getattr(args, Argument.ID.value)} не знайдено")
        return

    contact.remove_tag(getattr(args, Argument.TAG.value))
    address_book.set_contact(contact)
    print(f"Тег {getattr(args, Argument.TAG.value)} успішно видалено з контакту {getattr(args, Argument.ID.value)}")
    address_book.save()

@input_error
def add_address(args: argparse.Namespace) -> None:
    """
    Add an address to an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(f"Контакт з ID {getattr(args, Argument.ID.value)} не знайдено")
        return

    address = Address(getattr(args, Argument.ADDRESS.value))
    contact.add_address(address)
    address_book.set_contact(contact)
    print(f"Адреса {getattr(args, Argument.ADDRESS.value)} успішно додано до контакту {getattr(args, Argument.ID.value)}")
    address_book.save()

@input_error
def delete_address(args: argparse.Namespace) -> None:
    """
    Remove an address from an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(f"Контакт з ID {getattr(args, Argument.ID.value)} не знайдено")
        return

    address = Address(getattr(args, Argument.ADDRESS.value))
    contact.remove_address(address)
    address_book.set_contact(contact)
    print(f"Адреса {getattr(args, Argument.ADDRESS.value)} успішно видалено з контакту {getattr(args, Argument.ID.value)}")
    address_book.save()

@input_error
def congratulations_date(args: argparse.Namespace) -> None:
    """
    List contacts with birthdays in a given number of days from today
    """
    days = int(getattr(args, Argument.DAYS.value, 7))
    address_book.print_aniversaries_table(days)
