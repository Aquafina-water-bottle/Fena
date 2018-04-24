import os.path
from collections import deque

from config_data import ConfigData
from command_lexer import CommandLexer
from command_parser import CommandParser

class CommandBuilder:
    """
    Holds branching simple commands using a builder model
    Args:
        command (Token with TokenType.COMMAND)

        prefix (str): Any prefix to objectives, teams or tags
        constobj (str)
        shortcuts (dict): All function shortcuts present in the file
            Maps function name to the function path
    """
    config_data = ConfigData()
    prefix = ""
    constobj = ""
    shortcuts = {}

    @classmethod
    def initialize(cls, symbol_table, mcfunctions):
        """
        Sets the prefix, constobj and gets all function shortcuts
        """
        # default for prefix is "fena"
        if symbol_table.prefix is None:
            cls.prefix = "fena"
        else:
            cls.prefix = symbol_table.prefix
        
        # default for constobj is "constants"
        if symbol_table.constobj is None:
            cls.constobj = "constants"
        else:
            cls.constobj = symbol_table.constobj

        # gets all mcfunction shortcuts
        for mcfunction in mcfunctions:
            CommandBuilder._set_shortcut(mcfunction.path)

    @classmethod
    def _set_shortcut(cls, full_path):
        """
        Gets the function paths all the way until "functions"
        """
        # strips away ".mcfunction"
        path_without_ext, extension = os.path.splitext(full_path)
        name = os.path.basename(path_without_ext)
        assert extension == ".mcfunction"

        # gets the list of all directories including base file without extension
        path_list = os.path.normpath(path_without_ext).split(os.sep)

        # gets all directories of the shortcut including the function name
        # path_list should contain "functions" by the end, or else it will be an empty list
        directories = deque()
        while path_list and path_list[-1] != "functions":
            directories.appendleft(path_list.pop())

        if not path_list:
            raise SyntaxError("Path {} must contain a functions/ folder".format(full_path))

        if len(directories) <= 1:
            raise SyntaxError("Path {} must have a folder inside the functions/ folder".format(full_path))

        shortcut = directories.popleft() + ":"
        shortcut += "/".join(directories)

        cls.shortcuts[name] = shortcut

    def __init__(self, command):
        self.command = command

    def build(self):
        """
        Builds itself so the string representation can be used
        """
        lexer = CommandLexer(self.command.value)
        parser = CommandParser(lexer)
        command = parser.parse()
        print(command)

    def add_execute(self, tokens):
        pass

    def add_scoreboard(self, tokens):
        pass

    def add_function(self, tokens):
        pass

    def add_simple(self, tokens):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass
