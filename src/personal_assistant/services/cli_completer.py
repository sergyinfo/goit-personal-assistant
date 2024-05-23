"""
This module contains the CommandCompleter class 
which is used to handle command completion in the CLI
"""
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

class CommandCompleter(Completer):
    """
    Completer class to handle command completion
    """
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document: Document, complete_event):
        """
        Get completions based on the current input
        """
        text_before_cursor = document.text_before_cursor
        words = text_before_cursor.split()

        # Determine the current 'base' of the command to filter relevant suggestions
        base_command = ' '.join(words[:-1]) if len(words) > 1 else ''
        base_command_len = len(base_command)

        # Filter commands that start with the current base command
        completions = [
            command for command in self.commands if command.startswith(text_before_cursor.strip())
        ]

        # If the last word is the beginning of new command part, 
        #reset base command and adjust the start position
        if text_before_cursor.endswith(' '):
            base_command = text_before_cursor
            base_command_len += 1  # Include space in length calculation

        for completion in completions:
            # Only add the completion suffix that's not yet typed
            if completion.startswith(base_command) and completion != base_command:
                completion_suffix = completion[base_command_len:].lstrip()
                yield Completion(completion_suffix, start_position=-len(words[-1]) if words else 0)

