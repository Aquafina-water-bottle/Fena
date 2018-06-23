import logging

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fenalib.assert_utils import assert_type
from fenalib.token_position import TokenPosition
from fenalib.token_classes import TypedToken, DelimiterToken, WhitespaceToken
from fenalib.token_classes import SimpleTokenClass, TokenClass
from fenalib.coord_utils import is_coord
from fenalib.config_data import ConfigData

"""
Note that this file is named "lexical_token" because if it was named "token",
it would interfere with the token used from the default logging module
"""

class Token:
    # typed_tokens = frozenset(TypedToken)
    # simple_token_types = TokenTypes.get(DelimiterToken, WhitespaceToken)
    # all_token_types = typed_tokens | simple_token_types

    config_data = ConfigData()

    def __init__(self, position, token_type, value=None):
        """
        Args:
            position (TokenPosition): position inside the file formatted as (row, column)
            type (TypedToken, SimpleToken, WhitespaceToken, StatementToken) type of the token
            value (any): an optional custom value
            replacement (any): an optional custom value to be set as a replacement of the token type
                - this will be used only when building instead of returning the value
        """
        assert_type(position, TokenPosition)
        assert_type(token_type, TokenClass)
        assert_type(value, str, optional=True)

        self.position = position
        self.token_type = token_type
        self.value = value
        self.replacement = None

        if self.value is None:
            assert_type(token_type, SimpleTokenClass)
            self.value = self.token_type.value

    def matches(self, token_type, value=None, values=None):
        """
        returns whether the token matches the given type and/or value

        Args:
            type (any token type)
            value (optional, any type)

        Returns:
            bool: Whether the type matches the given type
        """
        assert_type(token_type, TokenClass)
        assert not (value is not None and values is not None)
        if value is not None:
            return (self.token_type == token_type) and self.value == value

        if values is not None:
            return (self.token_type == token_type) and self.value in values

        return self.token_type == token_type

    def matches_any_of(self, *types):
        """
        returns whether the token matches any one of the types

        Args:
            types (any token type): any number of types to compare the token with

        Returns:
            bool: Whether the token matches any of the provided types
        """
        for token_type in types:
            if self.matches(token_type):
                return True
        return False

    def __str__(self):
        return f"Token[{self.value!r} ({str(self.token_type)}) at {self.position}]"

    def __repr__(self):
        if self.replacement is None:
            return f'Token[{self.position!r}: type={self.token_type!r}, value={self.value!r}]'
        return f'Token[{self.position!r}: type={self.token_type!r}, value={self.value!r}, replacement={self.replacement!r}]'


def test():
    from token_position import TokenPosition
    # from token_classes import SimpleToken

    token_pos = TokenPosition(row=5, column=2, char_pos=167)

    # token = Token(token_pos, SimpleToken.PLUS)
    token = Token(token_pos, DelimiterToken.EQUALS)
    print(token)
    print(repr(token))

    # print(token.type in ALL_TOKEN_TYPES)
    # print(token.type in SimpleToken)

    # error since it requires a value
    # integer = Token(token_pos, TypedToken.INT)
    integer = Token(token_pos, TypedToken.INT, 26)
    print(repr(integer))

def test_docs():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test_docs()
    test()
