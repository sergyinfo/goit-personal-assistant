"""
Helper functions for the Personal Assistant.
"""

import argparse
from typing import Dict

def get_commands(parsers: Dict[str, argparse.ArgumentParser]) -> list[str]:
    """
    Recursively get commands from each subparser.
    """
    commands = []
    for name, parser in parsers.items():
        sub_commands = _get_commands_from_parser(parser, prefix=name)
        commands.extend(sub_commands)
    return commands

def _get_commands_from_parser(parser: Dict, prefix: str = '') -> list[str]:
    """
    Helper function to recursively get commands.
    """
    local_commands = []
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for choice, subparser in action.choices.items():
                cmd = f"{prefix} {choice}" if prefix else choice
                local_commands.append(cmd)
                local_commands.extend(_get_commands_from_parser(subparser, prefix=cmd))
    return local_commands

def to_comma_separated_string(items):
    """
    Convert a list of items to a comma-separated string.
    """
    return ", ".join(str(item) for item in items)
