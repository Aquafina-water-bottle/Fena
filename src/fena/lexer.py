if __name__ == "__main__":
    import logging_setup

import logging
import json

from token_classes import WhitespaceSimpleToken, StatementSimpleToken, NBTSimpleToken, SimpleToken, SelectorSimpleToken, NBTSimpleToken, NBTNumberEndSimpleToken
from token_classes import TypedToken, SelectorTypedToken, TokenValues

from config_data import ConfigData
from lexical_token import Token
from token_position import TokenPosition, TokenPositionRecorder

class Lexer:
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
        This method is responsible for breaking a sentence
        apart into tokens, one token at a time.
        """
        yield from self.handle_line_begin()

        # does not require "else" since if it is a selector, it should end in the block above
        while not self.reached_eof:
            # skips all whitespace until \n
            if self.get_char().isspace() and not self.current_chars_are(WhitespaceSimpleToken.NEWLINE.value):
                self.skip_whitespace()

            # handles indents and dedents after newline
            elif self.current_chars_are(WhitespaceSimpleToken.NEWLINE.value):
                yield from self.handle_newline()

            else:
                yield from self.get_command()

        # at the end of file by this point, and it must end with dedent tokens if a newline did not end
        if self.indents > 0:
            yield self.get_dedent()

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
            if self.current_chars_are(WhitespaceSimpleToken.NEWLINE.value):
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
        raise TypeError("Lexer{pos}: {message}".format(pos=self.recorder, message=message))

    def skip_whitespace(self, skip_newline=False):
        """
        Skips all whitespace that isn't a newline
        """
        if skip_newline:
            while not self.reached_eof and self.get_char().isspace():
                self.advance()
        else:
            while not self.reached_eof and self.get_char().isspace() and not self.current_chars_are(WhitespaceSimpleToken.NEWLINE.value):
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

    def skip_comment(self):
        while not self.reached_eof and not self.current_chars_are(WhitespaceSimpleToken.NEWLINE.value):
            self.advance()

    def get_indent(self):
        """
        Gets a singular indent token and adds one from the indent length

        Returns:
            Token: Indent token
        """
        self.indents += 1
        return self.create_new_token(WhitespaceSimpleToken.INDENT)

    def get_dedent(self):
        """
        Gets a singular dedent token and subtracts one from the indent length

        Returns:
            Token: Dedent token
        """
        self.indents -= 1
        return self.create_new_token(WhitespaceSimpleToken.DEDENT)

    def handle_newline(self):
        """
        Handles the combination of a newline and the beginning of the next line

        Yields:
            Token: Newline token and all tokens gotten from handling a beginning of a line
        """
        # gets one newline token whenever called unless it is at the beginning of the line
        yield self.create_new_token(WhitespaceSimpleToken.NEWLINE)
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

        # if the current char is a comment after whitespace, it is still an empty line
        if self.get_char() in (WhitespaceSimpleToken.NEWLINE.value, WhitespaceSimpleToken.COMMENT.value):
            if self.current_chars_are(WhitespaceSimpleToken.COMMENT.value):
                self.skip_comment()
            return

        # otherwise, the whitespace is valid for interpretation for indents and dedents
        # checks whether the indenting whitespace is actually valid (4 spaces)
        # boolean value of any integer is False if 0, True for anything else
        if len(whitespace) % len(WhitespaceSimpleToken.INDENT.value):
            self.error("Invalid whitespace: {} (requires indentation of 4 spaces)".format(repr(whitespace)))

        # gets the number of indents at the current area
        current_indents = whitespace.count(WhitespaceSimpleToken.INDENT.value)

        if current_indents > self.indents:
            if current_indents-1 == self.indents:
                yield self.get_indent()

            else:
                self.error("Too many indents (Expected one, got {}".format(current_indents - self.indents))

        # gets all possible dedent tokens
        while current_indents < self.indents:
            yield self.get_dedent()

        # all possible dedent and indent tokens have been gotten by this point
        # however, there are certain things that can only happen after a valid newline (statements)
        if self.current_chars_are(StatementSimpleToken.STATEMENT_SPECIFIER.value):
            yield from self.get_statement()

    def get_statement(self):
        """
        Gets all proper statement tokens, starting from "!" and ending at the next "\n"
            This expects the first value to be "!", and the second value to be a statement keyword

        Yields:
            Token: All statement tokens (statement specifier, statement keyword, strings after keywords)
        """
        yield self.create_new_token(StatementSimpleToken.STATEMENT_SPECIFIER, advance=True)
        self.skip_whitespace()

        keyword_token = self.get_until_space()
        if keyword_token.value not in TokenValues.get(StatementSimpleToken):
            self.error("Statement keyword {} does not exist".format(repr(keyword_token.value)))

        keyword_token.cast(StatementSimpleToken)
        yield keyword_token
        self.skip_whitespace()

        # assumes the rest are strings until newline
        while not self.reached_eof and self.get_char() != "\n":
            if self.get_char().isspace():
                self.skip_whitespace()

            yield self.get_until_space()

    def get_until_space(self, exempt_chars=""):
        """
        Gets the string and stops when it is a whitespace character or the current
        character is within the exempt chars
        """
        if self.get_char() in exempt_chars:
            self.error("Cannot get a string because the string starts with {}, but cannot be within {}".format(
                repr(self.get_char()), repr(exempt_chars)))
        if self.get_char().isspace():
            self.error("Cannot get a string because the string starts a whitespace {}".format(repr(self.get_char())))
        if self.reached_eof:
            self.error("Cannot get a string because the end of the file has been reached")

        self.recorder.lock()
        while not self.reached_eof and not self.get_char().isspace() and not self.get_char() in exempt_chars:
            self.advance()

        # checks if the result is a 0 length string: error
        assert self.get_locked_chars()
        return self.create_new_token(TypedToken.STRING, unlock=True)

    def get_command(self):
        """
        Gets all command related tokens

        Yields:
            Token: Delimiter, NBT, Selector, String tokens
        """
        while not self.reached_eof and not self.current_chars_are(WhitespaceSimpleToken.NEWLINE.value):
            if self.get_char() in TokenValues.get(SimpleToken):
                yield self.create_new_token(SimpleToken(self.get_char()), advance=True)

            elif self.current_chars_are(SelectorSimpleToken.BEGIN.value):
                yield from self.get_selector()

            elif self.current_chars_are(NBTSimpleToken.BEGIN.value):
                yield from self.get_tag()
                
            else:
                yield self.get_until_space(",:()")

            self.skip_whitespace()

    def get_selector(self):
        """
        Gets all selector tokens (handles selector variables and brackets)

        Yields:
            Token: Selector tokens (Selector variables and all selector arguments)
        """
        # checks for valid selector var as @a, @e, @r, @s, @p (or whatever is specified in the config)
        if self.get_chars(2) not in Lexer.config_data.selector_variables:
            self.error("Invalid selector variable: {}".format(repr(self.get_chars(2))))

        yield self.create_new_token(SelectorTypedToken.SELECTOR_VARIABLE, value=self.get_chars(2), advance=True)

        # starts getting the tokens inside square brackets including the square brackets
        if self.current_chars_are(SelectorSimpleToken.OPEN_BRACKET.value):
            yield self.create_new_token(SelectorSimpleToken.OPEN_BRACKET, advance=True)
            yield from self.get_selector_arguments()
            yield self.create_new_token(SelectorSimpleToken.CLOSE_BRACKET, advance=True)

    def get_selector_arguments(self):
        """
        Gets all selector arguments inside the square brackets []
        """
        while not self.current_chars_are(SelectorSimpleToken.CLOSE_BRACKET.value):
            if self.get_char().isspace():
                self.skip_whitespace()

            elif self.current_chars_are(NBTSimpleToken.BEGIN.value):
                yield from self.get_tag()

            # Gets simple delimiter tokens
            elif self.get_char() in "=!,()":
                yield self.create_new_token(SelectorSimpleToken(self.get_char()), advance=True)
            elif self.current_chars_are(".."):
                yield self.create_new_token(SelectorSimpleToken(self.get_chars(2)), advance=True)

            elif self.current_chars_are('"'):
                yield self.get_literal_string()
            elif self.get_char().isdigit() or self.get_char() == "-":
                yield self.get_number()
            elif self.get_char().isalpha() or self.get_char() in "_.":
                yield self.get_until_space(exempt_chars=r"!=.,()[]{}")
            else:
                self.error()

    def get_literal_string(self):
        """
        Returns:
            Token: Literal string with quotes enclosing it
        """

        # advances the first "
        self.recorder.lock()
        self.advance()

        while not self.current_chars_are(SimpleToken.QUOTE.value):
            # Skips past any \" since it doesn't count as a string end
            if self.current_chars_are(r'\"'):
                self.advance(2)

            # There shouldn't ever be a newline in a string
            elif self.current_chars_are(WhitespaceSimpleToken.NEWLINE.value):
                self.error()

            # Advances normally
            else:
                self.advance()

        # advances the last "
        self.advance()

        return self.create_new_token(TypedToken.LITERAL_STRING, unlock=True)

    def get_number(self, int_type=TypedToken.INT, float_type=TypedToken.FLOAT):
        """
        Gets a number token as either an integer or float token
        Format: ("-")? & (INT)+ & ("." & (INT)+)?

        Args:
            int_type: Type of the token if the number is an integer
            float_type: Type of the token if the number is a float

        Returns:
            Token: Integer or Float token with the provided type
        """
        self.recorder.lock()
        if self.get_char() == "-":
            self.advance()

        while self.get_char().isdigit():
            self.advance()
        if self.get_char() == "." and self.get_chars(2) != "..":  # float
            while self.get_char().isdigit():
                self.advance()

            return self.create_new_token(float_type, value=float(self.get_locked_chars()), unlock=True)
        return self.create_new_token(int_type, value=int(self.get_locked_chars()), unlock=True)

    def get_tag(self):
        """
        Yields:
            Token: NBT tag tokens or JSON tokens
        """
        if self.current_chars_are('{"'):
            yield self.get_json()
        else:
            yield from self.get_nbt()

    def get_json(self):
        """
        WTF PYTHON IS SO CONVIENENT
        """
        decoder = json.JSONDecoder()
        json_object, position = decoder.raw_decode(self.text[self.recorder.char_pos:])
        self.advance(position)
        return self.create_new_token(TypedToken.JSON, value=json_object)

    def get_nbt(self, nbt_array=False):
        """
        Get all relevant nbt tokens
        """
        # gets the beginning bracket token
        if nbt_array:
            begin_type = NBTSimpleToken.BEGIN_ARRAY
            end_type = NBTSimpleToken.END_ARRAY
        else:
            begin_type = NBTSimpleToken.BEGIN
            end_type = NBTSimpleToken.END

        yield self.create_new_token(begin_type, advance=True)

        while not self.current_chars_are(end_type.value):
            if self.get_char().isspace() and self.get_char() != WhitespaceSimpleToken.NEWLINE.value:
                self.skip_whitespace()

            # skips comments inside nbt tags
            if self.current_chars_are(WhitespaceSimpleToken.NEWLINE.value):
                self.advance()
                self.skip_whitespace()
                if self.current_chars_are(WhitespaceSimpleToken.COMMENT.value):
                    self.skip_comment()

            elif self.get_char() in (NBTSimpleToken.COLON.value, NBTSimpleToken.COMMA.value):
                yield self.create_new_token(NBTSimpleToken(self.get_char()), advance=True)

            elif self.current_chars_are(NBTSimpleToken.BEGIN.value):
                # recursive call to get nbt in {}
                yield from self.get_nbt()

            elif self.current_chars_are(NBTSimpleToken.BEGIN_ARRAY.value):
                # recursive call to get nbt in []
                yield from self.get_nbt(nbt_array=True)

            elif self.get_char() == SimpleToken.QUOTE.value:
                yield self.get_literal_string()
            elif self.get_char().isdigit() or self.get_char() == "-":
                yield self.get_number()
                # sees if the number has a type by seeing if there is a letter after a number
                if self.get_char().isalpha():
                    if self.get_char() in TokenValues.get(NBTNumberEndSimpleToken):
                        yield self.create_new_token(NBTNumberEndSimpleToken(self.get_char()), advance=True)
                    else:
                        self.error("Unknown alphabetical value ending")
            elif self.get_char().isalpha():
                yield self.get_until_space(exempt_chars=r",:[]{}")
            else:
                self.error()

        # gets the ending bracket token
        yield self.create_new_token(end_type, advance=True)

    def __repr__(self):
        return "Lexer[text={}, recorder={}, indents={}, reached_eof={}]".format(repr(self.text), repr(self.recorder), self.indents, self.reached_eof)

if __name__ == "__main__":
    # import timeit

    with open("test_lexer.txt") as file:
        text = file.read()

    # number = 20
    # print(timeit.timeit("lexer = Lexer(text); lexer.test()", number=number, globals=globals()))
    lexer = Lexer(text)

    for token in lexer:
        logging.debug(repr(token))

    # gets only selector tokens
    lexer = Lexer("@e[x=5,y=4,z=2, type=armor_stand,_Entity, _pl=(5..6), {CustomNameVisible:1b}]")
    for token in lexer.get_selector():
        logging.debug(repr(token))

