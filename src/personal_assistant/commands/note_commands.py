"""
Functionality for note commands
"""
import argparse
from tabulate import tabulate
from colorama import Fore, Style
from personal_assistant.enums.command_types import Command, Argument, HelpText, Messages
from personal_assistant.models.note import Note
from personal_assistant.services.notebook import Notebook
from personal_assistant.services.storage.secure_json_storage import SecureJsonStorage
from personal_assistant.services.storage_service import StorageService
from personal_assistant.utils.decorators import input_error

def handle_note_commands(parser: argparse.ArgumentParser) -> None:
    """
    Add subparsers for note commands
    """
    subparsers = parser.add_subparsers(dest='note_command', help=HelpText.NOTE_COMMANDS.value)

    # Add note
    add_parser = subparsers.add_parser(Command.ADD.value, help=HelpText.ADD_NOTE.value)
    add_parser.add_argument('--' + Argument.CONTENT.value, required=True, help=HelpText.ARGUMENT_CONTENT.value, nargs='+')
    add_parser.set_defaults(func=add_note)

    # Edit note
    edit_parser = subparsers.add_parser(Command.EDIT.value, help=HelpText.EDIT_NOTE.value)
    edit_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    edit_parser.add_argument('--' + Argument.CONTENT.value, required=True, help=HelpText.ARGUMENT_CONTENT.value, nargs='+')
    edit_parser.set_defaults(func=edit_note)

    # Delete note
    delete_parser = subparsers.add_parser(Command.DELETE.value, help=HelpText.DELETE_NOTE.value)
    delete_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    delete_parser.set_defaults(func=delete_note)

    # Search notes
    search_parser = subparsers.add_parser(Command.SEARCH.value, help=HelpText.SEARCH_NOTE.value)
    search_parser.add_argument('--' + Argument.CONTENT.value, help=HelpText.ARGUMENT_SEARCH_CONTENT.value, nargs='+')
    search_parser.add_argument('--' + Argument.TAG.value, help=HelpText.ARGUMENT_SEARCH_TAG.value)
    search_parser.add_argument('--' + Argument.ID.value, help=HelpText.ARGUMENT_ID.value)
    search_parser.set_defaults(func=search_notes)

    # Add tag to note
    add_tag_parser = subparsers.add_parser(Command.ADD_TAG.value, help=HelpText.ADD_TAG_NOTE.value)
    add_tag_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    add_tag_parser.add_argument('--' + Argument.TAG.value, required=True, help=HelpText.ARGUMENT_TAG.value)
    add_tag_parser.set_defaults(func=add_tag_to_note)

    # Delete tag from note
    delete_tag_parser = subparsers.add_parser(Command.DELETE_TAG.value, help=HelpText.DELETE_TAG_NOTE.value)
    delete_tag_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    delete_tag_parser.add_argument('--' + Argument.TAG.value, required=True, help=HelpText.ARGUMENT_TAG.value)
    delete_tag_parser.set_defaults(func=delete_tag_from_note)

    # Archive note
    archive_parser = subparsers.add_parser(Command.ARCHIVE.value, help=HelpText.ARCHIVE_NOTE.value)
    archive_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    archive_parser.set_defaults(func=archive_note)

    # Restore note
    restore_parser = subparsers.add_parser(Command.RESTORE.value, help=HelpText.RESTORE_NOTE.value)
    restore_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    restore_parser.set_defaults(func=restore_note)

    # View active notes
    view_active_parser = subparsers.add_parser(Command.VIEW_ACTIVE.value, help=HelpText.VIEW_ACTIVE_NOTES.value)
    view_active_parser.set_defaults(func=view_active_notes)

    # View archived notes
    view_archived_parser = subparsers.add_parser(Command.VIEW_ARCHIVED.value, help=HelpText.VIEW_ARCHIVED_NOTES.value)
    view_archived_parser.set_defaults(func=view_archived_notes)

    # View note's history
    view_history_parser = subparsers.add_parser(Command.VIEW_HISTORY.value, help=HelpText.VIEW_HISTORY_NOTE.value)
    view_history_parser.add_argument('--' + Argument.ID.value, required=True, help=HelpText.ARGUMENT_ID.value)
    view_history_parser.set_defaults(func=view_note_history)

storage_service = StorageService(SecureJsonStorage())
notebook = Notebook(storage_service)

try:
    print(Messages.LOADING_NOTEBOOK.value)
    notebook.load()
except FileNotFoundError:
    print(Messages.NO_NOTEBOOK_FOUND.value)
except Exception as e:
    print(Messages.ERROR_LOADING_NOTEBOOK.value.format(e))

@input_error
def add_note(args: argparse.Namespace) -> None:
    """Add a new note to the notebook"""
    content = ' '.join(getattr(args, Argument.CONTENT.value))
    note = Note(text=content, tag_manager=notebook.tag_manager)
    notebook.add_note(note)
    print(Messages.NOTE_ADDED.value.format(note.text, note.note_id))
    notebook.save()

@input_error
def edit_note(args: argparse.Namespace) -> None:
    """Edit a note in the notebook by ID"""
    content = ' '.join(getattr(args, Argument.CONTENT.value))
    notebook.update_note_text(getattr(args, Argument.ID.value), content)
    print(Messages.NOTE_UPDATED.value.format(getattr(args, Argument.ID.value)))
    notebook.save()

@input_error
def delete_note(args: argparse.Namespace) -> None:
    """Delete a note from the notebook by ID"""
    notebook.remove_note(getattr(args, Argument.ID.value))
    print(Messages.NOTE_DELETED.value.format(getattr(args, Argument.ID.value)))
    notebook.save()

@input_error
def search_notes(args: argparse.Namespace) -> None:
    """Search notes by content or tag or ID"""
    content = ' '.join(getattr(args, Argument.CONTENT.value)) if getattr(args, Argument.CONTENT.value) else None
    tag = getattr(args, Argument.TAG.value) if getattr(args, Argument.TAG.value) else None
    note_id = getattr(args, Argument.ID.value) if getattr(args, Argument.ID.value) else None
    print(Messages.SEARCHING_NOTES.value.format(content, tag, note_id))
    
    notes = []
    if content:
        notes = notebook.find_note_by_content(content)
    elif tag:
        notes = notebook.find_notes_by_tag(tag)
    elif note_id:
        note = notebook.find_note_by_id(note_id)
        notes = [note] if note else []

    if notes:
        print(Messages.FOUND_NOTES.value)
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
        print(Messages.NO_NOTES_FOUND.value)

@input_error
def add_tag_to_note(args: argparse.Namespace) -> None:
    """Add a tag to a note by ID"""
    print(Messages.ADDING_TAG.value.format(getattr(args, Argument.TAG.value), getattr(args, Argument.ID.value)))
    note = notebook.find_note_by_id(getattr(args, Argument.ID.value))
    if note:
        note.add_tag(getattr(args, Argument.TAG.value))
        print(Messages.TAG_ADDED_TO_NOTE.value.format(getattr(args, Argument.TAG.value), getattr(args, Argument.ID.value)))
    notebook.save()

@input_error
def delete_tag_from_note(args: argparse.Namespace) -> None:
    print(Messages.DELETING_TAG.value.format(getattr(args, Argument.TAG.value), getattr(args, Argument.ID.value)))
    note = notebook.find_note_by_id(getattr(args, Argument.ID.value))
    if note:
        note.remove_tag(getattr(args, Argument.TAG.value))
        print(Messages.TAG_DELETED_FROM_NOTE.value.format(getattr(args, Argument.TAG.value), getattr(args, Argument.ID.value)))
    notebook.save()

@input_error
def archive_note(args: argparse.Namespace) -> None:
    """Archive a note by ID"""
    note = notebook.find_note_by_id(getattr(args, Argument.ID.value))
    if note:
        note.archive()
        print(Messages.NOTE_ARCHIVED.value.format(getattr(args, Argument.ID.value)))
    notebook.save()

@input_error
def restore_note(args: argparse.Namespace) -> None:
    """Restore a note by ID"""
    note = notebook.find_note_by_id(getattr(args, Argument.ID.value))
    if note:
        note.restore()
        print(Messages.NOTE_RESTORED.value.format(getattr(args, Argument.ID.value)))
    notebook.save()

@input_error
def view_active_notes(args: argparse.Namespace) -> None:
    """View all active notes"""
    active_notes = [note for note in notebook.notes.values() if not note.is_archived]
    if active_notes:
        print(Messages.ACTIVE_NOTES.value)
        table = [[note.note_id, note.text, note.created_at, note.updated_at, note.tags] for note in active_notes]
        headers = [f"{Fore.YELLOW}ID{Style.RESET_ALL}", f"{Fore.BLUE}Text{Style.RESET_ALL}", f"{Fore.BLUE}Created At{Style.RESET_ALL}", f"{Fore.BLUE}Updated At{Style.RESET_ALL}", f"{Fore.YELLOW}Tags{Style.RESET_ALL}"]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print(Messages.NO_ACTIVE_NOTES.value)

@input_error
def view_archived_notes(args: argparse.Namespace) -> None:
    """View all archived notes"""
    archived_notes = [note for note in notebook.notes.values() if note.is_archived]
    if archived_notes:
        print(Messages.ARCHIVED_NOTES.value)
        table = [[note.note_id, note.text, note.created_at, note.updated_at, note.tags] for note in archived_notes]
        headers = [f"{Fore.YELLOW}ID{Style.RESET_ALL}", f"{Fore.BLUE}Text{Style.RESET_ALL}", f"{Fore.BLUE}Created At{Style.RESET_ALL}", f"{Fore.BLUE}Updated At{Style.RESET_ALL}", f"{Fore.YELLOW}Tags{Style.RESET_ALL}"]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print(Messages.NO_ARCHIVED_NOTES.value)

@input_error
def view_note_history(args: argparse.Namespace) -> None:
    """View the history of a note by ID"""
    note = notebook.find_note_by_id(getattr(args, Argument.ID.value))
    if note:
        history = note.get_history()
        if history:
            print(Messages.HISTORY_FOR_NOTE.value.format(getattr(args, Argument.ID.value)))
            table = [[entry.timestamp, entry.previous_text, entry.new_text] for entry in history]
            headers = [f"{Fore.GREEN}Timestamp{Style.RESET_ALL}", f"{Fore.RED}Previous Text{Style.RESET_ALL}", f"{Fore.CYAN}New Text{Style.RESET_ALL}"]
            print(tabulate(table, headers=headers, tablefmt="grid"))
        else:
            print(Messages.NO_HISTORY_FOR_NOTE.value.format(getattr(args, Argument.ID.value)))
    else:
        print(Messages.NOTE_NOT_FOUND.value.format(getattr(args, Argument.ID.value)))
