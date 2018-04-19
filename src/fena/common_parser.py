from abc import ABC, abstractmethod

class CommonParser(ABC):
    """
    Args:
        lexer (CommonLexer)
        parser_type (str)

    Attributes:
        lexer (CommonLexer)
        parser_type (str)
        current_token (Token)
    """
        
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.advance()

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type, error_message=None):
        if error_message is None:
            error_message = "{} Syntax Error".format(repr(__class__.__name__))
        if not self.current_token.type.matches(token_type):
            raise SyntaxError("{} : {}".format(repr(self.current_token), error_message))
        self.advance()

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


def test():
    # from common_lexer import CommonLexer

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
