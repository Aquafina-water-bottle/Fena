"""
Singleton class that contains:
    objectives dict
    tags dict
    teams dict
    functions dict

    constobj
    prefix
"""

import logging
import os.path
from collections import deque

class InFileConfigData:
    """
    Holds branching simple commands using a builder model
    Args:
        prefix (str): Any prefix to objectives, teams or tags
        constobj (str)
        objectives (dict): Holds all properly named objectives and shortcut objectives
        tags (dict): Holds all properly named tags and shortcut objectives
            - Note that tags are also defined in nbt data
        teams (dict): Holds all properly named teams and shortcut objectives
            - Note that a team can also be defined in nbt data
                - objectives, tags and teams all map to _name -> prefix.name and prefix.name -> prefix.name
                - the reason for prefix.name -> prefix.name is for containment tests and
                  for ensuring all objs/tags/teams can be mapped if contained
        functions (dict): All function shortcuts present in the file
            - Maps function name to the function path
    """

    def __init__(self):
        self.objectives = {}
        self.tags = {}
        self.teams = {}
        self.functions = {}
        self.constobj = None
        self.prefix = None
    
    def __new__(cls):
        """
        Ensures they are the same class
        """
        if not hasattr(cls, '_in_file_config_data'):
            cls._in_file_config_data = super().__new__(cls)
        return cls._in_file_config_data

    # def initialize(cls, symbol_table, mcfunctions):
    #     """
    #     Sets the prefix, constobj and gets all function shortcuts
    #     """
    #     # default for prefix is "fena"
    #     if symbol_table.prefix is None:
    #         cls.prefix = "fena"
    #         logging.warning("Using the default prefix of {}".format(cls.prefix))
    #     else:
    #         cls.prefix = symbol_table.prefix
    #     
    #     # default for constobj is "constants"
    #     if symbol_table.constobj is None:
    #         cls.constobj = "constants"
    #     else:
    #         cls.constobj = symbol_table.constobj

    #     # gets all mcfunction shortcuts
    #     for mcfunction in mcfunctions:
    #         self._set_shortcut(mcfunction.path)

    # def _set_shortcut(self, full_path):
    #     """
    #     Gets the function paths all the way until "functions"
    #     """
    #     # strips away ".mcfunction"
    #     path_without_ext, extension = os.path.splitext(full_path)
    #     name = os.path.basename(path_without_ext)
    #     assert extension == ".mcfunction"

    #     # gets the list of all directories including base file without extension
    #     path_list = os.path.normpath(path_without_ext).split(os.sep)

    #     # gets all directories of the shortcut including the function name
    #     # path_list should contain "functions" by the end, or else it will be an empty list
    #     directories = deque()
    #     while path_list and path_list[-1] != "functions":
    #         directories.appendleft(path_list.pop())

    #     if not path_list:
    #         raise SyntaxError("Path {} must contain a functions/ folder".format(full_path))

    #     if len(directories) <= 1:
    #         raise SyntaxError("Path {} must have a folder inside the functions/ folder".format(full_path))

    #     shortcut = directories.popleft() + ":"
    #     shortcut += "/".join(directories)

    #     cls.shortcuts[name] = shortcut

