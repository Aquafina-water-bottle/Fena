if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fena.mcfunction import McFunction

class Writer:
    """
    Literally cleans and writes out all the proper files
    Cleans:
        - all files ending with .mcfunction for each folder the mcfunctions are in if self.clean is true
        - eg. if there are two mcfunctions with paths /functions/test/main.mcfunction and /functions/test/src/something.mcfunction,
            all files ending with ".mcfunction" under /functions/test and /functions/test/src will be deleted
            - all folder paths are based off the given existing mcfunctions
            - therefore, if there is an mcfunction that wasn't parsed under /functions/ego/test/not_parsed/hello.mcfunction, all
                mcfunctions inside /functions/ego/test/not_parsed will be kept
            - there will be no folder walking to delete mcfunctions

    Writes:
        - each mcfunction file based off of their full path
        - fena/src/parsed_cmds.txt to summarize all commands for each mcfunction file
    """
    def __init__(self, mcfunctions, args):
        assert isinstance(mcfunctions, McFunction)
        pass

    def _get_mcfunction_paths(self):
        pass

    def clean(self):
        pass

    def write(self):
        pass