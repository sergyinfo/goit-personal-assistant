"""
Functionality for note commands
"""
import argparse
from personal_assistant.enums.command_types import Command

def handle_note_commands(parser: argparse.ArgumentParser) -> None:
    """
    Add subparsers for note commands
    """
    subparsers = parser.add_subparsers(dest='note_command', help='Команди для керування нотатками')

    # Add note
    add_parser = subparsers.add_parser(Command.ADD.value, help='Додати нотатку')
    add_parser.add_argument('--content', required=True, help='Зміст нотатки')
    add_parser.set_defaults(func=add_note)

    # Edit note
    edit_parser = subparsers.add_parser(Command.EDIT.value, help='Редагувати нотатку')
    edit_parser.add_argument('--id', required=True, help='ID нотатки')
    edit_parser.add_argument('--content', required=True, help='Новий зміст нотатки')
    edit_parser.set_defaults(func=edit_note)

    # Delete note
    delete_parser = subparsers.add_parser(Command.DELETE.value, help='Видалити нотатку')
    delete_parser.add_argument('--id', required=True, help='ID нотатки')
    delete_parser.set_defaults(func=delete_note)

    # Search notes
    search_parser = subparsers.add_parser(Command.SEARCH.value, help='Пошук нотаток')
    search_parser.add_argument('--content', help='Текст для пошуку в нотатках')
    search_parser.add_argument('--tag', help='Тег для фільтрації нотаток')
    search_parser.set_defaults(func=search_notes)

    # Add tag to note
    add_tag_parser = subparsers.add_parser(Command.ADD_TAG.value, help='Додати тег до нотатки')
    add_tag_parser.add_argument('--id', required=True, help='ID нотатки')
    add_tag_parser.add_argument('--tag', required=True, help='Тег для додавання')
    add_tag_parser.set_defaults(func=add_tag_to_note)

    # Delete tag from note
    delete_tag_parser = subparsers.add_parser(
        Command.DELETE_TAG.value, help='Видалити тег з нотатки'
    )
    delete_tag_parser.add_argument('--id', required=True, help='ID нотатки')
    delete_tag_parser.add_argument('--tag', required=True, help='Тег для видалення')
    delete_tag_parser.set_defaults(func=delete_tag_from_note)

def add_note(args: argparse.Namespace) -> None:
    print(f"Adding note with content: {args.content}")
    pass

def edit_note(args: argparse.Namespace) -> None:
    print(f"Editing note {args.id} to new content: {args.content}")
    pass

def delete_note(args: argparse.Namespace) -> None:
    print(f"Deleting note {args.id}")
    pass

def search_notes(args: argparse.Namespace) -> None:
    content = args.content if args.content else 'any'
    tag = args.tag if args.tag else 'any'
    print(f"Searching notes by content: {content} and tag: {tag}")
    pass

def add_tag_to_note(args: argparse.Namespace) -> None:
    print(f"Adding tag {args.tag} to note {args.id}")
    pass

def delete_tag_from_note(args: argparse.Namespace) -> None:
    print(f"Deleting tag {args.tag} from note {args.id}")
    pass