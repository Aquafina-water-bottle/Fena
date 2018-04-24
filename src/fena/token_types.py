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

    COLON = ":"
    COMMA = ","
    OPEN_PARENTHESES = "("
    CLOSE_PARENTHESES = ")"

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
    Contains all possible keyword tokens proceeded after a "!" and the "!" token
    """
    STATEMENT_SPECIFIER = "!"
    MFUNC = "mfunc"
    FOLDER = "folder"
    PREFIX = "prefix"
    CONSTOBJ = "constobj"

STATEMENT_TOKEN_VALUES = frozenset(token.value for token in StatementToken)


class ScoreboardShortToken(Enum):
    PLUS = "+"
    MINUS = "-"
    EQUALS = "="
    TEST = "?"
    RESET = "reset"
    ENABLE = "enable"
    JOIN = "join"
    EMPTY = "empty"
    LEAVE = "leave"

SCOREBOARD_SHORTCUT_TOKENS_VALUES = frozenset(token.value for token in ScoreboardShortToken)

class ExecuteShortToken(Enum):
    AS = "as"
    POS = "pos"
    AT = "at"
    FACING = "facing"
    AST = "as at"

    IF = "if"
    IFNOT = "ifnot"
    UNLESS = "unless"

    RESULT = "result"
    SUCCESS = "success"

EXECUTE_SHORTCUT_TOKENS_VALUES = frozenset(token.value for token in ExecuteShortToken)

class ExecuteShortArgsToken(Enum):
    # other
    FEET = "feet"
    EYES = "eyes"
    AXES = "axes"

    # dimensions
    OVERWORLD = "overworld"
    NETHER = "nether"
    THE_END = "the_end"

    # comparison operators
    EQUALS = "=="
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_EQUAL = "<="

    # primative types used for scaling
    SHORT = "short"

    # bossbar keywords
    MAX = "max"
    VALUE = "value"


class SelectorTokenType(Enum):
    TARGET_SELECTOR_VARIABLE = "selector variable"
    TARGET_SELECTOR_ARGUMENT = "selector argument"
    STRING = "string"
    INT = "int"

class SelectorSimpleToken(Enum):
    BEGIN = "@"
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


class NBTSimpleToken(Enum):
    BEGIN = "{"
    END = "}"
    BEGIN_LIST = "["
    END_LIST = "]"
    COMMA = ","
    INT_ARRAY_BEGIN = "I;"
    BYTE_ARRAY_BEGIN = "B;"
    LONG_ARRAY_BEGIN = "L;"
    QUOTE = '"'



ALL_TYPES = (frozenset(TokenType) | frozenset(SelectorTokenType) | frozenset(SimpleToken) | frozenset(WhitespaceToken) | frozenset(StatementToken) | frozenset(SelectorSimpleToken))
ALL_TOKENS = frozenset(SimpleToken) | frozenset(WhitespaceToken) | frozenset(StatementToken) | frozenset(SelectorSimpleToken)


def test():
    print(SimpleToken.PLUS)
    print(repr(SimpleToken.PLUS))
    print(SimpleToken.PLUS in SimpleToken)
    print(SimpleToken.PLUS in TokenType)
    print(SimpleToken.PLUS in ALL_TYPES)

if __name__ == "__main__":
    test()
