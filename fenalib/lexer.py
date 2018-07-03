import logging

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

    import fenalib.logging_setup as logging_setup
    logging_setup.setup_logging()

from fenalib.assert_utils import assert_type
from fenalib.repr_utils import addrepr
from fenalib.token_classes import TypedToken, DelimiterToken, WhitespaceToken, TokenValues
from fenalib.config_data import ConfigData
from fenalib.lexical_token import Token
from fenalib.token_position import TokenPosition, TokenPositionRecorder

@addrepr
class Lexer:
    """
    Args:
        text (str)

    Attributes:
        text (str)
        recorder (TokenPositionRecorder)
        reached_eof (bool)
        indents (int)
    """
    config_data = ConfigData()

    def __init__(self, text):
        self.text = text
        self.recorder = TokenPositionRecorder()
        self.reached_eof = False

        # list of indent strings
        # 1 indent is either 4 spaces or 1 tab space
        self.indents = 0

        # bool returns true if it is a zero length string or complete whitespace
        if not self.text.strip():
            raise EOFError("File does not contain anything")

    def __iter__(self):
        """
        Breaks apart the entire document into a sequence of tokens.

        Yields:
            Token: For each token that exists in the document
        """
        yield from self.handle_line_begin()

        # does not require "else" since if it is a selector, it should end in the block above
        while not self.reached_eof:
            # skips all whitespace until \n
            if self.get_char().isspace() and not self.current_chars_are(WhitespaceToken.NEWLINE.value):
                self.skip_whitespace()
                continue

            # handles indents and dedents after newline
            elif self.current_chars_are(WhitespaceToken.NEWLINE.value):
                yield from self.handle_newline()

            else:
                yield from self.get_command()

        # at the end of file by this point, and it must end with dedent tokens if a newline did not end
        while self.indents > 0:
            yield self.get_dedent()

        # gets one last EOF token
        yield self.create_new_token(WhitespaceToken.EOF)

    def advance(self, increment=1):
        """
        Advances the position

        Args:
            increment (int): Number of chars that will be incremented
        """
        assert_type(increment, int)

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

    def error(self, message=None, expected=None):
        """
        Args:
            class_name (str): Name of the class that will implement this
            message (str or None): Message to be displayed with the error.
                Defaults to None, which will display a generic message containing the current character
        """
        # message and expected cannot both be used
        if message is None:
            char = self.get_char()
            if expected is None:
                message = f"Invalid character {char!r}"
            else:
                message = f"Expected {expected!r} but got {char!r}"
        raise TypeError(f"Lexer{self.recorder}: {message}")
        # raise TypeError(f"{self!r}: {message}")

    def invalid_method(self, *args, **kwargs):
        raise NotImplementedError(f"Lexer{self.recorder}: Invalid method")

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
        assert_type(chars, str)
        self.advance(len(chars))

    def get_char(self):
        """
        Args:
            length (int, optional) number of characters from the current position

        Returns:
            int: current characters from the current position given the length
        """
        if self.reached_eof:
            self.error("Cannot get a character when the end of file has been reached")

        char_pos = self.recorder.char_pos
        return self.text[char_pos]

    def get_chars(self, length):
        """
        Args:
            length (int) number of characters from the current position

        Returns:
            str: current characters from the current position given the length
        """
        if self.reached_eof:
            self.error("Cannot get a character when the end of file has been reached")

        assert_type(length, int)
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
        assert_type(chars, str)
        length = len(chars)
        return chars == self.get_chars(length)

    def create_new_token(self, token_type, value=None, position=None, advance=False, unlock=False):
        """
        Creates a new token and automatically fills out the token fields unless specified

        If the current state of the position is locked, it gets the locked chars instead

        Args:
            token_type (any TokenType)
            value (any, defaults to None): What value the token should have
            position (TokenPosition, defaults to None): The position of the current token
            advance (bool, defaults to False): Whether to advance after creating the token or not
            unlock (bool, defaults to False): Whethre to unlock after creating the token or not
        """
        if position is None:
            position = self.recorder.position
        assert_type(position, TokenPosition)

        if self.recorder.locked:
            value = self.get_locked_chars()

        token = Token(position, token_type, value)

        if unlock:
            self.recorder.unlock()

        if advance:
            self.advance_chars(token.value)

        return token

    def skip_comment(self):
        while not self.reached_eof and not self.current_chars_are(WhitespaceToken.NEWLINE.value):
            self.advance()

    def get_indent(self):
        """
        Gets a singular indent token and adds one from the indent length

        Returns:
            Token: Indent token
        """
        self.indents += 1
        return self.create_new_token(WhitespaceToken.INDENT)

    def get_dedent(self):
        """
        Gets a singular dedent token and subtracts one from the indent length

        Returns:
            Token: Dedent token
        """
        self.indents -= 1
        return self.create_new_token(WhitespaceToken.DEDENT)

    def handle_newline(self):
        """
        Handles the combination of a newline and the beginning of the next line

        Yields:
            Token: Newline token and all tokens gotten from handling a beginning of a line
        """
        # gets one newline token whenever called unless it is at the beginning of the line
        yield self.create_new_token(WhitespaceToken.NEWLINE)
        self.advance()

        yield from self.handle_line_begin()

    def handle_line_begin(self):
        """
        Handles all tokens gotten at the beginning of a line

        It creates the given number of indent or dedent tokens depending on the indents found.

        Yields:
            Token: Indent and dedent tokens, and statement tokens
        """
        # gets any whitespace past the newline
        self.recorder.lock()
        self.skip_whitespace()
        whitespace = self.get_locked_chars()
        self.recorder.unlock()

        if self.reached_eof:
            return

        # if the current char is a comment after whitespace, it is still an empty line
        if self.get_char() in (WhitespaceToken.NEWLINE.value, WhitespaceToken.COMMENT.value):
            if self.current_chars_are(WhitespaceToken.COMMENT.value):
                self.skip_comment()
            return

        # otherwise, the whitespace is valid for interpretation for indents and dedents
        # checks whether the indenting whitespace is actually valid (4 spaces)
        # boolean value of any integer is False if 0, True for anything else
        if len(whitespace) % len(WhitespaceToken.INDENT.value):
            self.error(f"Invalid whitespace: {whitespace!r} (requires indentation of 4 spaces)")

        # gets the number of indents at the current area
        current_indents = whitespace.count(WhitespaceToken.INDENT.value)

        if current_indents > self.indents:
            if current_indents-1 == self.indents:
                yield self.get_indent()

            else:
                indent_num = current_indents - self.indents
                self.error(f"Too many indents (Expected one, got {indent_num}")

        # gets all possible dedent tokens
        while current_indents < self.indents:
            yield self.get_dedent()

        # all possible dedent and indent tokens have been gotten by this point
        # however, there are certain things that can only happen after a valid newline (statements)
        if self.current_chars_are(DelimiterToken.EXCLAMATION_MARK.value):
            yield from self.get_statement()

    def get_statement(self):
        """
        Gets all proper statement tokens, starting from "!" and ending at the next "\n"
            This expects the first value to be "!", and the second value to be a statement keyword

        Yields:
            Token: All statement tokens (statement specifier, statement keyword, strings after keywords)
        """
        yield self.create_new_token(DelimiterToken.EXCLAMATION_MARK, advance=True)
        self.skip_whitespace()

        # assumes the rest are strings until newline
        while not self.reached_eof and self.get_char() != "\n":
            if self.get_char().isspace():
                self.skip_whitespace()
                continue

            if self.current_chars_are(DelimiterToken.QUOTE.value):
                yield self.get_literal_string()
            elif self.get_char() in TokenValues.get(DelimiterToken):
                yield self.create_new_token(DelimiterToken(self.get_char()), advance=True)
            else:
                yield self.get_until_space(exempt_chars=TokenValues.get(DelimiterToken))

    def get_until_space(self, exempt_chars=""):
        """
        Gets the string and stops when it is a whitespace character or the current
        character is within the exempt chars
        """
        if self.get_char() in exempt_chars:
            self.error(f"Cannot get a string because the string starts with {self.get_char()!r}, but cannot be within {exempt_chars}")
        if self.get_char().isspace():
            self.error(f"Cannot get a string because the string starts a whitespace {self.get_char()!r}")
        if self.reached_eof:
            self.error("Cannot get a string because the end of the file has been reached")

        self.recorder.lock()
        while not self.reached_eof and not self.get_char().isspace() and not self.get_char() in exempt_chars:
            self.advance()

        # checks if the result is a 0 length string: error
        assert self.get_locked_chars(), "Cannot be a 0 length string bruh wtf is this"
        return self.create_new_token(TypedToken.STRING, unlock=True)

    def get_command(self):
        """
        Gets all command related tokens

        Yields:
            Token: Delimiter, NBT, Selector, String tokens
        """
        while not self.reached_eof and not self.current_chars_are(WhitespaceToken.NEWLINE.value):
            if self.get_char().isspace():
                self.skip_whitespace()
                continue

            if self.current_chars_are(DelimiterToken.AT.value):
                yield from self.get_selector()

            elif self.current_chars_are(DelimiterToken.OPEN_CURLY_BRACKET.value):
                yield from self.get_curly_bracket_tag()

            elif self.current_chars_are(DelimiterToken.OPEN_SQUARE_BRACKET.value):
                yield from self.get_block_states()

            # elif self.current_chars_are(DelimiterToken.QUOTE.value):
            #     yield self.get_literal_string()

            elif self.get_chars(2) in TokenValues.get(DelimiterToken):
                yield self.create_new_token(DelimiterToken(self.get_chars(2)), advance=True)
            elif self.get_char() in TokenValues.get(DelimiterToken) - {"="}:
                yield self.create_new_token(DelimiterToken(self.get_char()), advance=True)

            else:
                yield self.get_until_space(exempt_chars=TokenValues.get(DelimiterToken) - {"="})

    def get_selector(self):
        """
        Gets all selector tokens (handles selector variables and brackets)

        Yields:
            Token: Selector tokens (Selector variables and all selector arguments)
        """
        # checks for valid selector var as a, e, r, s, p (or whatever is specified in the config)
        yield self.create_new_token(DelimiterToken.AT, advance=True)

        if self.get_char() not in Lexer.config_data.selector_variable_specifiers:
            self.error(f"Invalid selector variable: '@{self.get_char()}'")

        yield self.create_new_token(TypedToken.SELECTOR_VARIABLE_SPECIFIER, value=self.get_char(), advance=True)

        # starts getting the tokens inside square brackets including the square brackets
        if not self.reached_eof and self.current_chars_are(DelimiterToken.OPEN_SQUARE_BRACKET.value):
            yield self.create_new_token(DelimiterToken.OPEN_SQUARE_BRACKET, advance=True)
            yield from self.get_selector_arguments()
            yield self.create_new_token(DelimiterToken.CLOSE_SQUARE_BRACKET, advance=True)

    def get_selector_arguments(self):
        """
        Gets all selector arguments inside the square brackets []
        """
        while not self.current_chars_are(DelimiterToken.CLOSE_SQUARE_BRACKET.value):
            if self.get_char().isspace() and self.get_char() != WhitespaceToken.NEWLINE.value:
                self.skip_whitespace()
                continue

            elif self.current_chars_are(DelimiterToken.OPEN_CURLY_BRACKET.value):
                yield from self.get_curly_bracket_tag()

            elif self.current_chars_are('"'):
                yield self.get_literal_string()
            elif self.get_char().isdigit() or self.get_char() == "-":
                yield self.get_number()

            # Gets simple delimiter tokens
            elif self.get_char() in TokenValues.get(DelimiterToken):
                yield self.create_new_token(DelimiterToken(self.get_char()), advance=True)
            elif self.get_chars(2) in TokenValues.get(DelimiterToken):
                yield self.create_new_token(DelimiterToken(self.get_chars(2)), advance=True)

            elif self.current_chars_are("*"):
                yield self.create_new_token(TypedToken.STRING, value=self.get_char(), advance=True)

            # otherwise, general string
            elif self.get_char().isalpha() or self.get_char() in "_.":
                yield self.get_until_space(exempt_chars=TokenValues.get(DelimiterToken))

            else:
                self.error()

    def get_literal_string(self, allow_newline=False):
        """
        Returns:
            Token: Literal string with quotes enclosing it
        """
        self.recorder.lock()

        # advances the first "
        if not self.current_chars_are(DelimiterToken.QUOTE.value):
            self.error(expected=DelimiterToken.QUOTE.value)
        self.advance()

        while not self.current_chars_are(DelimiterToken.QUOTE.value):
            # Skips past any \" or \\ since it doesn't count as a string end
            if self.current_chars_are(r'\"') or self.current_chars_are(r'\\'):
                self.advance(2)

            # There shouldn't ever be a newline in a string
            elif self.current_chars_are(WhitespaceToken.NEWLINE.value) and not allow_newline:
                self.error("Unexpected newline during a string declaration")

            # Advances normally
            else:
                self.advance()

        # advances the last "
        self.advance()

        return self.create_new_token(TypedToken.LITERAL_STRING, unlock=True)

    def get_number(self):
        """
        Gets a number token as either an integer or float token
        Format: ("-")? & (INT)+ & ("." & (INT)+)?

        Returns:
            Token: integer or float token with TypedToken.INT or TypedToken.FLOAT
        """
        is_float = False

        self.recorder.lock()
        if self.get_char() == "-":
            self.advance()

        while self.get_char().isdigit():
            self.advance()

        # float type, assuming it is not ".." which indicates a range
        # a range will be separated into its individual tokens (number, range delimiter, number)
        if self.get_char() == "." and self.get_chars(2) != "..":
            is_float = True
            self.advance()
            while self.get_char().isdigit():
                self.advance()

        # exponential value, meaning that the type of float will now be TypedToken.EXPONENTIAL_FLOAT
        if self.get_char().lower() == "e":
            is_float = True
            self.advance()

            # allows either + or - after e or E
            if self.get_char().lower() in ("+", "-"):
                self.advance()

            # requires at least one digit
            if not self.get_char().isdigit():
                self.error(f"Got {self.get_char()!r} but expected a digit after an exponential 'e' or 'E' for a float")
            while self.get_char().isdigit():
                self.advance()

        token_type = TypedToken.FLOAT if is_float else TypedToken.INT
        return self.create_new_token(token_type, unlock=True)

    def get_curly_bracket_tag(self, array=False):
        """
        Get all relevant nbt tag or json tokens

        This also checks for proper encapsulation of {} and []
        """
        # gets the beginning bracket token
        if array:
            begin_type = DelimiterToken.OPEN_SQUARE_BRACKET
            end_type = DelimiterToken.CLOSE_SQUARE_BRACKET
        else:
            begin_type = DelimiterToken.OPEN_CURLY_BRACKET
            end_type = DelimiterToken.CLOSE_CURLY_BRACKET

        if not self.current_chars_are(begin_type.value):
            self.error(expected=begin_type.value)
        yield self.create_new_token(begin_type, advance=True)

        while not self.current_chars_are(end_type.value):
            if self.get_char().isspace() and self.get_char() != WhitespaceToken.NEWLINE.value:
                self.skip_whitespace()
                continue

            # skips comments inside nbt tags
            if self.current_chars_are(WhitespaceToken.NEWLINE.value):
                self.advance()
                self.skip_whitespace()
                if self.current_chars_are(WhitespaceToken.COMMENT.value):
                    self.skip_comment()
                continue

            elif self.get_char() in (DelimiterToken.COLON.value, DelimiterToken.COMMA.value, DelimiterToken.SEMICOLON.value):
                yield self.create_new_token(DelimiterToken(self.get_char()), advance=True)

            elif self.current_chars_are(DelimiterToken.OPEN_CURLY_BRACKET.value):
                # recursive call to get nbt in {}
                yield from self.get_curly_bracket_tag()

            elif self.current_chars_are(DelimiterToken.OPEN_SQUARE_BRACKET.value):
                # recursive call to get nbt in []
                yield from self.get_curly_bracket_tag(array=True)

            elif self.get_char() == DelimiterToken.QUOTE.value:
                yield self.get_literal_string(allow_newline=True)
            elif self.get_char().isdigit() or self.get_char() == "-":
                yield self.get_number()
            elif self.get_char().isalpha() or self.get_char() in "_.":
                yield self.get_until_space(exempt_chars=TokenValues.get(DelimiterToken))
            else:
                self.error(f"Invalid character {self.get_char()!r} inside tag")

        # gets the ending bracket token
        yield self.create_new_token(end_type, advance=True)

    def get_block_states(self):
        """
        Gets the minimal amount of tokens required for a block states area
        """
        yield self.create_new_token(DelimiterToken.OPEN_SQUARE_BRACKET, advance=True)

        while not self.current_chars_are(DelimiterToken.CLOSE_SQUARE_BRACKET.value):
            if self.get_char().isspace() and self.get_char() != WhitespaceToken.NEWLINE.value:
                self.skip_whitespace()
                continue

            if self.get_char().isalpha() or self.get_char() == "*":
                yield self.get_until_space(exempt_chars=TokenValues.get(DelimiterToken))
            elif self.get_char().isdigit() or self.get_char() == "-":
                yield self.get_number()
            elif self.get_char() in (DelimiterToken.COMMA.value, DelimiterToken.EQUALS.value):
                yield self.create_new_token(DelimiterToken(self.get_char()), advance=True)
            else:
                self.error(f"Invalid character {self.get_char()!r} inside block states")

        yield self.create_new_token(DelimiterToken.CLOSE_SQUARE_BRACKET, advance=True)

if __name__ == "__main__":
    # import timeit

    with open("log/after_pre_pyexpander.txt") as file:
        text = file.read()

    lexer = Lexer(text)

    for token in lexer:
        logging.debug(repr(token))

    print(repr(lexer))

    # gets only selector tokens
    # lexer = Lexer("@e[x=5,y=4,z=2, type=armor_stand,_entity, _pl=(5..6), {CustomNameVisible:1b}]")
    # for token in lexer.get_selector():
    #     logging.debug(repr(token))

    # lexer = Lexer(r'{"test":1 "test":2}')
    # for token in lexer.get_curly_bracket_tag():
    #     print(repr(token))
    #     logging.debug(repr(token))

    # lexer = Lexer("_pl")
    # print(lexer.get_until_space())
    # lexer = Lexer("@s _ti += players _ti2")
    # lexer = Lexer("setblock _ti <= players _ti2")
    # lexer = Lexer("stonebrick[variant=mossy_stonebrick]")
    # for token in lexer.get_command():
    #     print(repr(token))

