from enum import Enum, auto

class TokenValues:
    cache = {}
    
    @staticmethod
    def get(token_class):
        assert token_class not in (TypedToken)
        if token_class not in TokenValues.cache:
            values = frozenset(token.value for token in token_class)
            TokenValues.cache[token_class] = values

        return TokenValues.cache[token_class]

# class TokenTypes:
#     cache = {}
#     
#     @staticmethod
#     def get(*token_classes):
#         total_token_types = frozenset()
#         for token_class in token_classes:
#             if token_class not in TokenValues.cache:
#                 values = frozenset(token_class)
#                 TokenTypes.cache[token_class] = values
# 
#             total_token_types |= TokenTypes.cache[token_class]
# 
#         return total_token_types

# def get_token_types(token_classes):
#     """
#     Args:
#         token_classes (Enum)
# 
#     Returns:
#         frozenset: The set containing all tokens
#     """
#     token_type_set = set()
#     for token_type in token_classes:
#         token_type_set |= set(token_type)
#     return frozenset(token_type_set)

class TokenClass:
    pass

class SimpleTokenClass(TokenClass):
    pass

class TypedToken(TokenClass, Enum):
    """
    Contains only a token type since the value is arbitrary
    """
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    LITERAL_STRING = auto()
    # COORD = auto()
    SELECTOR_VARIABLE_SPECIFIER = auto()

class DelimiterToken(SimpleTokenClass, Enum):
    """
    Contains the type and value
    """
    QUOTE = '"'
    # ESCAPED_QUOTE = r'\"'
    COLON = ":"
    COMMA = ","
    AT = "@"
    EQUALS = "="
    EXCLAMATION_MARK = "!"
    RANGE = ".."
    SEMICOLON = ";"
    GROUP_TAG = "#"

    OPEN_PARENTHESES = "("
    CLOSE_PARENTHESES = ")"
    OPEN_SQUARE_BRACKET = "["
    CLOSE_SQUARE_BRACKET = "]"
    OPEN_CURLY_BRACKET = "{"
    CLOSE_CURLY_BRACKET = "}"

class WhitespaceToken(SimpleTokenClass, Enum):
    COMMENT = "#"
    INDENT = "    "
    DEDENT = "dedent"
    NEWLINE = "\n"
    EOF = "EOF (end of file)"

def test():
    print(DelimiterToken.COLON)
    print(repr(DelimiterToken.COLON))
    print(DelimiterToken.COLON in DelimiterToken)
    print(DelimiterToken.COLON in TypedToken)
    print(isinstance(DelimiterToken.COLON, TypedToken))
    print(isinstance(DelimiterToken, TypedToken))
    print(isinstance(DelimiterToken.COLON, SimpleTokenClass))
    print(isinstance(DelimiterToken, SimpleTokenClass))
    print(isinstance(DelimiterToken.COLON, TokenClass))
    print(isinstance(DelimiterToken, TokenClass))
    print(isinstance(TypedToken.INT, TypedToken))

    print(TokenValues.get(DelimiterToken))
    print(TokenValues.cache)
    print(TokenValues.get(DelimiterToken))

    print(TokenValues.get(DelimiterToken))

if __name__ == "__main__":
    test()
