class CommonLexer:
    def __new__(cls, lexer_type, token):
        """
        Ensures that there is only one class instance for the given lexer type
        by creating and getting the class attribute of _{lexer_type}
        """
        attr_name = "_{}".format(lexer_type)
        if not hasattr(cls, attr_name):
            setattr(cls, attr_name, super().__new__(cls))
            print(attr_name)
            # cls._selector_lexer = super().__new__(cls)

        return getattr(cls, attr_name)
        # return cls._selector_lexer
        
    def __init__(self, lexer_type, token):
        self.token = token
        self.lexer_type = lexer_type
        self.pos = 0

    def advance(self):
        self.pos += 1

    def get_next_token(self):
        pass

    def __str__(self):
        return "CommonLexer[token={}, lexer_type={}, pos={}]".format(self.token, self.lexer_type, self.pos)

    def __repr__(self):
        pass