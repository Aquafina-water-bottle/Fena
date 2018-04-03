class Token:
    def __init__(self, pos, type, value=None):
        """
        Args:
            pos (tuple (int, int)): position inside the file formatted as (line, column)
            type (str): type
            type (str, str): both type and value
            value: a custom value

        Accepts one of the following:
            str type,        (int, int) pos
            (str, str) type, (int, int) pos
            str type,        (int, int) pos,    value=custom
        """
        self.pos = pos
        self.type = None
        self.value = None

        if isinstance(type, tuple):  # tuple with repr, value
            self.type, self.value = type
        elif value is None:
            self.type = self.value = type
        else:
            self.value = value
            self.type = type

    @staticmethod
    def tokenListStr(tokenList):
        return " ".join((token.value for token in tokenList))

    def getPos(self):
        if self.pos is None:
            return "None"

        elif len(self.pos) == 2:
            line, column = self.pos
            return "Line {0} column {1}".format(line, column)

        else:
            line, column, length = self.pos
            return "Line {0} column {1}-{2}".format(line, column, column+length)

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

    def __str__(self):
        return repr(self.value)

    def __repr__(self):
        """String representation of the class instance.
        Examples:
            Token((2, 5): INTEGER, 3)
            Token((32, 12): PLUS, '+')
            Token((1, 52): MUL, '*')
        """
        return 'Token({0}: type={1}, value={2})'.format(self.getPos(), repr(self.type), repr(self.value))

    def forCommand(self):
        return str(self.value)

    @staticmethod
    def toCommand(tokenList):
        return " ".join([str(token.value) for token in tokenList])

    @staticmethod
    def toCommandRepr(tokenList):
        return " ".join([str(token) for token in tokenList])



