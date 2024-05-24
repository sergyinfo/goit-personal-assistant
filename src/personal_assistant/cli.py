"""
This module is the cli module for the personal assistant application.
It parses the command line arguments and calls the appropriate functions 
based on the command and entity types.
"""
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from personal_assistant.services.cli_completer import CommandCompleter
from personal_assistant.utils.helpers import get_commands
from personal_assistant.utils.cli_setup import (
    setup_parsers,
    handle_command,
    clear_screen,
    hello_screen
)

def main() -> None:
    """
    Main function to parse the command line arguments 
    and call the appropriate functions
    """

    # Clear the screen and setup the parsers for autocomplete
    #clear_screen()
    parser, parsers = setup_parsers()
    commands = get_commands(parsers)

    session = PromptSession(completer=CommandCompleter(commands=commands))

    hello_screen(parsers)

    try:
        while True:
            user_input = session.prompt("Enter your command: ")
            if user_input.strip().lower() == 'exit':
                clear_screen()
                print("Ending program...")
                break

            # Arguments parsing
            try:
                # Clear the screen before displaying the help text
                clear_screen()

                # Show the help text each time the user enters any command
                hello_screen(parsers)

                args = parser.parse_args(user_input.split())
                handle_command(args)
            except SystemExit:
                # argparse will call sys.exit() on error
                continue
    except KeyboardInterrupt:
        clear_screen()  # Clear the screen before exiting wuth Ctrl+C
        print("Програму перервано користувачем")

if __name__ == '__main__':
    main()
