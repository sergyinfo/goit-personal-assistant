"""
This module is the cli module for the personal assistant application.
It parses the command line arguments and calls the appropriate functions 
based on the command and entity types.
"""
from personal_assistant.utils.helpers import get_commands
from personal_assistant.utils.cli_setup import (
    setup_parsers,
    setup_readline,
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
    clear_screen()
    readline = setup_readline()
    parser, parsers = setup_parsers()
    commands = get_commands(parsers)

    def complete(text, state):
        buffer = readline.get_line_buffer()
        stripped_buffer = buffer.strip()

        # If the buffer is empty or the text is empty, show all commands
        if not stripped_buffer and text == '':
            completions = sorted(commands)  # Sort the commands
        else:
            # Trim the buffer to get the base command
            parts = buffer.strip().split()

            # Get the base command and the sub-command part
            base_command = parts[0] if parts else ''
            if len(parts) > 1:
                sub_command_part = ' '.join(parts[1:])
            else:
                sub_command_part = ''

            if not text:
                # User hit tab without typing anything
                filtered_commands = [
                    cmd for cmd in commands if cmd.startswith(base_command + ' ' + sub_command_part)
                ]
            else:
                # Filter the commands based on the text
                filtered_commands = [
                    cmd for cmd in commands if cmd.startswith(buffer.rstrip())
                ]

            completions = [command[len(buffer) - len(text):] for command in filtered_commands]
        return completions[state] if state < len(completions) else None

    readline.set_completer(complete)
    readline.parse_and_bind('tab: complete')
    hello_screen(parsers)

    try:
        while True:
            user_input = input("Enter your command: ")
            if user_input.strip().lower() == 'exit':
                clear_screen()
                print("Завершення програми...")
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
