"""
This module is the cli module for the personal assistant application.
It parses the command line arguments and calls the appropriate functions 
based on the command and entity types.
"""
import argparse
from personal_assistant.enums.command_types import Entity
from personal_assistant.commands.contact_commands import handle_contact_commands
from personal_assistant.commands.note_commands import handle_note_commands
from personal_assistant.utils.helpers import clear_screen, hello_screen

def setup_parsers():
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

def main() -> None:
    """
    Main function to parse the command line arguments 
    and call the appropriate functions
    """

    # Очищення екрану і виведення заставки один раз перед початком вводу
    clear_screen()
    parser, parsers = setup_parsers()
    hello_screen(parsers)

    try:
        while True:
            user_input = input("Enter your command: ")
            if user_input.strip().lower() == 'exit':
                clear_screen()
                print("Завершення програми...")
                break

            # Обробка введених аргументів
            try:
                # Очищення екрану перед виконанням будь-якої команди
                clear_screen()

                # Повторний вивід заставки після очищення екрану
                hello_screen(parsers)

                args = parser.parse_args(user_input.split())
                if hasattr(args, 'func'):
                    args.func(args)
            except SystemExit:
                # argparse викликає SystemExit, якщо команда виконана або потрібно показати допомогу
                continue
    except KeyboardInterrupt:
        clear_screen()  # Очистити екран у випадку переривання Ctrl+C
        print("Програму перервано користувачем")

if __name__ == '__main__':
    main()
