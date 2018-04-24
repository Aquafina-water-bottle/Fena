from abc import ABC, abstractmethod

from lexical_token import Token
from token_position import TokenPosition, TokenPositionRecorder
from token_types import WhitespaceToken

class CommonLexer(ABC):
    """
    Iterator object to get all tokens in a file

    Args:
        text (str)
        initial_pos (TokenPosition or None)
    """

    def __init__(self, class_name, text, initial_pos=None):
        self.class_name = class_name
        self.text = text
        self.recorder = TokenPositionRecorder(initial_pos=initial_pos)
        self.reached_eof = False

    @classmethod
    def from_lexer(self, class_name, lexer):
        self.class_name = class_name
        self.text = lexer.text
        self.recorder = lexer.recorder
        self.reached_eof = False

    @abstractmethod
    def __iter__(self):
        pass

    def advance(self, increment=1):
        """
        Advances the position

        Args:
            increment (int): Number of chars that will be incremented
        """
        assert isinstance(increment, int)

        # while loop to increment the self.recorder variable
        while increment > 0 and not self.reached_eof:

            # if the current character is \n, goes to a new line
            # note that the position increments after this, meaning
            # that "\n" is actually the previous character
            if self.current_chars_are(WhitespaceToken.NEWLINE.value):
                self.recorder.increment_row()
            else:
                self.recorder.increment_column()

            if self.recorder.char_pos > len(self.text) - 1:
                self.reached_eof = True

            increment -= 1

    def error(self, message=None):
        """
        Args:
            class_name (str): Name of the class that will implement this
            message (str or None): Message to be displayed with the error.
                Defaults to None, which will display a generic message containing the current character
        """
        if message is None:
            message = "Invalid character {char}".format(char=repr(self.get_char()))
        raise TypeError("{name}{pos}: {message}".format(name=self.class_name, pos=self.recorder, message=message))

    def skip_whitespace(self, skip_newline=False):
        """
        Skips all whitespace that isn't a newline
        """
        if skip_newline:
            while not self.reached_eof and self.get_char().isspace():
                self.advance()
        else:
            while not self.reached_eof and self.get_char().isspace() and not self.current_chars_are(WhitespaceToken.NEWLINE.value):
                self.advance()


    def advance_chars(self, chars):
        """
        Advances given the number of characters

        Args:
            chars (str)
        """
        assert isinstance(chars, str)
        self.advance(len(chars))

    def get_char(self):
        """
        Args:
            length (int, optional) number of characters from the current position

        Returns:
            int: current characters from the current position given the length
        """
        if self.reached_eof:
            return None
        char_pos = self.recorder.char_pos
        return self.text[char_pos]

    def get_chars(self, length):
        """
        Args:
            length (int, optional) number of characters from the current position

        Returns:
            str: current characters from the current position given the length
        """
        char_pos = self.recorder.char_pos
        return self.text[char_pos: char_pos + length]

    def get_locked_chars(self):
        """
        Returns:
            str: current characters from the locked position to the current position
        """
        begin, end = self.recorder.locked_char_pos
        return self.text[begin:end]

    def current_chars_are(self, chars):
        """
        Looks ahead to compare characters

        Args:
            chars (str): characters provided to compare to the current string
        
        Returns
            bool: whether the characters provided equal to the current string
        """
        length = len(chars)
        return chars == self.get_chars(length)

    def create_new_token(self, token_type, value=None, position=None, advance=False, unlock=False):
        """
        Creates a new token and automatically fills out the token fields unless specified

        If the current state of the position is locked, it gets the locked chars instead

        Args:
            value (any, defaults to None): What value the token should have
            position (TokenPosition, defaults to None): The position of the current token
            advance (bool, defaults to False): Whether to advance after creating the token or not
            unlock (bool, defaults to False): Whethre to unlock after creating the token or not
        """
        if position is None:
            position = self.recorder.position

        if self.recorder.locked:
            value = self.get_locked_chars()

        token = Token(position, token_type, value)

        if unlock:
            self.recorder.unlock()

        if advance:
            self.advance_chars(token.value)

        return token

    @abstractmethod
    def __repr__(self):
        if self.reached_eof:
            return "CommonLexer[pos={}, reached_eof={}]".format(repr(self.recorder), self.reached_eof)
        return "CommonLexer[pos={}, reached_eof={}, current_char={}]".format(repr(self.recorder), self.reached_eof, repr(self.get_char()))
