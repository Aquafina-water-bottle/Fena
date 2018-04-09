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


class SelectorTokenType(Enum):
    TARGET_SELECTOR_VARIABLE = "selector variable"
    TARGET_SELECTOR_ARGUMENT = "selector argument"
    STRING = "string"
    INT = "int"

class SelectorSimpleToken(Enum):
    OPEN_BRACKET = "["
    CLOSE_BRACKET = "]"
    EQUALS = "="
    NOT = "!"
    RANGE = ".."
    COMMA = ","
    OPEN_PARENTHESES = "("
    CLOSE_PARENTHESES = ")"
    END = "end"

SELECTOR_SIMPLE_TOKENS_VALUES = tuple(token.value for token in SelectorSimpleToken if token.value != "end")


ALL_TYPES = tuple(TokenType) + tuple(SelectorTokenType) + tuple(SimpleToken) + tuple(WhitespaceToken) + tuple(StatementToken) + tuple(SelectorSimpleToken)
ALL_TOKENS = tuple(SimpleToken) + tuple(WhitespaceToken) + tuple(StatementToken) + tuple(SelectorSimpleToken)


def test():
    print(SimpleToken.PLUS)
    print(repr(SimpleToken.PLUS))
    print(SimpleToken.PLUS in SimpleToken)
    print(SimpleToken.PLUS in TokenType)
    print(SimpleToken.PLUS in ALL_TYPES)

if __name__ == "__main__":
    test()
