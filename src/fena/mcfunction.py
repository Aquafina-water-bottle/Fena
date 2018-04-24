import os
import logging

from command_builder import CommandBuilder
from lexical_token import Token
from token_types import TokenType

class McFunctionBuilder:
    """
    Contains all commands within a single defined mcfunction

    Args:
        path (str): Full path to the mcfunction
        commands (list of Tokens with TokenType.COMMAND)

    Attributes:
        path (str): Full path to the mcfunction file
        commands (list): Commands in the mcfunction
    """
    
    def __init__(self, path):
        self.path = path
        self.commands = []

    def add_command(self, command):
        """
        Adds the given command to the commands list

        Args:
            command (Token with TokenType.COMMAND)
        """
        assert isinstance(command, Token)
        assert command.matches(TokenType.COMMAND)
        self.commands.append(command)

    def build(self):
        new_function = McFunction(self.path)
        for cmd_str in self.commands:
            command = CommandBuilder(cmd_str)
            new_function.add_command(command.build())

        return new_function

    def __str__(self):
        return "McFunctionBuilder[{}]".format(repr(self.path))

    def __repr__(self):
        return "McFunctionBuilder[path={}, commands={}]".format(repr(self.path), self.commands)

class McFunction:
    def __init__(self, path):
        self.path = path
        self.commands = []

    def add_command(self, command):
        """
        Adds the given command to the commands list

        Args:
            command (Token with TokenType.COMMAND)
        """
        assert isinstance(command, Token)
        assert command.matches(TokenType.COMMAND)
        self.commands.append(command)
