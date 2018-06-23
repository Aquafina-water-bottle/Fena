from fenalib.assert_utils import assert_type
import logging

class TokenPositionRecorder:
    """
    Mutable version of the TokenPosition that has no length, used during token creation

    Args:
        initial_pos (TokenPosition or None): The starting position of the position recorder

    Attributes:
        char_pos (int): The position within the entire file string
        row (int): What row the char_pos is at
        column (int): What column the char_pos is at
        started (bool): Whether the recorder has started or not

        locked (bool):
        locked_token_pos (TokenPosition): Records the position of the initial character of the lock
    """

    def __init__(self, initial_pos=None):
        self.char_pos = 0

        if initial_pos is None:
            initial_pos = TokenPosition(row=1, column=1, char_pos=0)
        
        self.position = initial_pos
        self.locked = False
        self.locked_token_pos = None

    @property
    def position(self):
        """
        Creates an immutable instance of itself to be used for token creation

        Returns:
            TokenPosition: Position of the current token

        Examples:
            >>> r = TokenPositionRecorder()
            >>> r.position
            TokenPosition[row=1, column=1, char_pos=0]

            >>> r.increment_column(22)
            >>> r.position
            TokenPosition[row=1, column=23, char_pos=22]
        """
        token_pos = TokenPosition(self.row, self.column, self.char_pos)
        if self.locked:
            return TokenPosition.from_positions(self.locked_token_pos, token_pos)
        return token_pos

    @position.setter
    def position(self, position):
        """
        Creates an immutable instance of itself to be used for token creation

        Args:
            position (TokenPosition): Position that the recorder will be changed to
        """
        assert_type(position, TokenPosition)

        # self.char_pos = position.char_pos
        self.row = position.row
        self.column = position.column

    def increment_column(self, columns=1):
        """
        Increments the column value
        
        Args:
            columns (int): Number of columns to increment

        Examples:
            >>> r = TokenPositionRecorder()
            >>> r
            TokenPositionRecorder[row=1, column=1, char_pos=0]

            >>> r.increment_column()
            >>> r
            TokenPositionRecorder[row=1, column=2, char_pos=1]

            >>> r.increment_column(5)
            >>> r
            TokenPositionRecorder[row=1, column=7, char_pos=6]
        """
        assert_type(columns, int)
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
            TokenPositionRecorder[row=1, column=1, char_pos=0]

            >>> r.increment_column()
            >>> r
            TokenPositionRecorder[row=1, column=2, char_pos=1]

            Upon incrementing the row, the column resets
            >>> r.increment_row()
            >>> r
            TokenPositionRecorder[row=2, column=1, char_pos=2]

            >>> r.increment_column(4)
            >>> r
            TokenPositionRecorder[row=2, column=5, char_pos=6]

            >>> r.increment_row()
            >>> r
            TokenPositionRecorder[row=3, column=1, char_pos=7]
        """
        self.column = 1
        self.row += 1
        self.char_pos += 1

    def lock(self):
        """
        Locks the starting position to process a multi-character string
        by setting the beginning integer slice as char_pos, and letting char_pos advance
        """

        # if not originally locked, does normal thing
        if not self.locked:
            self.locked = True
            self.locked_token_pos = TokenPosition(self.row, self.column, self.char_pos)
        # otherwise, warning
        else:
            logging.warning("{}: Unexpected lock before unlock".format(self))

    @property
    def locked_char_pos(self):
        """
        Returns:
            tuple (int, int): The character positions to get the proper slice of the string
        """
        return self.locked_token_pos.char_pos, self.char_pos

    def unlock(self, undo_progress=False):
        """
        Args:
            undo_progress (bool): Whether the character position resets itself back to its original position or not
        """
        if not self.locked:
            logging.warning("{}: Unexpected unlock before lock".format(self))
        self.locked = False

        if undo_progress:
            original_pos = self.locked_token_pos
            self.char_pos = original_pos.char_pos
            self.row = original_pos.row
            self.column = original_pos.column

        self.locked_token_pos = None

    def __str__(self):
        return "[row={}, col={}]".format(self.row, self.column)

    def __repr__(self):
        # if self.initial_char_pos == 0:
        #     char_pos = str(self.char_pos)
        # else:
        #     char_pos = "({} from initial={} + current={})".format(self.char_pos + self.initial_char_pos, self.initial_char_pos, self.char_pos)

        # return "TokenPositionRecorder[row={}, column={}, char_pos={}]".format(self.row, self.column, char_pos)
        return "TokenPositionRecorder[row={}, column={}, char_pos={}]".format(self.row, self.column, self.char_pos)


class TokenPosition(tuple):
    """
    Immutable Token Position used in each token to hold their position and length of token

    Immutable object gotten from https://stackoverflow.com/a/4828108

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

    __slots__ = []

    def __new__(cls, row, column, char_pos, row_end=None, column_end=None, char_pos_end=None):
        assert_type(row, int) and row > 0
        assert_type(column, int) and column > 0
        assert_type(char_pos, int) and char_pos >= 0
        
        if row_end is None:
            row_end = row
        if column_end is None:
            column_end = column
        if char_pos_end is None:
            char_pos_end = char_pos

        assert_type(row_end, int) and row_end > 0
        assert_type(column_end, int) and column_end > 0
        assert_type(char_pos_end, int) and char_pos_end >= 0
        return super().__new__(cls, (row, row_end, column, column_end, char_pos, char_pos_end))

        # self._row_begin = row
        # self._row_end = row_end
        # self._column_begin = column
        # self._column_end = column_end
        # self._char_pos = char_pos
        # self._char_pos_end = char_pos_end

    @ classmethod
    def from_positions(cls, token_pos, token_pos_end=None):
        # sets it to a smaller name so it doesn't take up as much room
        tp, tpe = token_pos, token_pos_end
        if token_pos_end is None:
            return cls(tp.row, tp.column, tp.char_pos)
        return cls(tp.row, tp.column, tp.char_pos, tpe.row, tpe.column, tpe.char_pos)

    @property
    def row(self):
        return super().__getitem__(0)

    @property
    def row_end(self):
        return super().__getitem__(1)

    @property
    def column(self):
        return super().__getitem__(2)

    @property
    def column_end(self):
        return super().__getitem__(3)

    @property
    def char_pos(self):
        return super().__getitem__(4)

    @property
    def char_pos_end(self):
        return super().__getitem__(5)

    def __getitem__(self, item):
        raise TypeError("{} object does not support indexing".format(repr(__class__.__name__)))

    def __str__(self):
        if self.row == self.row_end:
            if self.column == self.column_end:
                # both rows and columns lead to the same position
                return "[row={}, col={}]".format(self.row, self.column)

            # otherwise, columns are different but rows are the same
            return "[row={}, col=({} to {})]".format(self.row, self.column, self.column_end)

            # otherwise, rows are different and are leading to completely different places
        return "[(row={}, col={}) to (row={}, col={})]".format(self.row, self.column, self.row_end, self.column_end)

    def __repr__(self):
        if self.char_pos == self.char_pos_end:
            char_pos_repr = "char_pos={}".format(self.char_pos)
        else:
            char_pos_repr = "char_pos=({} to {})".format(self.char_pos, self.char_pos_end)

        if self.row == self.row_end:
            if self.column == self.column_end:
                # both rows and columns lead to the same position
                return "TokenPosition[row={}, column={}, {}]".format(self.row, self.column, char_pos_repr)

            # otherwise, columns are different but rows are the same
            return "TokenPosition[row={}, column=({} to {}), {}]".format(self.row, self.column, self.column_end, char_pos_repr)

            # otherwise, rows are different and are leading to completely different places
        return "TokenPosition[(row={}, column={}) to (row={}, col={}), {}]".format(self.row, self.column, self.row_end, self.column_end, char_pos_repr)

def test():
    pass

def test_docs():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test_docs()
    # test()
