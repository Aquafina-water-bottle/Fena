import Common.lexicalToken


class Token(Common.lexicalToken.Token):
    def __str__(self):
        return repr(self.value)

    def forCommand(self):
        return str(self.value)

    def matchesOne(self, *types):
        """
        returns whether the token matches any one of the types

        :param types: any number of types
        :return:
        """
        for type in types:
            if isinstance(type, tuple):
                if self.type == type[0] and self.value == type[1]:
                    return True
            elif self.type == type:
                return True
        return False

    def matches(self, type, value=None):
        """
        returns whether the token matches the given type and/or value

        :param type:
        :param value:
        :return:
        """
        if isinstance(type, tuple):
            return self.type == type[0] and self.value == type[1]
        return (self.type == type) and (value is None or self.value == value)

    @staticmethod
    def toCommand(tokenList):
        return " ".join([str(token.value) for token in tokenList])

    @staticmethod
    def toCommandRepr(tokenList):
        return " ".join([str(token) for token in tokenList])



