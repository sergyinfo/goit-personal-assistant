"""
Module for contact commands
"""
import argparse
from personal_assistant.enums.command_types import Command

def handle_contact_commands(parser: argparse.ArgumentParser) -> None:
    """
    Add subparsers for contact commands
    """
    subparsers = parser.add_subparsers(
        dest='contact_command', help='Команди для керування контактами'
    )

    # Contact add
    add_parser = subparsers.add_parser(Command.ADD.value, help='Додати контакт')
    add_parser.add_argument('--name', required=True, help='Ім\'я контакту')
    add_parser.set_defaults(func=add_contact)

    # Contact edit
    edit_parser = subparsers.add_parser(Command.EDIT.value, help='Редагувати контакт')
    edit_parser.add_argument('--id', required=True, help='ID контакта для редагування')
    edit_parser.add_argument('--name', help='Нове ім\'я контакту')
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

def add_contact(args: argparse.Namespace) -> None:
    print(f"Adding contact: {args.name}")
    pass

def edit_contact(args: argparse.Namespace) -> None:
    print(f"Editing contact {args.id} to new name {args.name if args.name else 'not provided'}")
    pass

def delete_contact(args: argparse.Namespace) -> None:
    print(f"Deleting contact {args.id}")
    pass

def search_contacts(args: argparse.Namespace) -> None:
    print(f"Searching contacts by name: {args.name if args.name else 'any'}, email: {args.email if args.email else 'any'}, phone: {args.phone if args.phone else 'any'}")
    pass

def add_phone(args: argparse.Namespace) -> None:
    print(f"Adding phone {args.phone} to contact {args.id}")
    pass

def delete_phone(args: argparse.Namespace) -> None:
    print(f"Deleting phone {args.phone} from contact {args.id}")
    pass

def add_email(args: argparse.Namespace) -> None:
    print(f"Adding email {args.email} to contact {args.id}")
    pass

def delete_email(args: argparse.Namespace) -> None:
    print(f"Deleting email {args.email} from contact {args.id}")
    pass

def add_tag_to_contact(args: argparse.Namespace) -> None:
    print(f"Adding tag {args.tag} to contact {args.id}")
    pass

def delete_tag_from_contact(args: argparse.Namespace) -> None:
    print(f"Deleting tag {args.tag} from contact {args.id}")
    pass
