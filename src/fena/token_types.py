from enum import Enum

class TokenRepr:
    def __init__(self, token_repr, value):
        self.repr = token_repr
        self.value = value

    def __str__(self):
        return "[{} as {}]".format(self.repr, repr(self.value))

    def __repr__(self):
        return "TokenRepr[repr={}, value={}]".format(repr(self.repr), repr(self.value))

class TokenType(Enum):
    """
    Contains only a token type since the value is arbitrary
    """
    SELECTOR = "selector"
    INT = "int"
    FLOAT = "float"
    COORD = "coord"
    COORDS = "coords"
    DATATAG = "datatag"
    STRING = "string"
    COMMAND = "command"
    LEADING_COMMAND = "leading command"

class SimpleToken(Enum):
    """
    Contains the type and value
    """

    STATEMENT = TokenRepr("statement", "!")
    PLUS = TokenRepr("plus", "+")
    MINUS = TokenRepr("minus", "-")
    EQUALS = TokenRepr("equals", "=")
    TEST = TokenRepr("test", "?")
    RESET = TokenRepr("reset", "reset")
    ENABLE = TokenRepr("enable", "enable")
    JOIN = TokenRepr("join", "join")
    EMPTY = TokenRepr("empty", "empty")
    LEAVE = TokenRepr("leave", "leave")
    DETECT = TokenRepr("detect", "detect")
    IFBLOCK = TokenRepr("ifblock", "ifblock")

class WhitespaceToken(Enum):
    INDENT = TokenRepr("indent", "    ")
    DEDENT = TokenRepr("dedent", "dedent")
    NEWLINE = TokenRepr("newline", "\n")
    EOF = TokenRepr("EOF", None)

class StatementToken(Enum):
    """
    Contains all possible keyword tokens proceeded after a "!" 
    """
    MFUNC = TokenRepr("mfunc", "mfunc")
    FOLDER = TokenRepr("folder", "folder")
    INITIALS = TokenRepr("initials", "initials")

ALL_TYPES = tuple(TokenType) + tuple(SimpleToken) + tuple(WhitespaceToken) + tuple(StatementToken)

def test():
    print(SimpleToken.PLUS)
    print(repr(SimpleToken.PLUS))
    print(SimpleToken.PLUS in SimpleToken)
    print(SimpleToken.PLUS in TokenType)
    print(SimpleToken.PLUS in ALL_TYPES)

if __name__ == "__main__":
    test()
