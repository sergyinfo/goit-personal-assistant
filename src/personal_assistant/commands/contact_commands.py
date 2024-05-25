"""
Module for contact commands
"""
import argparse
from personal_assistant.enums.command_types import Command, Argument, HelpText, Messages
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
        dest='contact_command', help=HelpText.CONTACT_COMMANDS.value
    )

    # Contact list
    list_parser = subparsers.add_parser(Command.LIST.value, help=HelpText.LIST.value)
    list_parser.set_defaults(func=contact_list)

    # Contact add
    add_parser = subparsers.add_parser(Command.ADD.value, help=HelpText.ADD.value)
    add_parser.add_argument('--' + Argument.NAME.value, required=True, help=HelpText.ARGUMENT_NAME.value)
    add_parser.add_argument('--' + Argument.BIRTHDAY.value, help=HelpText.ARGUMENT_BIRTHDAY.value)
    add_parser.add_argument('--' + Argument.NOTE.value, help=HelpText.ARGUMENT_NOTE.value)
    add_parser.set_defaults(func=add_contact)

    # Contact edit
    edit_parser = subparsers.add_parser(Command.EDIT.value, help=HelpText.EDIT.value)
    edit_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    edit_parser.add_argument('--' + Argument.NAME.value, help=HelpText.ARGUMENT_NAME.value)
    edit_parser.add_argument('--' + Argument.BIRTHDAY.value, help=HelpText.ARGUMENT_BIRTHDAY.value)
    edit_parser.add_argument('--' + Argument.NOTE.value, help=HelpText.ARGUMENT_NOTE.value)
    edit_parser.set_defaults(func=edit_contact)

    # Contact delete
    delete_parser = subparsers.add_parser(Command.DELETE.value, help=HelpText.DELETE.value)
    delete_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    delete_parser.set_defaults(func=delete_contact)

    # Contact search
    search_parser = subparsers.add_parser(Command.SEARCH.value, help=HelpText.SEARCH.value)
    search_parser.add_argument('--' + Argument.QUERY.value, required=True, help=HelpText.ARGUMENT_QUERY.value)
    search_parser.add_argument('--' + Argument.BY.value, help=HelpText.ARGUMENT_BY.value)
    search_parser.set_defaults(func=search_contacts)

    # Phone add
    add_phone_parser = subparsers.add_parser(
        Command.ADD_PHONE.value, help=HelpText.ADD_PHONE.value
    )
    add_phone_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    add_phone_parser.add_argument('--' + Argument.PHONE.value, required=True, help=HelpText.ARGUMENT_PHONE.value)
    add_phone_parser.set_defaults(func=add_phone)

    # Phone delete
    delete_phone_parser = subparsers.add_parser(
        Command.DELETE_PHONE.value, help=HelpText.DELETE_PHONE.value
    )
    delete_phone_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    delete_phone_parser.add_argument('--' + Argument.PHONE.value, required=True, help=HelpText.ARGUMENT_PHONE.value)
    delete_phone_parser.set_defaults(func=delete_phone)

    # E-mail add
    add_email_parser = subparsers.add_parser(
        Command.ADD_EMAIL.value, help=HelpText.ADD_EMAIL.value
    )
    add_email_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    add_email_parser.add_argument('--' + Argument.EMAIL.value, required=True, help=HelpText.ARGUMENT_EMAIL.value)
    add_email_parser.set_defaults(func=add_email)

    # E-mail remove
    delete_email_parser = subparsers.add_parser(
        Command.DELETE_EMAIL.value, help=HelpText.DELETE_EMAIL.value
    )
    delete_email_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    delete_email_parser.add_argument('--' + Argument.EMAIL.value, required=True, help=HelpText.ARGUMENT_EMAIL.value)
    delete_email_parser.set_defaults(func=delete_email)

    # Address add
    add_address_parser = subparsers.add_parser(
        Command.ADD_ADDRESS.value, help=HelpText.ADD_ADDRESS.value
    )
    add_address_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    add_address_parser.add_argument('--' + Argument.ADDRESS.value, required=True, help=HelpText.ARGUMENT_ADDRESS.value)
    add_address_parser.set_defaults(func=add_address)

    # Address remove
    delete_address_parser = subparsers.add_parser(
        Command.DELETE_ADDRESS.value, help=HelpText.DELETE_ADDRESS.value
    )
    delete_address_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    delete_address_parser.add_argument('--' + Argument.ADDRESS.value, required=True, help=HelpText.ARGUMENT_ADDRESS.value)
    delete_address_parser.set_defaults(func=delete_address)

    # Tag add
    add_tag_parser = subparsers.add_parser(
        Command.ADD_TAG.value, help=HelpText.ADD_TAG.value
    )
    add_tag_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    add_tag_parser.add_argument('--' + Argument.TAG.value, required=True, help=HelpText.ARGUMENT_TAG.value)
    add_tag_parser.set_defaults(func=add_tag_to_contact)

    # Tag delete
    delete_tag_parser = subparsers.add_parser(
        Command.DELETE_TAG.value, help=HelpText.DELETE_TAG.value
    )
    delete_tag_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    delete_tag_parser.add_argument('--' + Argument.TAG.value, required=True, help=HelpText.ARGUMENT_TAG.value)
    delete_tag_parser.set_defaults(func=delete_tag_from_contact)

    # Closest aniversary
    aniversaries_parser = subparsers.add_parser(
        Command.ANIVERSARIES.value, help=HelpText.ANIVERSARIES.value
    )
    aniversaries_parser.add_argument('--' + Argument.DAYS.value, help=HelpText.ARGUMENT_DAYS.value)
    aniversaries_parser.set_defaults(func=congratulations_date)

storage_service = StorageService(SecureJsonStorage())
address_book = AddressBook(storage_service)
try:
    address_book.load()
except FileNotFoundError:
    print(Messages.NO_ADDRESS_BOOK_FOUND.value)
except Exception as e:
    print(Messages.ERROR_LOADING_ADDRESS_BOOK.value.format(e))

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

    if birthday:
        birthday = Birthday(birthday)

    if note:
        note = Note(note, address_book.tag_manager)

    contact = Contact(name, birthday, note)
    address_book.set_contact(contact)
    print(Messages.CONTACT_ADDED.value.format(name, contact.id))
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
        print(Messages.NO_PARAMETERS_FOR_EDITING.value)
        return

    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(Messages.CONTACT_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
        return

    if name:
        contact.set_name(name)

    if birthday is not None:
        contact.set_birthday(Birthday(birthday))

    if note is not None:
        contact.set_note(Note(note, address_book.tag_manager))

    address_book.set_contact(contact)
    print(Messages.CONTACT_UPDATED.value.format(getattr(args, Argument.ID.value)))
    address_book.save()

@input_error
def delete_contact(args: argparse.Namespace) -> None:
    """
    Delete a contact from the address book
    """
    address_book.remove_contact(getattr(args, Argument.ID.value))
    print(Messages.CONTACT_DELETED.value.format(getattr(args, Argument.ID.value)))
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
        print(Messages.CONTACTS_NOT_FOUND.value)

@input_error
def add_phone(args: argparse.Namespace) -> None:
    """
    Add a phone number to an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(Messages.CONTACT_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
        return

    phone = PhoneNumber(getattr(args, Argument.PHONE.value))
    contact.add_phone(phone)
    address_book.set_contact(contact)
    print(Messages.PHONE_ADDED.value.format(getattr(args, Argument.PHONE.value), getattr(args, Argument.ID.value)))
    address_book.save()

@input_error
def delete_phone(args: argparse.Namespace) -> None:
    """
    Delete a phone number from an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(Messages.CONTACT_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
        return
    phone = PhoneNumber(getattr(args, Argument.PHONE.value))
    contact.remove_phone(phone)
    address_book.set_contact(contact)
    print(Messages.PHONE_DELETED.value.format(getattr(args, Argument.PHONE.value), getattr(args, Argument.ID.value)))
    address_book.save()

@input_error
def add_email(args: argparse.Namespace) -> None:
    """
    Add an email to an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(Messages.CONTACT_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
        return

    email = EmailAddress(getattr(args, Argument.EMAIL.value))
    contact.add_email(email)
    address_book.set_contact(contact)
    print(Messages.EMAIL_ADDED.value.format(getattr(args, Argument.EMAIL.value), getattr(args, Argument.ID.value)))
    address_book.save()

@input_error
def delete_email(args: argparse.Namespace) -> None:
    """
    Delete an email from an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(Messages.CONTACT_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
        return

    email = EmailAddress(getattr(args, Argument.EMAIL.value))
    contact.remove_email(email)
    address_book.set_contact(contact)
    print(Messages.EMAIL_DELETED.value.format(getattr(args, Argument.EMAIL.value), getattr(args, Argument.ID.value)))
    address_book.save()

@input_error
def add_tag_to_contact(args: argparse.Namespace) -> None:
    """
    Add a tag to an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(Messages.CONTACT_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
        return

    contact.add_tag(getattr(args, Argument.TAG.value))
    address_book.set_contact(contact)
    print(Messages.TAG_ADDED.value.format(getattr(args, Argument.TAG.value), getattr(args, Argument.ID.value)))
    address_book.save()

@input_error
def delete_tag_from_contact(args: argparse.Namespace) -> None:
    """
    Delete a tag from an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(Messages.CONTACT_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
        return

    contact.remove_tag(getattr(args, Argument.TAG.value))
    address_book.set_contact(contact)
    print(Messages.TAG_DELETED.value.format(getattr(args, Argument.TAG.value), getattr(args, Argument.ID.value)))
    address_book.save()

@input_error
def add_address(args: argparse.Namespace) -> None:
    """
    Add an address to an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(Messages.CONTACT_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
        return

    address = Address(getattr(args, Argument.ADDRESS.value))
    contact.add_address(address)
    address_book.set_contact(contact)
    print(Messages.ADDRESS_ADDED.value.format(getattr(args, Argument.ADDRESS.value), getattr(args, Argument.ID.value)))
    address_book.save()

@input_error
def delete_address(args: argparse.Namespace) -> None:
    """
    Remove an address from an existing contact
    """
    contact = address_book.get_contact(getattr(args, Argument.ID.value))
    if not contact:
        print(Messages.CONTACT_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
        return

    address = Address(getattr(args, Argument.ADDRESS.value))
    contact.remove_address(address)
    address_book.set_contact(contact)
    print(Messages.ADDRESS_DELETED.value.format(getattr(args, Argument.ADDRESS.value), getattr(args, Argument.ID.value)))
    address_book.save()

@input_error
def congratulations_date(args: argparse.Namespace) -> None:
    """
    List contacts with birthdays in a given number of days from today
    """
    days = int(getattr(args, Argument.DAYS.value, 7) or 7)
    address_book.print_aniversaries_table(days)
