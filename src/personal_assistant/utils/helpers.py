"""
Helper functions for the Personal Assistant.
"""

import argparse
from typing import Dict

def get_commands(parsers: Dict[str, argparse.ArgumentParser]) -> list[str]:
    """ Рекурсивно отримує команди з кожного субпарсера. """
    commands = []
    for name, parser in parsers.items():
        sub_commands = _get_commands_from_parser(parser, prefix=name)
        commands.extend(sub_commands)
    print(commands)
    return commands

def _get_commands_from_parser(parser: Dict, prefix: str = '') -> list[str]:
    """ Допоміжна функція для рекурсивного отримання команд. """
    local_commands = []
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for choice, subparser in action.choices.items():
                cmd = f"{prefix} {choice}" if prefix else choice
                local_commands.append(cmd)
                local_commands.extend(_get_commands_from_parser(subparser, prefix=cmd))
    return local_commands
