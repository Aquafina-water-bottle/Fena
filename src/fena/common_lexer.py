from lexical_token import Token
from token_position import TokenPosition, TokenPositionRecorder
from abc import ABC, abstractmethod

class CommonLexer(ABC):
    """
    Args:
        text (str)
        initial_pos (TokenPosition or None)
    """

    def __init__(self, text, initial_pos=None):
        self.text = text
        self.position = TokenPositionRecorder()
        self.reached_eof = False

    @abstractmethod
    def error(self, class_name, message=None):
        """
        Args:
            class_name (str): Name of the class that will implement this
            message (str or None): Message to be displayed with the error.
                Defaults to None, which will display a generic message containing the current character
        """
        if message is None:
            message = "Invalid character {char}".format(char=self.get_char())
        raise TypeError("{name}{pos}: {message}".format(name=class_name, pos=self.position, message=message))

    @abstractmethod
    def get_next_token(self):
        pass

    @abstractmethod
    def advance(self, increment=1):
        """
        Advances the position

        Args:
            increment (int): Number of chars that will be incremented
        """
        pass

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
        char_pos = self.position.char_pos
        return self.text[char_pos]

    def get_chars(self, length):
        """
        Args:
            length (int, optional) number of characters from the current position

        Returns:
            str: current characters from the current position given the length
        """
        char_pos = self.position.char_pos
        return self.text[char_pos: char_pos + length]

    def get_locked_chars(self):
        """
        Returns:
            str: current characters from the locked position to the current position
        """
        begin, end = self.position.get_locked_char_pos()
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
            position = self.position.create_instance()

        if self.position.locked:
            value = self.get_locked_chars()

        token = Token(position, token_type, value)

        if unlock:
            self.position.unlock()

        if advance:
            self.advance_chars(token.value)

        return token

    @abstractmethod
    def __repr__(self):
        pass