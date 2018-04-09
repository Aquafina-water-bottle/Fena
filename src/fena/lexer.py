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

        # this is here because the first statement has to be handled
        # self.handle_after_newline()

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
            advance (bool, defaults to False): Whether when creating the token, it should advance or not
        """
        if position is None:
            position = self.position.create_instance()

        if self.position.locked:
            value = self.get_locked_chars()

        token = Token(position, token_type, value)

        if advance:
            self.advance_chars(token.value)

        return token

    def get_next_token(self, for_selector=False):
        """
        This method is responsible for breaking a sentence
        apart into tokens, one token at a time.
        """

        if for_selector:
            if self.get_chars(2) in self.config_data.target_selector_variables:
                return self.create_new_token(SelectorTokenType.TARGET_SELECTOR_VARIABLE, self.get_chars(2), advance=True)

            if self.get_char() in SELECTOR_SIMPLE_TOKENS_VALUES:
                return self.create_new_token(SelectorSimpleToken(self.get_char()), advance=True)
            if self.get_chars(2) in SELECTOR_SIMPLE_TOKENS_VALUES:
                return self.create_new_token(SelectorSimpleToken(self.get_chars(2)), advance=True)

            if self.get_char().isalpha() or self.get_char().isdigit() or self.get_char() in "-_":
                return self.get_string(for_selector=True)

            if self.current_chars_are(SimpleToken.COLON.value):
                # does not advance since it should stop here
                return self.create_new_token(SimpleToken.COLON)

            if self.get_char().isspace():
                return self.create_new_token(SelectorSimpleToken.END, advance=True)

            self.error("Invalid character for a selector: {}".format(repr(self.get_char())))

        # does not require "else" since if it is a selector, it should end in the block above
        while not self.reached_eof:
            # line break when "\" is found at the end of a line lol
            # note that pyexpander does this already, so this is temporarily removed
            # if self.current_chars_are("\\\n"):
            #     self.advance(2)
            #     self.skip_whitespace()
            #     continue

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

            # # gets a number if the first character is a digit or negative digit
            # # it gets the first 2 current chars, and gets the second current char to see if it's a digit
            # if self.get_char().isdigit() or (self.current_chars_are("-") and self.get_chars(2)[1].isdigit()):
            #     return self.get_number()

            # # gets coordinate
            # if self.current_chars_are("~"):
            #     return self.get_coord()

            # gets selector
            if self.current_chars_are("@"):
                return self.get_selector()

            # gets a singular colon token
            if self.current_chars_are(SimpleToken.COLON.value):
                return self.create_new_token(SimpleToken.COLON, advance=True)

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
        current_token = None
        selector_tokens = []
        while current_token is None or not current_token.matches_any_of(SelectorSimpleToken.END, SimpleToken.COLON):
            if current_token is not None:
                selector_tokens.append(current_token)
            current_token = self.get_next_token(for_selector=True)

        return self.create_new_token(TokenType.SELECTOR, value=Selector(selector_tokens))
            
    # def selector_eat(self, chars):
    #     """
    #     Advances the character if the characters match, used only for selectors
    #     """
    #     if not self.current_chars_are(chars):
    #         self.error("Expected {} but got {}".format(chars, self.get_chars(len(chars))))

    # def get_selector(self):
    #     """
    #     selector ::= DEFAULT_VAR & ("[" & selector_args & "]")?

    #     selector_args ::= (selector_single_arg)? | (selector_single_arg & ("," & selector_single_arg)*)?
    #     selector_single_arg ::= [selector_simple_arg, selector_range_arg, selector_tag_arg]
    #     selector_simple_arg ::= DEFAULT_ARG & "=" & ("!")? & [STRING, INT]

    #     selector_tag_arg ::= ("!")? & STRING
    #     selector_range_arg ::= STRING & ("=" & selector_range)?
    #     selector_range ::= [INTEGER, (INTEGER & ".."), (".." & INTEGER), (INTEGER & ".." & INTEGER)]

    #     Gets a full selector and splits the selector up into its component parts

    #     Returns:
    #         Token: with TokenType.SELECTOR and a Selector value
    #     """

    #     # checks whether the first characters are inside the target selector variables
    #     selector_var = self.get_chars(2)
    #     if selector_var not in self.config_data.target_selector_variables:
    #         self.error("'{}' is not {}".format(selector_var, self.config_data.target_selector_variables))

    #     # gets the starting position and advances past the selector variable
    #     starting_pos = self.position.create_instance()
    #     selector_var = self.create_new_token(SelectorTokenType.TARGET_SELECTOR_VARIABLE, selector_var)
    #     selector = Selector(selector_var)
    #     self.advance(2)

    #     # checks whether the selector actually has arguments
    #     # by seeing if the next character is a space or just "[]"
    #     if not (self.get_char().isspace() or self.get_chars(2) == "[]"):
    #         # this allows target selector arguments to be added
    #         self.selector_eat("[")
    #         self.selector_args(selector)
    #         self.selector_eat("]")

    #     ending_pos = self.position.create_instance()
    #     selector_pos = TokenPosition.from_positions(starting_pos, ending_pos)
    #     return self.create_new_token(TokenType.SELECTOR, value=selector, position=selector_pos)

    # def selector_args(self, selector):
    #     """
    #     selector_args ::= (selector_single_arg)? | (selector_single_arg & ("," & selector_single_arg)*)?
    #     """
    #     while not self.current_chars_are("]"):
    #         self.selector_single_arg(selector)
    #         if not self.current_chars_are("]"):
    #             self.selector_eat(",")

    # def selector_single_arg(self, selector):
    #     """
    #     selector_single_arg ::= [selector_simple_arg, selector_range_arg, selector_tag_arg]
    #     """
    #     # negated tag
    #     if self.current_chars_are("!"):
    #         tag_token = self.get_string(for_selector=True)
    #         selector.add_tag(tag_token)


    # def get_selector(self):
    #     """
    #     Gets the entire selector

    #     Returns:
    #         Token: selector token
    #     """
    #     self.lock()

    #     # because all beginning selectors are 2 characters, @x
    #     self.advance()
    #     self.advance()

    #     if self.current_chars_are("["):
    #         while not self.reached_eof and not self.current_chars_are("]"):
    #             self.advance()
    #         self.advance()  # to advance after "["

    #     result = self.get_locked_chars()
    #     token = Token(self.getTokenPos(), SELECTOR, result)
    #     self.unlock()

    #     return token

    def get_string(self, for_selector=False):
        """
        Simply gets the current string until next whitespace

        Returns:
            str: concatenation of the current chars until the next whitespace
        """
        self.position.lock()

        current_char = self.get_char()
        # if the token creation is for the selector, it only advances when it is in the alphabet, a number or "_"
        # otherwise, it just stops when it is a whitespace character
        while not self.reached_eof and (
            (for_selector and (current_char.isalpha() or current_char.isdigit() or current_char in "-_")) or (not for_selector and not current_char.isspace() and not current_char == ":")):
            self.advance()
            current_char = self.get_char()

        # result = self.get_locked_chars()
        # self.position.unlock()

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
            token = self.get_next_token()
            logging.debug(repr(token))

if __name__ == "__main__":
    with open("test_lexer.txt") as file:
        text = file.read()
    lexer = Lexer(text)
    lexer.test()
