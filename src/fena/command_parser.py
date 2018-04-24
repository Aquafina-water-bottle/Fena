from common_parser import CommonParser

class CommandParser(CommonParser):
    def __init__(self, lexer):
        super().__init__(__class__.__name__, lexer)

    def parse(self):
        pass

    def __repr__(self):
        pass

