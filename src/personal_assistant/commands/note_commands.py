"""
Functionality for note commands
"""
import argparse

from tabulate import tabulate
from colorama import Fore, Style
from personal_assistant.enums.command_types import Command
from personal_assistant.models.note import Note
from personal_assistant.services.notebook import Notebook
from personal_assistant.services.storage.secure_json_storage import SecureJsonStorage
from personal_assistant.services.storage_service import StorageService
from personal_assistant.utils.decorators import input_error

def handle_note_commands(parser: argparse.ArgumentParser) -> None:
    """
    Add subparsers for note commands
    """
    subparsers = parser.add_subparsers(dest='note_command', help='Команди для керування нотатками')

    # Add note
    add_parser = subparsers.add_parser(Command.ADD.value, help='Додати нотатку')
    add_parser.add_argument('--content', required=True, help='Зміст нотатки', nargs='+')
    add_parser.set_defaults(func=add_note)

    # Edit note
    edit_parser = subparsers.add_parser(Command.EDIT.value, help='Редагувати нотатку')
    edit_parser.add_argument('--id', required=True, help='ID нотатки')
    edit_parser.add_argument('--content', required=True, help='Новий зміст нотатки', nargs='+')
    edit_parser.set_defaults(func=edit_note)

    # Delete note
    delete_parser = subparsers.add_parser(Command.DELETE.value, help='Видалити нотатку')
    delete_parser.add_argument('--id', required=True, help='ID нотатки')
    delete_parser.set_defaults(func=delete_note)

    # Search notes
    search_parser = subparsers.add_parser(Command.SEARCH.value, help='Пошук нотаток')
    search_parser.add_argument('--content', help='Текст для пошуку в нотатках', nargs='+')
    search_parser.add_argument('--tag', help='Тег для фільтрації нотаток')
    search_parser.add_argument('--id', help='ID для фільтрації нотаток')
    search_parser.set_defaults(func=search_notes)

    # Add tag to note
    add_tag_parser = subparsers.add_parser(Command.ADD_TAG.value, help='Додати тег до нотатки')
    add_tag_parser.add_argument('--id', required=True, help='ID нотатки')
    add_tag_parser.add_argument('--tag', required=True, help='Тег для додавання')
    add_tag_parser.set_defaults(func=add_tag_to_note)

    # Delete tag from note
    delete_tag_parser = subparsers.add_parser(Command.DELETE_TAG.value, help='Видалити тег з нотатки')
    delete_tag_parser.add_argument('--id', required=True, help='ID нотатки')
    delete_tag_parser.add_argument('--tag', required=True, help='Тег для видалення')
    delete_tag_parser.set_defaults(func=delete_tag_from_note)

    # Archive note
    archive_parser = subparsers.add_parser(Command.ARCHIVE.value, help='Заархівувати нотатку')
    archive_parser.add_argument('--id', required=True, help='ID нотатки')
    archive_parser.set_defaults(func=archive_note)

    # Restore note
    restore_parser = subparsers.add_parser(Command.RESTORE.value, help='Розархівувати нотатку')
    restore_parser.add_argument('--id', required=True, help='ID нотатки')
    restore_parser.set_defaults(func=restore_note)

    # View active notes
    view_active_parser = subparsers.add_parser(Command.VIEW_ACTIVE.value, help='Показати всі не заархівовані нотатки')
    view_active_parser.set_defaults(func=view_active_notes)

    # View archived notes
    view_archived_parser = subparsers.add_parser(Command.VIEW_ARCHIVED.value, help='Показати всі заархівовані нотатки')
    view_archived_parser.set_defaults(func=view_archived_notes)

    # View note's history
    view_history_parser = subparsers.add_parser(Command.VIEW_HISTORY.value, help='Переглянути історію нотатки')
    view_history_parser.add_argument('--id', required=True, help='ID нотатки')
    view_history_parser.set_defaults(func=view_note_history)

storage_service = StorageService(SecureJsonStorage())
notebook = Notebook(storage_service)

try:
    print("Loading notebook...")
    notebook.load()
except FileNotFoundError:
    print("No notebook found. Creating a new one.")
except Exception as e:
    print(f"An error occurred while loading the notebook: {e}")

@input_error
def add_note(args: argparse.Namespace) -> None:
    """Add a new note to the notebook"""
    content = ' '.join(args.content)
    note = Note(text=content, tag_manager=notebook.tag_manager)
    notebook.add_note(note)
    print(f"Note added: {note.text} | ID: {note.note_id}")
    notebook.save()

@input_error
def edit_note(args: argparse.Namespace) -> None:
    """Edit a note in the notebook by ID"""
    content = ' '.join(args.content)
    notebook.update_note_text(args.id, content)
    print(f"Note {args.id} updated.")  
    notebook.save()

@input_error
def delete_note(args: argparse.Namespace) -> None:
    """Delete a note from the notebook by ID"""
    notebook.remove_note(args.id)
    print(f"Note with ID {args.id} deleted.")
    notebook.save()

@input_error
def search_notes(args: argparse.Namespace) -> None:
    """Search notes by content or tag or ID"""
    content = ' '.join(args.content) if args.content else None
    tag = args.tag if args.tag else None
    note_id = args.id if args.id else None
    print(f"Searching notes... Content: {content}, Tag: {tag}, ID: {id}")
    
    notes = []
    if content:
        notes = notebook.find_note_by_content(content)
    elif tag:
        notes = notebook.find_notes_by_tag(tag)
    elif note_id:
        note = notebook.find_note_by_id(note_id)
        notes = [note] if note else []

    if len(notes):
        print("Found notes:")
        table = [[note.note_id, note.text, note.created_at, note.updated_at, note.tags, note.is_archived] for note in notes]
        headers = [
            f"{Fore.YELLOW}ID{Style.RESET_ALL}", 
            f"{Fore.BLUE}Text{Style.RESET_ALL}", 
            f"{Fore.BLUE}Created At{Style.RESET_ALL}", 
            f"{Fore.BLUE}Updated At{Style.RESET_ALL}", 
            f"{Fore.YELLOW}Tags{Style.RESET_ALL}", 
            f"{Fore.RED}Archived{Style.RESET_ALL}"
        ]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("No notes found by your request.")

@input_error
def add_tag_to_note(args: argparse.Namespace) -> None:
    """Add a tag to a note by ID"""
    print(f"Adding tag {args.tag} to note {args.id}")
    note = notebook.find_note_by_id(args.id)
    if note:
        note.add_tag(args.tag)
        print(f"Tag {args.tag} added to note {args.id}.")
    notebook.save()

@input_error
def delete_tag_from_note(args: argparse.Namespace) -> None:
    print(f"Deleting tag {args.tag} from note {args.id}")
    note = notebook.find_note_by_id(args.id)
    if note:
        note.remove_tag(args.tag)
        print(f"Tag {args.tag} removed from note {args.id}.")
    notebook.save()

@input_error
def archive_note(args: argparse.Namespace) -> None:
    """Archive a note by ID"""
    note = notebook.find_note_by_id(args.id)
    if note:
        note.archive()
        print(f"Note {args.id} archived.")
    notebook.save()

@input_error
def restore_note(args: argparse.Namespace) -> None:
    """Restore a note by ID"""
    note = notebook.find_note_by_id(args.id)
    if note:
        note.restore()
        print(f"Note with ID {args.id} restored.")
    notebook.save()

@input_error
def view_active_notes(args: argparse.Namespace) -> None:
    """View all active notes"""
    active_notes = [note for note in notebook.notes.values() if not note.is_archived]
    if len(active_notes):
        print("Active notes:")
        table = [[note.note_id, note.text, note.created_at, note.updated_at, note.tags] for note in active_notes]
        headers = [f"{Fore.YELLOW}ID{Style.RESET_ALL}", f"{Fore.BLUE}Text{Style.RESET_ALL}", f"{Fore.BLUE}Created At{Style.RESET_ALL}", f"{Fore.BLUE}Updated At{Style.RESET_ALL}", f"{Fore.YELLOW}Tags{Style.RESET_ALL}"]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("No active notes found.")

@input_error
def view_archived_notes(args: argparse.Namespace) -> None:
    """View all archived notes"""
    archived_notes = [note for note in notebook.notes.values() if note.is_archived]
    if len(archived_notes):
        print("Archived notes:")
        table = [[note.note_id, note.text, note.created_at, note.updated_at, note.tags] for note in archived_notes]
        headers = [f"{Fore.YELLOW}ID{Style.RESET_ALL}", f"{Fore.BLUE}Text{Style.RESET_ALL}", f"{Fore.BLUE}Created At{Style.RESET_ALL}", f"{Fore.BLUE}Updated At{Style.RESET_ALL}", f"{Fore.YELLOW}Tags{Style.RESET_ALL}"]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("No archived notes found.")

@input_error
def view_note_history(args: argparse.Namespace) -> None:
    """View the history of a note by ID"""
    note = notebook.find_note_by_id(args.id)
    if note:
        history = note.get_history()
        if history:
            print(f"History for note with ID: {args.id}:")
            table = [[entry.timestamp, entry.previous_text, entry.new_text] for entry in history]
            headers = [f"{Fore.GREEN}Timestamp{Style.RESET_ALL}", f"{Fore.RED}Previous Text{Style.RESET_ALL}", f"{Fore.CYAN}New Text{Style.RESET_ALL}"]
            print(tabulate(table, headers=headers, tablefmt="grid"))
        else:
            print(f"No history found for note {args.id}.")
    else:
        print(f"Note {args.id} not found.")
