class Token:
    def __init__(self, pos, type, value=None):
        """
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

    def getPos(self):
        if self.pos is None:
            return "None"

        elif len(self.pos) == 2:
            line, column = self.pos
            return "Line {0} column {1}".format(line, column)

        else:
            line, column, length = self.pos
            return "Line {0} column {1}-{2}".format(line, column, column+length)

    def __repr__(self):
        """String representation of the class instance.
        Examples:
            Token((2, 5): INTEGER, 3)
            Token((32, 12): PLUS, '+')
            Token((1, 52): MUL, '*')
        """
        return 'Token({0}: type={1}, value={2})'.format(self.getPos(), repr(self.type), repr(self.value))
