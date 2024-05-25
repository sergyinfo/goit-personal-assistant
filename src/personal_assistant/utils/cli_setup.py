"""
Module for setting up the command line interface
"""
import os
import platform
import shutil
from typing import Dict, Tuple
import argparse
from tabulate import tabulate
from colorama import init, Fore, Back
from pyfiglet import Figlet
from personal_assistant.commands.contact_commands import handle_contact_commands
from personal_assistant.commands.note_commands import handle_note_commands
from personal_assistant.enums.military_command_types import Entity

init(autoreset=True)

def setup_parsers() -> Tuple[argparse.ArgumentParser, Dict[str, argparse.ArgumentParser]]:
    """
    Setup the command line parsers.
    """
    parser = argparse.ArgumentParser(
        description="Персональний помічник для управління контактами та нотатками"
    )
    subparsers = parser.add_subparsers(dest='command', help='Доступні команди')

    parsers = {}

    # Contacts parser
    contact_parser = subparsers.add_parser(Entity.CONTACT.value, description='Керування контактами')
    handle_contact_commands(contact_parser)
    parsers[Entity.CONTACT.value] = contact_parser

    # Notes parser
    note_parser = subparsers.add_parser(Entity.NOTE.value, description='Керування нотатками')
    handle_note_commands(note_parser)
    parsers[Entity.NOTE.value] = note_parser

    return parser, parsers

def handle_command(args: argparse.Namespace) -> None:
    """
    Handle the command based on the command and entity types.
    """
    if hasattr(args, 'func'):
        args.func(args)
    else:
        # Handle unknown command or show help
        print("Unknown command. Use 'help' to see available commands.")

def get_terminal_size() -> Tuple[int, int]:
    """
    Get the terminal size.
    Returns:
        Tuple[int, int]: A tuple containing the number of rows and columns of the terminal.
    """
    try:
        columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    except Exception as e:
        print(f"Failed to get terminal size: {e}")
        columns, rows = (80, 24)  # Fallback if there's an error
    return rows, columns 

def print_centered(text, term_width, color) -> None:
    """
    Print the text centered in the terminal.
    """
    lines = text.split('\n')
    for line in lines:
        # Align text to the center
        print(color + line.center(term_width))

def clear_screen() -> None:
    """
    Clear the terminal screen.
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        os.system('cls')
    else:
        os.system('clear')

def hello_screen(parsers: Dict[str, argparse.ArgumentParser]) -> None:
    """
    Print the welcome screen.
    """
    _, term_width = get_terminal_size()

    # figlet = Figlet(font='starwars', width=term_width)
    figlet = Figlet(font='larry3d', width=term_width)
    welcome_text1 = figlet.renderText('Welcome To')
    welcome_text2 = figlet.renderText('BRO Assistant')

    print_centered(welcome_text1, term_width, Fore.WHITE + Back.BLUE)
    print_centered(welcome_text2, term_width, Fore.BLACK + Back.YELLOW)
    print("\n")

    headers = ["Команда", "Опис", "Параметри"]
    all_rows = []

    for name, subparser in parsers.items():
        description = subparser.description or "Немає доступного опису для цієї команди."
        command_options = []
        for action in subparser._actions:
            if isinstance(action, argparse._SubParsersAction):
                for choice, subsubparser in action.choices.items():
                    command_options.append(f"{choice} {subsubparser.format_usage()}")
            else:
                options = ', '.join(action.option_strings)
                help_string = action.help or "Без опису"
                command_options.append(f"{options}: {help_string}")

        # Зберігаємо інформацію про кожну команду в один список
        all_rows.append([name, description, "\n".join(command_options)])

    # Генеруємо та виводимо єдину таблицю
    table = tabulate(all_rows, headers, tablefmt="grid")
    table_lines = table.split('\n')
    for line in table_lines:
        print(line.center(term_width))
    print("\n")
