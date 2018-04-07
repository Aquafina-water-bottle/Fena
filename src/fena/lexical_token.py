from token_types import TokenType, SimpleToken, StatementToken, WhitespaceToken, ALL_TYPES, SIMPLE_TOKEN_VALUES, STATEMENT_TOKEN_VALUES

class Token:
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
            assert not isinstance(self.type, TokenType), "A value is required for TokenType (type={}, pos={})".format(self.type, self.pos)
            assert isinstance(self.type, (SimpleToken, WhitespaceToken, StatementToken))
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

    def cast(self, token_type):
        """
        Changes the type of this token

        Args:
            token_type (any token type): What token type this token should change into
        """
        if token_type == SimpleToken and self.value in SIMPLE_TOKEN_VALUES:
            self.type = token_type(self.value)
        elif token_type == StatementToken and self.value in STATEMENT_TOKEN_VALUES:
            self.type = token_type(self.value)
        else:
            raise TypeError("{} : Invalid type casting to {}".format(repr(self), repr(token_type)))

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
