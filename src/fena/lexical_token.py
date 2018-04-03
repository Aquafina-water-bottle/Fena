from token_types import SimpleToken, StatementToken, WhitespaceToken, ALL_TYPES, TokenType

class Token:
    def __init__(self, pos, token_type, value=None):
        """
        Args:
            pos (TokenPosition): position inside the file formatted as (line, column)
            type (TokenType, SimpleToken, WhitespaceToken, StatementToken) type of the token
            value: an optional custom value
        """
        self.pos = pos
        self.type = token_type
        self.value = value

        if self.value is None:
            assert not isinstance(self.type, TokenType), "A value is required for TokenType (type={}, pos={})".format(self.type, self.pos)
            token_value = self.type.value.value
            self.value = token_value

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

    def __str__(self):
        return "Token[{} at {}]".format(repr(self.value), self.pos)

    def __repr__(self):
        return 'Token[{0}: type={1}, value={2}]'.format(repr(self.pos), repr(self.type), repr(self.value))


class TokenPosition:
    def __init__(self, line, column, length=None):
        """
        """
        self.line = line
        self.column = column
        self.length = length

    def __str__(self):
        if self.length is None:
            return "[row={}, col={}]".format(self.line, self.column)
        return "[row={}, col={} to {}]".format(self.line, self.column, self.column + self.length)

    def __repr__(self):
        if self.length is None:
            return "TokenPosition[row={}, column={}]".format(self.line, self.column)
        return "TokenPosition[row={}, column={} to {}]".format(self.line, self.column, self.column + self.length)


def test():
    token_pos = TokenPosition(line=5, column=2)
    token = Token(token_pos, SimpleToken.PLUS)
    print(token)
    print(repr(token))

    print(token.type in ALL_TYPES)
    print(token.type in SimpleToken)

    integer = Token(token_pos, TokenType.INT, 26)
    print(repr(integer))

if __name__ == "__main__":
    test()
