if __name__ == "__main__":
    import logging_setup

import logging

from token_types import TokenType, SimpleToken, WhitespaceToken, StatementToken, SelectorTokenType, SelectorSimpleToken, ALL_TYPES, SELECTOR_SIMPLE_TOKENS_VALUES
from config_data import ConfigData
from lexical_token import Token
from token_position import TokenPosition, TokenPositionRecorder
from selector import Selector

class Lexer:
    config_data = ConfigData()

    def __init__(self, text):
        self.text = text

        # whether the end of the file has been reached or not
        self.reached_eof = False

        # row, column
        self.position = TokenPositionRecorder()

        # list of indent strings
        # 1 indent is either 4 spaces or 1 tab space
        self.indents = 0

        self.returned_newline = False
        self.handle_newline(beginning_line=True)

        # bool returns true if it is a zero length string or complete whitespace
        if not self.text.strip():
            raise EOFError("File does not contain anything")

    def error(self, message=None):
        if message is None:
            raise TypeError("{}: Invalid character '{}'".format(self.position, self.get_char()))
        raise TypeError("{}: {}".format(self.position, message))

    def advance_chars(self, chars):
        """
        Advances given the number of characters

        Args:
            chars (str)
        """
        assert isinstance(chars, str)
        self.advance(len(chars))

    def advance(self, increment=1):
        """
        Advance the "pos" pointer and set the "current_char" variable.

        Args:
            increment (int): Number of chars that will be incremented
        """
        assert isinstance(increment, int)

        # while loop to increment the self.position variable
        while increment > 0 and not self.reached_eof:

            # if the current character is \n, goes to a new line
            # note that the position increments after this, meaning
            # that "\n" is actually the previous character
            if self.current_chars_are(WhitespaceToken.NEWLINE.value):
                self.position.increment_row()
            else:
                self.position.increment_column()

            if self.position.char_pos > len(self.text) - 1:
                self.reached_eof = True

            increment -= 1

    def create_new_token(self, token_type, value=None, position=None, advance=False):
        """
        Creates a new token and automatically fills out the position

        If the current state of the position is locked, it gets the locked chars instead

        Args:
            value (any, defaults to None): What value the token should have
            position (TokenPosition, defaults to None): the position of the current token
            advance (bool, defaults to False): Whether when creating the token, it should advance afterwards or not
        """
        if position is None:
            position = self.position.create_instance()

        if self.position.locked:
            value = self.get_locked_chars()

        token = Token(position, token_type, value)

        if advance:
            self.advance_chars(token.value)

        return token

    # def get_next_token(self, for_selector=False):
    def get_next_token(self):
        """
        This method is responsible for breaking a sentence
        apart into tokens, one token at a time.
        """

        # does not require "else" since if it is a selector, it should end in the block above
        while not self.reached_eof:
            # skips all whitespace until \n
            if self.get_char().isspace() and not self.current_chars_are(WhitespaceToken.NEWLINE.value):
                self.skip_whitespace()
                continue

            # handles indents and dedents after newline
            if self.current_chars_are(WhitespaceToken.NEWLINE.value):
                # can return a single indent token, single dedent token or nothing at all
                # this will be ran multiple times if there are multiple dedents in one line
                whitespace_token = self.handle_newline()
                if whitespace_token is not None:
                    return whitespace_token
                continue

            if self.current_chars_are(SimpleToken.OPEN_PARENTHESES.value):
                return self.create_new_token(SimpleToken.OPEN_PARENTHESES, advance=True)

            if self.current_chars_are(SimpleToken.CLOSE_PARENTHESES.value):
                return self.create_new_token(SimpleToken.CLOSE_PARENTHESES, advance=True)

            if self.current_chars_are(SimpleToken.COMMA.value):
                return self.create_new_token(SimpleToken.COMMA, advance=True)

            if self.current_chars_are(SimpleToken.COLON.value):
                return self.create_new_token(SimpleToken.COLON, advance=True)

            # gets selector
            if self.current_chars_are("@"):
                return self.get_selector()

            # gets datatag
            if self.current_chars_are("{"):
                return self.get_data_tag()

            return self.get_string()

        # at the end of file by this point, and it must end with dedent tokens if a newline did not end
        if self.indents > 0:
            return self.get_dedent()

        return self.create_new_token(WhitespaceToken.EOF)

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

    def skip_whitespace(self):
        """
        Skips all whitespace that isn't a newline
        """
        while not self.reached_eof and self.get_char().isspace() and not self.current_chars_are(WhitespaceToken.NEWLINE.value):
            self.advance()

    def skip_comment(self):
        while not self.reached_eof and not self.current_chars_are(WhitespaceToken.NEWLINE.value):
            self.advance()

    def get_indent(self):
        """
        Gets a singular indent token and adds one from the indent length
        """

        self.indents += 1
        return self.create_new_token(WhitespaceToken.INDENT)

    def get_dedent(self):
        """
        Gets a singular dedent token and subtracts one from the indent length
        """

        self.indents -= 1
        return self.create_new_token(WhitespaceToken.DEDENT)

    def handle_newline(self, beginning_line=False):
        """
        Once a newline is hit, it creates the given number of indent or dedent tokens
        It only advances if all possible tokens have been created or the line is
        either an empty line or a comment

        Args:
            beginning_line (bool): Whether the current line is the first line of the file or not
        """
        if not self.returned_newline and not beginning_line:
            self.returned_newline = True
            return self.create_new_token(WhitespaceToken.NEWLINE)

        self.position.lock()

        # skips the newline
        if not beginning_line:
            self.advance()

        # gets any whitespace
        self.skip_whitespace()

        # if the current char is a comment after whitespace, it is still an empty line
        current_char = self.get_char()
        if current_char == WhitespaceToken.NEWLINE.value:
            self.position.unlock()
            self.returned_newline = False
            return

        if current_char == WhitespaceToken.COMMENT.value:
            self.skip_comment()
            self.position.unlock()
            self.returned_newline = False
            return

        # otherwise, the whitespace is valid for interpretation for indents and dedents
        # gets the string value while removing the newline
        whitespace = self.get_locked_chars()[1:]
        self.position.unlock(undo_progress=True)

        # checks whether the indenting whitespace is actually valid
        # boolean value of any integer is False if 0, True for anything else
        if len(whitespace) % len(WhitespaceToken.INDENT.value):
            # advances to skip the newline and report the error at the proper line
            self.advance()
            self.error("Invalid whitespace: {}".format(repr(whitespace)))

        # gets the number of indents at the current area
        current_indents = whitespace.count(WhitespaceToken.INDENT.value)

        if current_indents > self.indents:
            if current_indents-1 == self.indents:
                # doesnt skip the newline and indent to run this function once more to get to
                # the case where number of indents on the line are equal to the current indentation
                return self.get_indent()

            else:
                self.advance()
                self.error("Too many indents")

        if current_indents < self.indents:
            return self.get_dedent()

        # guaranteed to be current_indents == self.indents
        # no dedent and indent tokens will be made unless already made, so all whitespace will be skipped
        self.advance()
        self.returned_newline = False
        self.skip_whitespace()

        # however, there are certain things that can only happen after a valid newline,
        # most notably the statement token
        if self.current_chars_are(SimpleToken.STATEMENT.value):
            return self.create_new_token(SimpleToken.STATEMENT, advance=True)

    def get_data_tag(self):
        # skips the first curly bracket
        result = "{"
        curly_brackets = 1
        self.advance()

        original_pos = self.position.create_instance()
        self.position.lock()

        while not self.reached_eof and curly_brackets > 0:
            # handles comments
            if self.current_chars_are(WhitespaceToken.NEWLINE.value):
                # unlocks so newlines and whitespace are not included in the result
                result += self.get_locked_chars()
                self.position.unlock()

                # skips newline
                self.advance()
                self.skip_whitespace()

                if self.get_char() == WhitespaceToken.COMMENT.value:
                    self.skip_comment()

                self.position.lock()
                continue

            if self.current_chars_are("{"):
                curly_brackets += 1
            if self.current_chars_are("}"):
                curly_brackets -= 1
            self.advance()

        result += self.get_locked_chars()
        self.position.unlock()

        # gets a new token position from the original position and the current position
        token_pos = TokenPosition.from_positions(original_pos, self.position.create_instance())
        return self.create_new_token(TokenType.DATATAG, value=result, position=token_pos)

    def get_selector(self):
        # current_token = None
        # selector_tokens = []
        # while current_token is None or not current_token.matches_any_of(SelectorSimpleToken.END, SimpleToken.COLON):
        #     current_token = self.get_next_token(for_selector=True)
        #     selector_tokens.append(current_token)

        self.position.lock()
        if self.get_chars(2) not in self.config_data.target_selector_variables:
            self.error("Expected a selector in {}, got {}".format(self.config_data.target_selector_variables, self.get_chars(2)))
        self.advance(2)

        # checks whether more of a selector is expected
        if self.current_chars_are("["):
            while not self.current_chars_are("]"):
                self.advance()

            # skips the "]"
            self.advance()

        token = self.create_new_token(TokenType.SELECTOR)
        self.position.unlock()

        return token
            
    def get_string(self):
        """
        Simply gets the current string until next whitespace

        Returns:
            str: concatenation of the current chars until the next whitespace
        """
        self.position.lock()

        current_char = self.get_char()
        # otherwise, it just stops when it is a whitespace character or it isn't a special delimiter character
        while not self.reached_eof and not current_char.isspace() and not current_char in ":(),":
            self.advance()
            current_char = self.get_char()

        # result = self.get_locked_chars()
        # self.position.unlock()

        # checks if the result is a 0 length string: error
        if not self.get_locked_chars():
            self.error("Got a 0 length string")

        token = self.create_new_token(TokenType.STRING)
        self.position.unlock()

        return token

        # # gets any predefined simple token
        # for simple_token in SimpleToken:
        #     if result == simple_token.value:
        #         return Token(tokenPos, simple_token)

        # # gets leading commands
        # for command in options[LEADING_COMMANDS]:
        #     if result == command:
        #         return Token(tokenPos, LEADING_COMMAND, command)

        # # gets any command
        # for command in options[COMMANDS]:
        #     if result == command:
        #         return Token(tokenPos, COMMAND, command)

        # return Token(tokenPos, STRING, result)

    def test(self):
        # token = self.get_next_token()
        # print(repr(token))
        while not self.reached_eof:
            # self.get_next_token()
            token = self.get_next_token()
            logging.debug(repr(token))

if __name__ == "__main__":
    import timeit

    with open("test_lexer.txt") as file:
        text = file.read()

    # number = 20
    # print(timeit.timeit("lexer = Lexer(text); lexer.test()", number=number, globals=globals()))
    lexer = Lexer(text)
    lexer.test()
