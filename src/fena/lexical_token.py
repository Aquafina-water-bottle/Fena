import logging

from token_types import SimpleToken, StatementToken, TokenType, ALL_TYPES, ALL_TOKENS, SIMPLE_TOKEN_VALUES, STATEMENT_TOKEN_VALUES
from coord_utils import is_coord

class Token:
    # invalid types are all types that have preset values
    invalid_types = ALL_TYPES ^ ALL_TOKENS

    # required types are tokens that require values
    required_types = ALL_TOKENS

    def __init__(self, pos, token_type, value=None):
        """
        Args:
            pos (TokenPosition): position inside the file formatted as (row, column)
            type (TokenType, SimpleToken, WhitespaceToken, StatementToken) type of the token
            value: an optional custom value
        """
        self.pos = pos
        self.type = token_type
        self.value = value

        if self.value is None:
            assert not self.type in Token.invalid_types, "A value is required for a token type (type={}, pos={})".format(self.type, self.pos)
            assert self.type in Token.required_types, "The type {} must be a required type of {}".format(Token.required_types, repr(token_type))
            self.value = self.type.value

    def matches(self, token_type, value=None):
        """
        returns whether the token matches the given type and/or value

        Args:
            type (any token type)
            value (optional, any type)

        Returns:
            bool: Whether the type matches the given type
        """
        assert token_type in ALL_TYPES
        return (self.type == token_type) and (value is None or self.value == value)

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

    def cast(self, token_type, error_message=None):
        """
        Changes the type of this token without adequate checks, so
        checking is based off of where this method was ran

        Args:
            token_type (any token type): What token type this token should change into
            error_message (str or None): What will be displayed in the error message
        """
        if isinstance(token_type, TokenType):
            if token_type == TokenType.COORD and is_coord(self.value):
                self._cast(token_type, is_value=True)
            else:
                self._cast_error(token_type, message=error_message)
            return

        # guaranteed not to be TokenType
        try:
            self._cast(token_type)
        except ValueError:
            # repr of self shows the token type
            self._cast_error(token_type, message=error_message)

    def _cast(self, token_type, is_value=False):
        """
        Args:
            token_type (any token type): What token type this token should change into
            is_value (bool): Whether the token type can be directly set or it must be gotten from the enum class
        """
        if is_value:
            new_type = token_type
        else:
            new_type = token_type(self.value)
        logging.debug("Converted token {} to type {}".format(repr(self), new_type))
        self.type = new_type

    def _cast_error(self, token_type, message=None):
        if message is None:
            message = "Invalid type casting"
        raise TypeError("{} cast to {}: {}".format(self, repr(token_type), message))

    def __str__(self):
        return "Token[{} at {}]".format(repr(self.value), self.pos)

    def __repr__(self):
        return 'Token[{0}: type={1}, value={2}]'.format(repr(self.pos), repr(self.type), repr(self.value))


def test():
    from token_position import TokenPosition
    token_pos = TokenPosition(row=5, column=2, char_pos=167)

    token = Token(token_pos, SimpleToken.PLUS)
    print(token)
    print(repr(token))

    print(token.type in ALL_TYPES)
    print(token.type in SimpleToken)

    # error since it requires a value
    # integer = Token(token_pos, TokenType.INT)
    integer = Token(token_pos, TokenType.INT, 26)
    print(repr(integer))

def test_docs():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test_docs()
    test()
