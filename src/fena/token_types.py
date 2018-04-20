from enum import Enum, auto

class TokenType(Enum):
    """
    Contains only a token type since the value is arbitrary
    """
    SELECTOR = auto()
    INT = auto()
    FLOAT = auto()
    COORD = auto()
    COORDS = auto()
    DATATAG = auto()
    STRING = auto()
    COMMAND = auto()
    STATEMENT = auto()

class SimpleToken(Enum):
    """
    Contains the type and value
    """

    STATEMENT_SPECIFIER = "!"
    COLON = ":"
    PLUS = "+"
    MINUS = "-"
    EQUALS = "="
    TEST = "?"
    COMMA = ","
    OPEN_PARENTHESES = "("
    CLOSE_PARENTHESES = ")"
    RESET = "reset"
    ENABLE = "enable"
    JOIN = "join"
    EMPTY = "empty"
    LEAVE = "leave"
    DETECT = "detect"
    IFBLOCK = "ifblock"

SIMPLE_TOKEN_VALUES = frozenset(token.value for token in SimpleToken)


class WhitespaceToken(Enum):
    COMMENT = "#"
    INDENT = "    "
    DEDENT = "dedent"
    NEWLINE = "\n"
    EOF = None

WHITESPACE_TOKEN_VALUES = frozenset(token.value for token in WhitespaceToken)


class StatementToken(Enum):
    """
    Contains all possible keyword tokens proceeded after a "!" 
    """
    MFUNC = "mfunc"
    FOLDER = "folder"
    PREFIX = "prefix"
    CONSTOBJ = "constobj"

STATEMENT_TOKEN_VALUES = frozenset(token.value for token in StatementToken)


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

SELECTOR_SIMPLE_TOKENS_VALUES = frozenset(token.value for token in SelectorSimpleToken if token.value != "end")


ALL_TYPES = frozenset(TokenType) | frozenset(SelectorTokenType) | frozenset(SimpleToken) | frozenset(WhitespaceToken) | frozenset(StatementToken) | frozenset(SelectorSimpleToken)
ALL_TOKENS = frozenset(SimpleToken) | frozenset(WhitespaceToken) | frozenset(StatementToken) | frozenset(SelectorSimpleToken)


def test():
    print(SimpleToken.PLUS)
    print(repr(SimpleToken.PLUS))
    print(SimpleToken.PLUS in SimpleToken)
    print(SimpleToken.PLUS in TokenType)
    print(SimpleToken.PLUS in ALL_TYPES)

if __name__ == "__main__":
    test()
