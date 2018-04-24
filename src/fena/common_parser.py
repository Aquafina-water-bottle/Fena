from abc import ABC, abstractmethod

class CommonParser(ABC):
    """
    Args:
        lexer (CommonLexer)
        parser_type (str)

    Attributes:
        iterator (CommonLexer)
        parser_type (str)
        current_token (Token)
    """
        
    def __init__(self, class_name, lexer):
        self.class_name = class_name
        self.iterator = iter(lexer)
        self.current_token = None
        self.advance()

    @abstractmethod
    def parse(self):
        pass

    def error(self, message=None):
        if message is None:
            message = "Invalid syntax"
        raise SyntaxError("{} {}: {}".format(self.class_name, self.current_token, message))

    def advance(self):
        """
        Gets the next token from the lexer without checking any type
        """
        self.current_token = next(self.iterator, None)

    def eat(self, token_type, value=None, error_message=None):
        """
        Advances given the token type and values match up with the current token

        Args:
            token_type (any token type)
            value (any, defaults to None)
        """

        if (value is None or self.current_token.value == value) and self.current_token.matches(token_type):
            token = self.current_token
            self.advance()

        else:
            if error_message is None:
                error_message = "Expected {}".format(token_type)
            self.error(error_message)

        return token

    @abstractmethod
    def __repr__(self):
        return "CommonParser[iterator={}, current_token={}]".format(repr(self.iterator), repr(self.current_token))


def test():
    # from common_iterator import CommonLexer

    # class Test(CommonParser):
    #     pass

    # class LexerTest(CommonLexer):
    #     pass

    # bruh = LexerTest("bruh", "token")
    # t = Test(bruh)
    # c = CommonParser(bruh)
    # t2 = Test(bruh)

    # print(tuple(map(id, (t, t2, c))))
    # print(vars(t))
    # print(repr(t))
    pass

if __name__ == "__main__":
    test()
