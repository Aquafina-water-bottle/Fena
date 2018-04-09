import os
import logging

class McFunction:
    """
    Contains all commands within a single defined mcfunction

    Args:
        path (str): Full path to the mcfunction
        prefix (str or None): Any prefix to objectives, teams or tags

    Attributes:
        path (str): Full path to the mcfunction file
        name (str): mcfunction name used for the shortcut
        func_path (str): mcfunction path as defined by the function command
        prefix (str or None): Any prefix to objectives, teams or tags
        commands (list): List of commands in the mcfunction
    """

    def __init__(self, path, prefix):
        self.path = path
        self.name = os.path.basename(self.path).replace(".mcfunction", "")
        self.func_path = self._get_func_path()
        self.prefix = prefix
        self.commands = []

        # holds a list of command strings
        self.cmd_strs = []

    def add_command(self, command):
        """
        Adds the given command to the commands list

        :param command: string representing the command
        """
        self.commands.append(command)

    # @staticmethod
    # def get_func_path(path):
    #     # gets the function paths all the way until "functions"
    #     function_paths = []

    #     # the path that will be changed, with the mcfunction file removed
    #     path_calc = os.path.dirname(path)
    #     file_ending = ".mcfunction"

    #     # the mcfunction file
    #     func_name = os.path.basename(path)
    #     if func_name.endswith(file_ending):
    #         func_name = func_name[:-len(file_ending)]

    #     base_name = os.path.basename(path_calc)
    #     path_disp = ""

    #     # gets all directories in reverse order
    #     while base_name != "functions" and base_name != "":
    #         function_paths.append(base_name)
    #         path_calc = os.path.dirname(path_calc)
    #         base_name = os.path.basename(path_calc)

    #     # the base name should end at functions for there to be a functions folder
    #     if base_name != "functions":
    #         raise SyntaxError("Path {} must contain a functions/ folder".format(path))

    #     # checks whether the length is 0 for some reason
    #     assert len(function_paths) != 0, "Path {} must contain a folder".format(path)

    #     # path_disp should end with a separator, aka : or /
    #     path_disp = function_paths.pop() + ":"

    #     # while the function_paths list is not empty
    #     while function_paths:
    #         path_disp += function_paths.pop() + "/"

    #     path_disp += func_name
    #     return path_disp

    def _get_func_path(self):
        # gets the function paths all the way until "functions"
        function_paths = []

        # the path that will be changed, with the mcfunction file removed
        path_calc = os.path.dirname(self.path)

        # the mcfunction file
        base_name = os.path.basename(path_calc)
        path_disp = ""

        # gets all directories in reverse order
        while base_name != "functions" and base_name != "":
            function_paths.append(base_name)
            path_calc = os.path.dirname(path_calc)
            base_name = os.path.basename(path_calc)

        # the base name should end at functions for there to be a functions folder
        if base_name != "functions":
            raise SyntaxError("Path {} must contain a functions/ folder".format(self.path))

        # checks whether the length is 0 for some reason
        assert len(function_paths) != 0, "Path {} must contain a folder".format(self.path)

        # path_disp should end with a separator, aka : or /
        path_disp = function_paths.pop() + ":"

        # while the function_paths list is not empty
        while function_paths:
            path_disp += function_paths.pop() + "/"

        path_disp += self.name
        # path_disp += ".mcfunction"
        return path_disp

    def debug_commands(self):
        logging.debug(str(self))
        for command in self.commands:
            cmd_str = " ".join(str(cmd.value) for cmd in command.tokens)
            logging.debug(cmd_str)

    def __str__(self):
        return "McFunction[name={}, func_path={}]".format(repr(self.name), repr(self.func_path))

    def __repr__(self):
        return "McFunction[path={}, name={}, func_path={}, commands={}]".format(repr(self.path), repr(self.name), repr(self.func_path), self.commands)