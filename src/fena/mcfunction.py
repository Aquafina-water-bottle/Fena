import os

class McFunction:
    """
    Contains all commands within a single defined mcfunction
    """

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path).replace(".mcfunction", "")
        self.funcPath = self._getFuncPath()
        self.commands = []

        # holds a list of command strings
        self.cmd_strs = []

        # might be implemented in the future, idk
        self.nick = None

    def addCommand(self, command):
        """
        Adds the given command to the commands list

        :param command: string representing the command
        """
        self.commands.append(command)

    @staticmethod
    def getFuncPath(path):
        # gets the function paths all the way until "functions"
        functionPaths = []

        # the path that will be changed, with the mcfunction file removed
        pathCalc = os.path.dirname(path)
        fileEnding = ".mcfunction"

        # the mcfunction file
        funcName = os.path.basename(path)
        if funcName.endswith(fileEnding):
            funcName = funcName[:-len(fileEnding)]

        baseName = os.path.basename(pathCalc)
        pathDisp = ""

        # gets all directories in reverse order
        while baseName != "functions" and baseName != "":
            functionPaths.append(baseName)
            pathCalc = os.path.dirname(pathCalc)
            baseName = os.path.basename(pathCalc)

        # the base name should end at functions for there to be a functions folder
        if baseName != "functions":
            raise SyntaxError("Path {} must contain a functions/ folder".format(path))

        # checks whether the length is 0 for some reason
        assert len(functionPaths) != 0, "Path {} must contain a folder".format(path)

        # pathDisp should end with a separator, aka : or /
        pathDisp = functionPaths.pop() + ":"

        # while the functionPaths list is not empty
        while functionPaths:
            pathDisp += functionPaths.pop() + "/"

        pathDisp += funcName
        return pathDisp

    def _getFuncPath(self):
        return McFunction.getFuncPath(self.path)