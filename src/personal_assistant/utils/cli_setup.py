"""
Module for setting up the command line interface
"""
import os
import platform
from typing import Any, Callable, Dict
import argparse
import sys
from tabulate import tabulate
from colorama import init, Fore, Back
from pyfiglet import Figlet
from personal_assistant.commands.contact_commands import handle_contact_commands
from personal_assistant.commands.note_commands import handle_note_commands

init(autoreset=True)

def setup_readline():
    """
    Setup the readline module for command line completion based on user platform
    """
    if platform.system() == 'Windows':
        try:
            import pyreadline as readline
        except ImportError:
            print("Install pyreadline package for command line completion on Windows")
            sys.exit(1)
    else:
        import readline
    return readline


def setup_parsers() -> tuple:
    """
    Setup the command line parsers.
    """
    parser = argparse.ArgumentParser(
        description="Персональний помічник для управління контактами та нотатками"
    )
    subparsers = parser.add_subparsers(dest='command', help='Доступні команди')

    parsers = {}

    # Contacts parser
    contact_parser = subparsers.add_parser('contacts', help='Керування контактами')
    handle_contact_commands(contact_parser)
    parsers['contacts'] = contact_parser

    # Notes parser
    note_parser = subparsers.add_parser('notes', help='Керування нотатками')
    handle_note_commands(note_parser)
    parsers['notes'] = note_parser

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

def get_terminal_size() -> tuple[int, int]:
    """
    Get the terminal size.
    """
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)

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

    figlet = Figlet(font='slant', width=term_width)
    welcome_text1 = figlet.renderText('Welcome To')
    welcome_text2 = figlet.renderText('BRO Assistant')

    print_centered(welcome_text1, term_width, Fore.BLACK + Back.YELLOW)
    print_centered(welcome_text2, term_width, Fore.WHITE + Back.BLUE)
    print("\n")

    headers = ["Команда", "Опис", "Параметри"]
    all_rows = []

    for name, subparser in parsers.items():
        if subparser.description:
            description = subparser.description
        else:
            description = "Немає доступного опису для цієї команди."

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

