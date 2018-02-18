import Common.lexicalToken


class Token(Common.lexicalToken.Token):
    def __str__(self):
        return repr(self.value)

    def forCommand(self):
        return str(self.value)

    @staticmethod
    def toCommand(tokenList):
        return " ".join([str(token.value) for token in tokenList])

    @staticmethod
    def toCommandRepr(tokenList):
        return " ".join([str(token) for token in tokenList])



