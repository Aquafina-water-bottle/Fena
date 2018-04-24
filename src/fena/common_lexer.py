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

    @classmethod
    def from_lexer(self, class_name, lexer):
        self.class_name = class_name
        self.text = lexer.text
        self.recorder = lexer.recorder
        self.reached_eof = False

    @abstractmethod
    def __iter__(self):
        pass


    @abstractmethod
    def __repr__(self):
        if self.reached_eof:
            return "CommonLexer[pos={}, reached_eof={}]".format(repr(self.recorder), self.reached_eof)
        return "CommonLexer[pos={}, reached_eof={}, current_char={}]".format(repr(self.recorder), self.reached_eof, repr(self.get_char()))
