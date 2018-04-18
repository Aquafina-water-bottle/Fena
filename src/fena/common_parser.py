class CommonParser:
    """
    Singleton class to parse a selector to reduce initialization costs

    parser() and __repr__() are meant to be overriden

    Args:
        lexer (CommonLexer)
        parser_type (str)

    Attributes:
        lexer (CommonLexer)
        parser_type (str)
        current_token (Token)
    """

    def __new__(cls, parser_type, lexer):
        """
        Ensures that there is only one class instance for the given parser type
        by creating and getting the class attribute of _{parser_type}
        """
        attr_name = "_{}".format(parser_type)
        if not hasattr(cls, attr_name):
            setattr(cls, attr_name, super().__new__(cls))
            print(attr_name)
            # cls._selector_parser = super().__new__(cls)

        return getattr(cls, attr_name)
        # return cls._selector_parser
        
    def __init__(self, parser_type, lexer):
        self.lexer = lexer
        self.parser_type = parser_type
        self.current_token = None
        # self.current_token = self.advance()

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type, error_message=None):
        if error_message is None:
            error_message = "Selector Syntax Error"
        if not self.current_token.type.matches(token_type):
            raise SyntaxError("{} : {}".format(repr(self.current_token), error_message))
        self.advance()

    def parse(self):
        pass

    def __str__(self):
        return "CommonParser[lexer={}, parser_type={}, current_token={}]".format(self.lexer, self.parser_type, self.current_token)

    def __repr__(self):
        pass


def test():
    class Test(CommonParser):
        pass

    t = Test("test", 1)
    c = CommonParser("common_test", 1)
    t2 = Test("test", 1)

    print(tuple(map(id, (t, t2, c))))
    print(vars(t))


if __name__ == "__main__":
    test()
