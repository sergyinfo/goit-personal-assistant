"""
Module for contact commands
"""
import argparse
from personal_assistant.enums.command_types import Command
from personal_assistant.models.contact import Contact
from personal_assistant.models.note import Note
from personal_assistant.models.birthday import Birthday
from personal_assistant.services import AddressBook, StorageService
from personal_assistant.services.storage.json_storage import JsonStorage
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
    add_parser.add_argument('--name', required=True, help='Ім\'я контакту')
    add_parser.add_argument('--birthday', help='Дата народження')
    add_parser.add_argument('--note', help='Примітка')
    add_parser.set_defaults(func=add_contact)

    # Contact edit
    edit_parser = subparsers.add_parser(Command.EDIT.value, help='Редагувати контакт')
    edit_parser.add_argument('--id', required=True, help='ID контакта для редагування')
    edit_parser.add_argument('--name', required=True, help='Ім\'я контакту')
    edit_parser.add_argument('--birthday', help='Дата народження')
    edit_parser.add_argument('--note', help='Примітка')
    edit_parser.set_defaults(func=edit_contact)

    # Contact delete
    delete_parser = subparsers.add_parser(Command.DELETE.value, help='Видалити контакт')
    delete_parser.add_argument('--id', required=True, help='ID контакта для видалення')
    delete_parser.set_defaults(func=delete_contact)

    # Contact search
    search_parser = subparsers.add_parser(Command.SEARCH.value, help='Пошук контактів')
    search_parser.add_argument('--name', help='Ім\'я для пошуку')
    search_parser.add_argument('--email', help='Email для фільтрації')
    search_parser.add_argument('--phone', help='Телефонний номер для фільтрації')
    search_parser.set_defaults(func=search_contacts)

    # Phone add
    add_phone_parser = subparsers.add_parser(
        Command.ADD_PHONE.value, help='Додати телефонний номер'
    )
    add_phone_parser.add_argument('--id', required=True, help='ID контакта')
    add_phone_parser.add_argument('--phone', required=True, help='Телефонний номер')
    add_phone_parser.set_defaults(func=add_phone)

    # Phone delete
    delete_phone_parser = subparsers.add_parser(
        Command.DELETE_PHONE.value, help='Видалити телефонний номер'
    )
    delete_phone_parser.add_argument('--id', required=True, help='ID контакта')
    delete_phone_parser.add_argument('--phone', required=True, help='Телефонний номер')
    delete_phone_parser.set_defaults(func=delete_phone)

    # E-mail add
    add_email_parser = subparsers.add_parser(
        Command.ADD_EMAIL.value, help='Додати електронну адресу'
    )
    add_email_parser.add_argument('--id', required=True, help='ID контакта')
    add_email_parser.add_argument('--email', required=True, help='Електронна адреса')
    add_email_parser.set_defaults(func=add_email)

    # E-mail remove
    delete_email_parser = subparsers.add_parser(
        Command.DELETE_EMAIL.value, help='Видалити електронну адресу'
    )
    delete_email_parser.add_argument('--id', required=True, help='ID контакта')
    delete_email_parser.add_argument('--email', required=True, help='Електронна адреса')
    delete_email_parser.set_defaults(func=delete_email)

    # Tag add
    add_tag_parser = subparsers.add_parser(
        Command.ADD_TAG.value, help='Додати тег до контакта'
    )
    add_tag_parser.add_argument('--id', required=True, help='ID контакта')
    add_tag_parser.add_argument('--tag', required=True, help='Тег для додавання')
    add_tag_parser.set_defaults(func=add_tag_to_contact)

    # Tag delete
    delete_tag_parser = subparsers.add_parser(
        Command.DELETE_TAG.value, help='Видалити тег з контакта'
    )
    delete_tag_parser.add_argument('--id', required=True, help='ID контакта')
    delete_tag_parser.add_argument('--tag', required=True, help='Тег для видалення')
    delete_tag_parser.set_defaults(func=delete_tag_from_contact)

storage_service = StorageService(JsonStorage())
address_book = AddressBook(storage_service)
try:
    address_book.load()
except FileNotFoundError:
    print("No address book found. Creating a new one.")
except Exception as e:
    print(f"An error occurred while loading the address book: {e}")

@input_error
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

    birthday = None
    if args.birthday is not None:
        birthday = Birthday(args.birthday)

    note = None
    if args.note is not None:
        note = Note(args.note, address_book.tag_manager)

    contact = Contact(args.name, birthday, note)
    address_book.set_contact(contact)
    print(f"Контакт {args.name} успішно додано з ID {contact.id}")
    address_book.save()


@input_error
def edit_contact(args: argparse.Namespace) -> None:
    """
    Edit an existing contact in the address book
    """
    contact = address_book.get_contact(args.id)
    if not contact:
        print(f"Контакт з ID {args.id} не знайдено")
        return

    if args.name:
        contact.set_name(args.name)

    if args.birthday is not None:
        contact.set_birthdate(Birthday(args.birthday))

    if args.note is not None:
        contact.set_note(Note(args.note, address_book.tag_manager))

    address_book.set_contact(contact)
    print(f"Контакт {args.id} успішно оновлено")
    address_book.save()


@input_error
def delete_contact(args: argparse.Namespace) -> None:
    """
    Delete a contact from the address book
    """
    address_book.remove_contact(args.id)
    print(f"Контакт {args.id} успішно видалено")
    address_book.save()


@input_error
def search_contacts(args: argparse.Namespace) -> None:
    """
    Search for contacts in the address book
    """
    results = address_book.find(args.name or "")
    if results:
        for contact in results:
            print(contact)
    else:
        print("Контакти не знайдено")


@input_error
def add_phone(args: argparse.Namespace) -> None:
    """
    Add a phone number to an existing contact
    """
    contact = address_book.get_contact(args.id)
    if not contact:
        print(f"Контакт з ID {args.id} не знайдено")
        return

    contact.add_phone(args.phone)
    address_book.set_contact(contact)
    print(f"Телефонний номер {args.phone} успішно додано до контакту {args.id}")
    address_book.save()


@input_error
def delete_phone(args: argparse.Namespace) -> None:
    """
    Delete a phone number from an existing contact
    """
    contact = address_book.get_contact(args.id)
    if not contact:
        print(f"Контакт з ID {args.id} не знайдено")
        return

    contact.remove_phone(args.phone)
    address_book.set_contact(contact)
    print(f"Телефонний номер {args.phone} успішно видалено з контакту {args.id}")
    address_book.save()


@input_error
def add_email(args: argparse.Namespace) -> None:
    """
    Add an email to an existing contact
    """
    contact = address_book.get_contact(args.id)
    if not contact:
        print(f"Контакт з ID {args.id} не знайдено")
        return

    contact.add_email(args.email)
    address_book.set_contact(contact)
    print(f"Електронну адресу {args.email} успішно додано до контакту {args.id}")
    address_book.save()


@input_error
def delete_email(args: argparse.Namespace) -> None:
    """
    Delete an email from an existing contact
    """
    contact = address_book.get_contact(args.id)
    if not contact:
        print(f"Контакт з ID {args.id} не знайдено")
        return

    contact.remove_email(args.email)
    address_book.set_contact(contact)
    print(f"Електронну адресу {args.email} успішно видалено з контакту {args.id}")
    address_book.save()


@input_error
def add_tag_to_contact(args: argparse.Namespace) -> None:
    """
    Add a tag to an existing contact
    """
    contact = address_book.get_contact(args.id)
    if not contact:
        print(f"Контакт з ID {args.id} не знайдено")
        return

    contact.add_tag(args.tag)
    address_book.set_contact(contact)
    print(f"Тег {args.tag} успішно додано до контакту {args.id}")
    address_book.save()


@input_error
def delete_tag_from_contact(args: argparse.Namespace) -> None:
    """
    Delete a tag from an existing contact
    """
    contact = address_book.get_contact(args.id)
    if not contact:
        print(f"Контакт з ID {args.id} не знайдено")
        return

    contact.remove_tag(args.tag)
    address_book.set_contact(contact)
    print(f"Тег {args.tag} успішно видалено з контакту {args.id}")
    address_book.save()

@input_error
def add_address(args: argparse.Namespace) -> None:
    """
    Add an address to an existing contact
    """
    contact = address_book.get_contact(args.id)
    if not contact:
        print(f"Контакт з ID {args.id} не знайдено")
        return

    contact.add_address(args.address)
    address_book.set_contact(contact)
    print(f"Адреса {args.address} успішно додано до контакту {args.id}")
    address_book.save()


@input_error
def remove_address(args: argparse.Namespace) -> None:
    """
    Remove an address from an existing contact
    """
    contact = address_book.get_contact(args.id)
    if not contact:
        print(f"Контакт з ID {args.id} не знайдено")
        return

    contact.remove_address(args.address)
    address_book.set_contact(contact)
    print(f"Адреса {args.address} успішно видалено з контакту {args.id}")
    address_book.save()


@input_error
def congratulations_date(args: argparse.Namespace) -> None:
    """
    List contacts with birthdays in a given number of days from today
    """
    days = int(args.days)
    contacts = address_book.congratulations_date(days)
    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("Немає контактів з днями народження у вказаний період")