"""
Helper functions for the Personal Assistant.
"""
import os
import platform
import argparse
from tabulate import tabulate
from typing import List, Dict, Any
from colorama import init, Fore, Back
from pyfiglet import Figlet
from personal_assistant.commands.contact_commands import handle_contact_commands
from personal_assistant.commands.note_commands import handle_note_commands

init(autoreset=True)
print(Back.RED)

def get_terminal_size():
    """
    Get the terminal size.
    """
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)

def print_centered(text, term_width, color):
    """
    Print the text centered in the terminal.
    """
    lines = text.split('\n')
    for line in lines:
        # Вирівнюємо текст по центру
        print(color + line.center(term_width))


def clear_screen():
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
