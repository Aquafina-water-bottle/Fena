if __name__ == "__main__":
    import logging_setup

import logging

from token_types import TokenType, SimpleToken, WhitespaceToken, StatementToken, SelectorTokenType, SelectorSimpleToken, ALL_TYPES, SELECTOR_SIMPLE_TOKENS_VALUES
from config_data import ConfigData
from lexical_token import Token
from token_position import TokenPosition, TokenPositionRecorder
from common_lexer import CommonLexer
from statement_lexer import StatementLexer

class Lexer(CommonLexer):
    config_data = ConfigData()

    def __init__(self, text):
        super().__init__(text)

        # list of indent strings
        # 1 indent is either 4 spaces or 1 tab space
        self.indents = 0

        self.returned_newline = False
        self.handle_newline(beginning_line=True)
        self.statement_lexer = StatementLexer()

        # bool returns true if it is a zero length string or complete whitespace
        if not self.text.strip():
            raise EOFError("File does not contain anything")

    def __iter__(self):
        """
        This method is responsible for breaking a sentence
        apart into tokens, one token at a time.
        """
        # yield from self.statement_lexer
        # if not self.statement_lexer.reached_eof:
        #     yield next(self.statement_lexer)

        # does not require "else" since if it is a selector, it should end in the block above
        while not self.reached_eof:
            # skips all whitespace until \n
            if self.get_char().isspace() and not self.current_chars_are(WhitespaceToken.NEWLINE.value):
                self.skip_whitespace()
                continue

            yield from self.statement_lexer

            # handles indents and dedents after newline
            if self.current_chars_are(WhitespaceToken.NEWLINE.value):
                # can return a single indent token, single dedent token or nothing at all
                # this will be ran multiple times if there are multiple dedents in one line
                whitespace_token = self.handle_newline()
                if whitespace_token is not None:
                    yield whitespace_token
                continue

            yield self.get_command()

            # if self.current_chars_are(SimpleToken.OPEN_PARENTHESES.value):
            #     return self.create_new_token(SimpleToken.OPEN_PARENTHESES, advance=True)

            # if self.current_chars_are(SimpleToken.CLOSE_PARENTHESES.value):
            #     return self.create_new_token(SimpleToken.CLOSE_PARENTHESES, advance=True)

            # if self.current_chars_are(SimpleToken.COMMA.value):
            #     return self.create_new_token(SimpleToken.COMMA, advance=True)

            # if self.current_chars_are(SimpleToken.COLON.value):
            #     return self.create_new_token(SimpleToken.COLON, advance=True)

            # gets selector
            # if self.current_chars_are("@"):
            #     return self.get_selector()

            # gets datatag
            # if self.current_chars_are("{"):
            #     return self.get_data_tag()

            # return self.get_string()

        # at the end of file by this point, and it must end with dedent tokens if a newline did not end
        if self.indents > 0:
            yield self.get_dedent()

    def error(self, message=None):
        return super().error(__class__.__name__, message)

    def advance(self, increment=1):
        """
        Advance the "pos" pointer and set the "current_char" variable.

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

        self.recorder.lock()

        # skips the newline
        if not beginning_line:
            self.advance()

        # gets any whitespace past the newline
        self.skip_whitespace()

        # if the current char is a comment after whitespace, it is still an empty line
        current_char = self.get_char()
        if current_char == WhitespaceToken.NEWLINE.value:
            self.recorder.unlock()
            self.returned_newline = False
            return

        if current_char == WhitespaceToken.COMMENT.value:
            self.skip_comment()
            self.recorder.unlock()
            self.returned_newline = False
            return

        # otherwise, the whitespace is valid for interpretation for indents and dedents
        # gets the string value while removing the newline
        whitespace = self.get_locked_chars()[1:]
        self.recorder.unlock(undo_progress=True)

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
        if self.current_chars_are(SimpleToken.STATEMENT_SPECIFIER.value):
            # return self.create_new_token(SimpleToken.STATEMENT_SPECIFIER, advance=True)
            statement_token = self.get_statement()
            self.statement_lexer.reset(statement_token.value, statement_token.pos)

    def get_statement(self):
        """
        Gets an entire line all the way to the newline

        Returns:
            str
        """
        self.recorder.lock()

        while not self.reached_eof and self.get_char() != "\n":
            self.advance()

        return self.create_new_token(TokenType.STATEMENT, unlock=True)

    def get_command(self):
        """
        Gets the next command including datatags

        Returns:
            str
        """
        original_pos = self.recorder.position
        self.recorder.lock()

        # otherwise, it just stops when it is a whitespace character or it isn't a special delimiter character
        # TODO: Allow selectors to have datatags
        while not self.reached_eof and not self.get_char() in ("{", "\n"):
            self.advance()

        result = self.get_locked_chars()
        self.recorder.unlock()

        # checks if the result is a 0 length string
        if not result:
            self.error("Got a 0 length string for a command")

        # gets the datatag if possible
        if self.get_char() == "{":
            result += self.get_data_tag()

        token_pos = TokenPosition.from_positions(original_pos, self.recorder.position)

        return self.create_new_token(TokenType.COMMAND, value=result, position=token_pos)

    def get_data_tag(self):
        """
        Returns:
            str
        """
        # skips the first curly bracket
        result = "{"
        curly_brackets = 1
        self.advance()

        self.recorder.lock()

        while not self.reached_eof and curly_brackets > 0:
            # handles comments
            if self.current_chars_are(WhitespaceToken.NEWLINE.value):
                # unlocks so newlines and whitespace are not included in the result
                result += self.get_locked_chars()
                self.recorder.unlock()

                # skips newline
                self.advance()
                self.skip_whitespace()

                if self.get_char() == WhitespaceToken.COMMENT.value:
                    self.skip_comment()

                self.recorder.lock()
                continue

            if self.current_chars_are("{"):
                curly_brackets += 1
            if self.current_chars_are("}"):
                curly_brackets -= 1
            self.advance()

        result += self.get_locked_chars()
        self.recorder.unlock()

        return result

    # def get_selector(self):
    #     # current_token = None
    #     # selector_tokens = []
    #     # while current_token is None or not current_token.matches_any_of(SelectorSimpleToken.END, SimpleToken.COLON):
    #     #     current_token = self.get_next_token(for_selector=True)
    #     #     selector_tokens.append(current_token)

    #     self.recorder.lock()
    #     if self.get_chars(2) not in self.config_data.target_selector_variables:
    #         self.error("Expected a selector in {}, got {}".format(self.config_data.target_selector_variables, self.get_chars(2)))
    #     self.advance(2)

    #     # checks whether more of a selector is expected
    #     if self.current_chars_are("["):
    #         while not self.current_chars_are("]"):
    #             self.advance()

    #         # skips the "]"
    #         self.advance()

    #     token = self.create_new_token(TokenType.SELECTOR)
    #     self.recorder.unlock()

    #     return token
    
    # def get_string(self):
    #     """
    #     Simply gets the current string until next whitespace

    #     Returns:
    #         str: concatenation of the current chars until the next whitespace
    #     """
    #     self.recorder.lock()

    #     current_char = self.get_char()
    #     # otherwise, it just stops when it is a whitespace character or it isn't a special delimiter character
    #     while not self.reached_eof and not current_char.isspace() and not current_char in ":(),":
    #         self.advance()
    #         current_char = self.get_char()

    #     # result = self.get_locked_chars()
    #     # self.recorder.unlock()

    #     # checks if the result is a 0 length string: error
    #     if not self.get_locked_chars():
    #         self.error("Got a 0 length string")

    #     token = self.create_new_token(TokenType.STRING)
    #     self.recorder.unlock()

    #     return token

    def __repr__(self):
        return "Lexer[common={}, indents={}, handle_newline={}]".format(super().__repr__(), self.indents, self.handle_newline)

if __name__ == "__main__":
    # import timeit

    with open("test_lexer.txt") as file:
        text = file.read()

    # number = 20
    # print(timeit.timeit("lexer = Lexer(text); lexer.test()", number=number, globals=globals()))
    lexer = Lexer(text)

    for token in lexer:
        logging.debug(repr(token))

    # token = True
    # while token:
    #     token = next(lexer, None)
    #     logging.debug(repr(token))

