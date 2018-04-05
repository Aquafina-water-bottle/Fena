import logging

class TokenPositionRecorder:
    """
    Mutable version of the TokenPosition that has no length, used during token creation
    Args:
        char_pos (int): The position within the entire file string
        row (int): What row the char_pos is at
        column (int): What column the char_pos is at
        started (bool): Whether the recorder has started or not

        locked (bool):
        locked_char_pos (int)
        locked_token_pos (TokenPosition): Records the position of the initial character of the lock
    """

    def __init__(self):
        self.char_pos = 0
        self.row = 1
        self.column = 1
        # self.started = False

        self.locked = False
        self.locked_char_pos = self.char_pos
        self.locked_token_pos = None

    def create_instance(self, length=1):
        """
        Creates an immutable instance of itself to be used for token creation

        Args:
            length (int): The length of the token (defaults to length of 1)

        Returns:
            TokenPosition: Position of the current token

        Examples:
            >>> r = TokenPositionRecorder()
            >>> r.create_instance()
            TokenPosition[row=None, column=None]

            >>> r.create_instance()
            TokenPosition[row=1, column=1]

            >>> r.increment_column(22)
            >>> r.create_instance(6)
            TokenPosition[row=1, column=(23 to 29)]

.           >>> r.create_instance()
            TokenPosition[row=None, column=None]
        """
        return TokenPosition(self.row, self.column, length)

    def increment_column(self, columns=1):
        """
        Increments the column value
        
        Args:
            columns (int): Number of columns to increment

        Examples:
            >>> r = TokenPositionRecorder()
            >>> r
            TokenPositionRecorder[char_pos=0, row=1, column=1]

            >>> r.increment_column()
            >>> r
            TokenPositionRecorder[char_pos=1, row=1, column=2]

            >>> r.increment_column(5)
            >>> r
            TokenPositionRecorder[char_pos=6, row=1, column=7]
        """
        assert isinstance(columns, int)
        self.column += columns
        self.char_pos += columns

    def increment_row(self):
        """
        Increments the row and resets the column value

        There are no arguments for a row since one you go down one row, it is expected you are going
        from the end of the previous line and to the beginning of a new line

        Examples:
            >>> r = TokenPositionRecorder()
            >>> r
            TokenPositionRecorder[char_pos=0, row=1, column=1]

            >>> r.increment_column()
            >>> r
            TokenPositionRecorder[char_pos=1, row=1, column=2]

            Upon incrementing the row, the column resets
            >>> r.increment_row()
            >>> r
            TokenPositionRecorder[char_pos=2, row=2, column=1]

            >>> r.increment_column(4)
            >>> r
            TokenPositionRecorder[char_pos=6, row=2, column=5]

            >>> r.increment_row()
            >>> r
            TokenPositionRecorder[char_pos=7, row=3, column=1]
        """
        self.column = 1
        self.row += 1
        self.char_pos += 1

    def lock(self):
        """
        Locks the starting position to process a multi-character string
        by setting the beginning integer slice as char_pos, and letting char_pos advance

        Returns:
            TokenPosition: The current position
        """

        # if not originally locked, does normal thing
        if not self.locked:
            self.locked = True
            self.locked_char_pos = self.char_pos
        # otherwise, warning
        else:
            logging.warning("{}: Unexpected lock before unlock".format(self))

        return self.create_instance()

    def get_locked_char_pos(self):
        """
        Returns:
            tuple (int, int): The character positions to get the proper slice of the string
        """
        return self.locked_char_pos, self.char_pos

    def unlock(self, undo_progress=False):
        """
        Args:
            undo_progress (bool): Whether the character position resets itself back to its original position or not

        Returns:
            TokenPosition: The current position
        """
        self.locked = False

        if undo_progress:
            self.char_pos = self.locked_char_pos
        self.locked_pos = None
        self.locked_token_pos = None

        return self.create_instance()

    def __str__(self):
        return "[row={}, col={}]".format(self.row, self.column)

    def __repr__(self):
        return "TokenPositionRecorder[char_pos={}, row={}, column={}]".format(self.char_pos, self.row, self.column)


class TokenPosition:
    """
    Immutable Token Position used in each token to hold their position and length of token

    Args:
        row (int): What row the token is at in the file, defaults to None for a token that doesn't exist
        column (int): What column the token is at in the file, defaults to None for a token that doesn't exist
        length (int): length of a multi character token, defaults to 1

    Representation of rows and columns:
        column:   1   2   3   4  
        row: 1: |   |   |   |   |
             2: |   |   |   |   |
             3: |   |   |   |   |
             4: |   |   |   |   |
    """

    def __init__(self, row, column, length=1):
        assert row is None or (isinstance(row, int) and row > 0)
        assert column is None or (isinstance(column, int) and column > 0)
        assert isinstance(length, int) and length > 0

        self._row = row
        self._column = column
        self._length = length

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def length(self):
        return self._length

    @property
    def end_column(self):
        return self.column + self.length

    def __str__(self):
        if self.length == 1:
            return "[row={}, col={}]".format(self.row, self.column)
        return "[row={}, col=({} to {})]".format(self.row, self.column, self.end_column)

    def __repr__(self):
        if self.length == 1:
            return "TokenPosition[row={}, column={}]".format(self.row, self.column)
        return "TokenPosition[row={}, column=({} to {})]".format(self.row, self.column, self.end_column)


def test():
    pass

def test_docs():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test_docs()
    # test()
