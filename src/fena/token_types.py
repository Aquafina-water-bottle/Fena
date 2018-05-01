from enum import Enum, auto

class TokenType(Enum):
    """
    Contains only a token type since the value is arbitrary
    """
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    LITERAL_STRING = auto()
    COORD = auto()
    COORDS = auto()
    NBT = auto()
    JSON = auto()
    BLOCK = auto()
    DETECT = auto()
    SELECTOR = auto()

class SimpleToken(Enum):
    """
    Contains the type and value
    """
    QUOTE = '"'
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

SCOREBOARD_SHORTCUT_TOKEN_VALUES = frozenset(token.value for token in ScoreboardShortToken)

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

EXECUTE_SHORTCUT_TOKEN_VALUES = frozenset(token.value for token in ExecuteShortToken)

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
    BYTE = "byte"
    SHORT = "short"
    INT = "int"
    LONG = "long"
    FLOAT = "float"
    DOUBLE = "double"

    # bossbar keywords
    MAX = "max"
    VALUE = "value"


class SelectorTokenType(Enum):
    TARGET_SELECTOR_VARIABLE = auto()
    TARGET_SELECTOR_ARGUMENT = auto()

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

SELECTOR_SIMPLE_TOKEN_VALUES = frozenset(token.value for token in SelectorSimpleToken if token.value != "end")


class NBTSimpleToken(Enum):
    EMPTY = r"{}"
    BEGIN = "{"
    END = "}"
    BEGIN_ARRAY = "["
    END_ARRAY = "]"
    COLON = ":"
    COMMA = ","
    INT_ARRAY_BEGIN = "I;"
    BYTE_ARRAY_BEGIN = "B;"
    LONG_ARRAY_BEGIN = "L;"
    QUOTE = '"'

    BYTE_END = "b"
    SHORT_END = "s"
    LONG_END = "l"
    FLOAT_END = "f"
    DOUBLE_END = "d"

NBT_SIMPLE_TOKEN_VALUES = frozenset(token.value for token in SelectorSimpleToken if token.value != "end")
NBT_NUMBER_END_VALUES = frozenset(token.value for token in 
    (NBTSimpleToken.BYTE_END, NBTSimpleToken.SHORT_END, NBTSimpleToken.LONG_END, NBTSimpleToken.FLOAT_END, NBTSimpleToken.DOUBLE_END))

def frozenset_union(*types):
    return_set = frozenset()
    for enum_type in types:
        return_set |= frozenset(enum_type)
    return return_set

ALL_TOKENS = frozenset_union(SimpleToken, WhitespaceToken, StatementToken, SelectorSimpleToken, 
    ScoreboardShortToken, ExecuteShortToken, ExecuteShortArgsToken, NBTSimpleToken)
ALL_TYPES = frozenset_union(ALL_TOKENS, TokenType, SelectorTokenType)


def test():
    print(SimpleToken.PLUS)
    print(repr(SimpleToken.PLUS))
    print(SimpleToken.PLUS in SimpleToken)
    print(SimpleToken.PLUS in TokenType)
    print(SimpleToken.PLUS in ALL_TYPES)

if __name__ == "__main__":
    test()
