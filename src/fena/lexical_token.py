import logging

from token_classes import TokenTypes, TypedToken, DelimiterToken, WhitespaceToken
from coord_utils import is_coord
from config_data import ConfigData

class Token:
    typed_tokens = frozenset(TypedToken)
    simple_token_types = TokenTypes.get(DelimiterToken, WhitespaceToken)
    all_token_types = typed_tokens | simple_token_types

    config_data = ConfigData()

    def __init__(self, pos, token_type, value=None):
        """
        Args:
            pos (TokenPosition): position inside the file formatted as (row, column)
            type (TypedToken, SimpleToken, WhitespaceToken, StatementToken) type of the token
            value (any): an optional custom value
            replacement (any): an optional custom value to be set as a replacement of the token type
                - this will be used only when building instead of returning the value
        """
        self.pos = pos
        self.type = token_type
        self.value = value
        self.replacement = None

        if self.value is None:
            assert not self.type in Token.typed_tokens, f"{self!r}: A value is required for the given token type"
            assert self.type in Token.simple_token_types, f"The type {token_type} must be a simple token type within {Token.simple_token_types!r}"
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
        assert token_type in Token.all_token_types
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
        if token_type == self.type:
            return

        if isinstance(token_type, TypedToken):
            # checks if coordinate, block or int
            if (token_type == TypedToken.COORD and is_coord(self.value) or 
                    token_type == TypedToken.BLOCK and self.value in Token.config_data.blocks or
                    token_type == TypedToken.INT):

                if token_type == TypedToken.INT:
                    self.value = int(self.value)

                self._cast_token_type(token_type)

            elif token_type == TypedToken.STRING:
                self.value = str(self.value)
                self._cast_token_type(token_type)

            else:
                self._cast_error(token_type, message=error_message)
            return

        # guaranteed not to be TypedToken
        try:
            self._cast_token_class(token_type)
        except ValueError:
            # repr of self shows the token type
            self._cast_error(token_type, message=error_message)

    def _cast_token_type(self, token_type):
        """
        Args:
            token_type (any token type): What token type this token should change into
        """
        new_type = token_type
        logging.debug("Converted token {!r} to type {}".format(repr(self), new_type))
        self.type = new_type

    def _cast_token_class(self, token_class):
        """
        """
        new_type = token_class(self.value)
        logging.debug("Converted token {} to type {}".format(self, new_type))
        self.type = new_type

    def _cast_error(self, token_type, message=None):
        if message is None:
            message = "Invalid type casting"
        raise TypeError("{!r} cast to {!r}: {}".format(self, token_type, message))


    def __str__(self):
        return "Token[{!r} at {}]".format(self.value, self.pos)

    def __repr__(self):
        if self.replacement is None:
            return 'Token[{!r}: type={!r}, value={!r}]'.format(self.pos, self.type, self.value)
        return 'Token[{!r}: type={!r}, value={!r}, replacement={!r}]'.format(self.pos, self.type, self.value, self.replacement)


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
