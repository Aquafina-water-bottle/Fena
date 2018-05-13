from enum import Enum, auto

class TokenValues:
    cache = {}
    
    @staticmethod
    def get(token_class):
        assert token_class not in ALL_TYPED_TOKEN_CLASSES
        if token_class not in TokenValues.cache:
            values = frozenset(token.value for token in token_class)
            TokenValues.cache[token_class] = values

        return TokenValues.cache[token_class]

def get_token_types(token_classes):
    """
    Args:
        token_classes (Enum)

    Returns:
        frozenset: The set containing all tokens
    """
    token_type_set = set()
    for token_type in token_classes:
        token_type_set |= set(token_type)
    return frozenset(token_type_set)


class TypedToken(Enum):
    """
    Contains only a token type since the value is arbitrary
    """
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    LITERAL_STRING = auto()
    COORD = auto()
    BLOCK = auto()
    JSON = auto()

class SimpleToken(Enum):
    """
    Contains the type and value
    """
    QUOTE = '"'
    ESCAPED_QUOTE = r'\"'
    COLON = ":"
    COMMA = ","
    OPEN_PARENTHESES = "("
    CLOSE_PARENTHESES = ")"
    EOF = None

class WhitespaceSimpleToken(Enum):
    COMMENT = "#"
    INDENT = "    "
    DEDENT = "dedent"
    NEWLINE = "\n"


class StatementSimpleToken(Enum):
    """
    Contains all possible keyword tokens proceeded after a "!" and the "!" token
    """
    STATEMENT_SPECIFIER = "!"
    MFUNC = "mfunc"
    FOLDER = "folder"
    PREFIX = "prefix"
    CONSTOBJ = "constobj"


class ScoreboardSimpleToken(Enum):
    PLUS = "+"
    MINUS = "-"
    EQUALS = "="
    RESET = "reset"
    ENABLE = "enable"
    GET = "<-"
    JOIN = "join"
    EMPTY = "empty"
    LEAVE = "leave"


class ExecuteSimpleToken(Enum):
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


class ExecuteArgsSimpleToken(Enum):
    # other
    FEET = "feet"
    EYES = "eyes"
    AXES = "axes"

    # dimensions
    OVERWORLD = "overworld"
    NETHER = "nether"
    THE_END = "end"

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


class SelectorTypedToken(Enum):
    SELECTOR_VARIABLE_SPECIFIER = auto()

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


class NBTSimpleToken(Enum):
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


class NBTNumberEndSimpleToken(Enum):
    BYTE_END = "b"
    SHORT_END = "s"
    LONG_END = "l"
    FLOAT_END = "f"
    DOUBLE_END = "d"



ALL_SIMPLE_TOKEN_CLASSES = frozenset({SimpleToken, WhitespaceSimpleToken, StatementSimpleToken, SelectorSimpleToken, 
    ScoreboardSimpleToken, ExecuteSimpleToken, ExecuteArgsSimpleToken, NBTSimpleToken, NBTNumberEndSimpleToken})

ALL_TYPED_TOKEN_CLASSES = frozenset({TypedToken, SelectorTypedToken})

ALL_TOKEN_CLASSES = ALL_SIMPLE_TOKEN_CLASSES | ALL_TYPED_TOKEN_CLASSES


ALL_SIMPLE_TOKEN_TYPES = get_token_types(ALL_SIMPLE_TOKEN_CLASSES)

ALL_TYPED_TOKEN_TYPES = get_token_types(ALL_TYPED_TOKEN_CLASSES)

ALL_TOKEN_TYPES = ALL_SIMPLE_TOKEN_TYPES | ALL_TYPED_TOKEN_TYPES


def test():
    print(SimpleToken.COLON)
    print(repr(SimpleToken.COLON))
    print(SimpleToken.COLON in SimpleToken)
    print(SimpleToken.COLON in TypedToken)
    print(SimpleToken.COLON in ALL_SIMPLE_TOKEN_TYPES)

    print(TokenValues.get(SimpleToken))
    # print(TokenValues.cache)
    print(TokenValues.get(SimpleToken))

    print(ALL_TOKEN_CLASSES)
    print(ALL_TYPED_TOKEN_CLASSES)
    print(ALL_TYPED_TOKEN_TYPES)
    print(TokenValues.get(StatementSimpleToken))

if __name__ == "__main__":
    test()
