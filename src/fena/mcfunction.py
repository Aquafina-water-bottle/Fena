# import logging
# import os

# from command_builder import CommandBuilder
# from lexical_token import Token
# from token_types import TokenType

# class McFunctionBuilder:
#     """
#     Contains all commands within a single defined mcfunction
# 
#     Args:
#         path (str): Full path to the mcfunction
#         commands (list of Tokens with TokenType.COMMAND)
# 
#     Attributes:
#         path (str): Full path to the mcfunction file
#         commands (list): Commands in the mcfunction
#     """
#     
#     def __init__(self, path):
#         self.path = path
#         self.commands = []
# 
#     def add_command(self, command):
#         """
#         Adds the given command to the commands list
# 
#         Args:
#             command (Token with TokenType.COMMAND)
#         """
#         assert isinstance(command, Token)
#         assert command.matches(TokenType.COMMAND)
#         self.commands.append(command)
# 
#     def build(self):
#         new_function = McFunction(self.path)
#         for cmd_str in self.commands:
#             command = CommandBuilder(cmd_str)
#             new_function.add_command(command.build())
# 
#         return new_function
# 
#     def __str__(self):
#         return "McFunctionBuilder[{}]".format(repr(self.path))
# 
#     def __repr__(self):
#         return "McFunctionBuilder[path={}, commands={}]".format(repr(self.path), self.commands)

class McFunction:
    """
    Args:
        full_path (str)

    Attributes:
        full_path (str): The full path to the mcfunction file
        commands (list or tuple): The full list of CommandBuilders
            It becomes a tuple of strs when the mcfunction is built
    """
    def __init__(self, mfunc_name, full_path):
        self.full_path = full_path
        self.mfunc_name = mfunc_name
        self.commands = []

    def add_command(self, command):
        """
        Adds the given command to the commands list

        Args:
            command (CommandBuilder)
        """
        assert isinstance(command, str)
        self.commands.append(command)

    def finalize(self):
        """
        Converts all mutable attributes into immutable attributes
        """
        self.commands = tuple(self.commands)

    # def build_commands(self):
    #     assert not self.built
    #     self.built = True
    #     built_commands = []
    #     
    #     for command in self.commands:
    #         built_command = command.build()
    #         assert isinstance(built_command, str)
    #         built_commands.append(built_command)

    #     assert isinstance(self.commands, list)
    #     self.commands = tuple(built_commands)
