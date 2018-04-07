from enum import Enum

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

    STATEMENT = "!"
    COLON = ":"
    PLUS = "+"
    MINUS = "-"
    EQUALS = "="
    TEST = "?"
    RESET = "reset"
    ENABLE = "enable"
    JOIN = "join"
    EMPTY = "empty"
    LEAVE = "leave"
    DETECT = "detect"
    IFBLOCK = "ifblock"

SIMPLE_TOKEN_VALUES = tuple(token.value for token in SimpleToken)


class WhitespaceToken(Enum):
    COMMENT = "#"
    INDENT = "    "
    DEDENT = "dedent"
    NEWLINE = "\n"
    EOF = None

WHITESPACE_TOKEN_VALUES = tuple(token.value for token in WhitespaceToken)


class StatementToken(Enum):
    """
    Contains all possible keyword tokens proceeded after a "!" 
    """
    MFUNC = "mfunc"
    FOLDER = "folder"
    PREFIX = "prefix"

STATEMENT_TOKEN_VALUES = tuple(token.value for token in StatementToken)


ALL_TYPES = tuple(TokenType) + tuple(SimpleToken) + tuple(WhitespaceToken) + tuple(StatementToken)
ALL_TOKENS = tuple(SimpleToken) + tuple(WhitespaceToken) + tuple(StatementToken)

def test():
    print(SimpleToken.PLUS)
    print(repr(SimpleToken.PLUS))
    print(SimpleToken.PLUS in SimpleToken)
    print(SimpleToken.PLUS in TokenType)
    print(SimpleToken.PLUS in ALL_TYPES)

if __name__ == "__main__":
    test()
