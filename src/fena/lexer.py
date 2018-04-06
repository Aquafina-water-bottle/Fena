import logging

from token_types import TokenType, SimpleToken, WhitespaceToken, StatementToken, ALL_TYPES
from config_data import ConfigData
from lexical_token import Token
from token_position import TokenPosition, TokenPositionRecorder


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

    def create_new_token(self, token_type, value=None):
        token_pos = self.position.create_instance()
        return Token(token_pos, token_type, value)

    def get_next_token(self):
        """
        This method is responsible for breaking a sentence
        apart into tokens, one token at a time.
        """
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

            # # gets selector
            # if self.get_chars(2) in options[SELECTOR_TYPES]:
            #     return self.get_selector()

            # # gets datatag
            # if self.current_chars_are("{"):
            #     return self.get_data_tag()

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

    # def handle_after_newline(self):
    #     if self.current_chars_are("#"):
    #         self.skip_comment()
    #         return

    #     if self.current_chars_are(STATEMENT[VALUE]):
    #         statementToken = Token(self.getTokenPos(), STATEMENT)
    #         self.storedTokens.put(statementToken)

    #         # advances after '!"
    #         self.advance()
    #         self.get_post_stmts()
    #         return

    # def get_statements(self):
    #     """
    #     Gets any statements with the first character being "!"

    #     Returns:
    #         StatementToken
    #     """

    #     stmt_str = self.get_string()
    #     if stmt_str in StatementToken:
    #         token_type = StatementToken(stmt_str)
    #         return self.create_new_token(token_type)

    #     if self.current_chars_are():
    #         # creates new PATH token
    #         self.storedTokens.put(Token(self.getTokenPos(), PATH))
    #         self.advance(PATH[VALUE])

    #     elif self.current_chars_are(MFUNC[VALUE]):
    #         # creates new MFUNC token
    #         self.storedTokens.put(Token(self.getTokenPos(), MFUNC))
    #         self.advance(MFUNC[VALUE])

    #     else:
    #         self.error()

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
                # skips the newline and indents
                self.advance()
                self.skip_whitespace()
                return self.get_indent()

            else:
                self.advance()
                self.error("Too many indents")

        if current_indents < self.indents:
            # doesn't actually advance here in case of multiple dedents
            self.position.lock()
            self.advance()
            dedent_token = self.get_dedent()
            self.position.unlock(undo_progress=True)

            return dedent_token

        # guaranteed to be current_indents == self.indents
        # meaning that no dedent and indent tokens will be made, so all will be skipped
        self.advance()
        self.returned_newline = False
        self.skip_whitespace()

    def handle_indents(self):
        """
        handle existing indents, dedents and new lines

        note that this is called when the current character is "\n"
        """
        pass

        # # newline tokens cannot be put in the beginning because there must be
        # # a string detected for a newline to register
        # # self.storedTokens.put(newlineToken)
        # self.advance()

        # # note that index is indents-1 to 0
        # for index in reversed(range(self.indents)):
        #     if self.current_chars_are(INDENT[VALUE]):
        #         self.advance(INDENT[VALUE])
        #     else:
        #         # dedents are detected here due to lack of indents
        #         # however, if the current token is literally a newline or comment, does nothing and immediately breaks
        #         # this will go back to the beginning of this method, creating a newline token there
        #         if self.current_chars_are("\n"):
        #             return

        #         if self.current_chars_are("#"):
        #             self.skip_comment()
        #             return

        #         dedents = index+1
        #         self.get_dedents(dedents)

        #         # adds the newline token here because newline tokens should come after dedent tokens
        #         newlineToken = Token(self.getTokenPos(), NEWLINE)
        #         self.storedTokens.put(newlineToken)
        #         self.handle_after_newline()
        #         return

        # # if the immediate next character is just a newline, ends
        # # this is for when there are no indents avaliable to go to the above
        # if self.current_chars_are("\n"):
        #     return

        # # handle new indents
        # newlineToken = Token(self.getTokenPos(), NEWLINE)
        # self.storedTokens.put(newlineToken)
        # if self.current_chars_are(INDENT[VALUE]):
        #     self.indents += 1

        #     indentToken = Token(self.getTokenPos(), INDENT)
        #     self.storedTokens.put(indentToken)
        #     self.advance(INDENT[VALUE])

        # # if there is additional whitespace after an indent, error
        # if self.current_chars_are(INDENT[VALUE]):
        #     self.error("Invalid indent")

        # # handles newline after indent because indent character will take up its place if not
        # self.handle_after_newline()

    # def get_number(self):
    #     """Return a (multidigit) integer or float consumed from the input."""
    #     self.lock()

    #     if not self.reached_eof and (self.current_chars_are("-") or self.get_char().isdigit):
    #         self.advance()

    #     while not self.reached_eof and self.get_char().isdigit():
    #         self.advance()

    #     if self.current_chars_are("."):  # indicates it's a float value
    #         self.advance()

    #         while not self.reached_eof and self.get_char().isdigit():
    #             self.advance()

    #         result = self.get_locked_chars()
    #         token = Token(self.getTokenPos(), FLOAT, float(result))
    #     else:
    #         result = self.get_locked_chars()
    #         token = Token(self.getTokenPos(), INT, int(result))

    #     # there has to be whitespace after the token for it to be truly a number
    #     # otherwise, it's a string
    #     if not self.get_char().isspace():
    #         trueTokenPos = self.getTokenPos()
    #         self.unlock()
    #         additional = self.get_string().value
    #         return Token(trueTokenPos, STRING, result + additional)
    #     self.unlock()
    #     return token

    # def get_coord(self):
    #     """
    #     gets the coordinate token, as either "~" or "~[number]",
    #     where number can be an int or float

    #     :return:
    #     """

    #     self.lock()
    #     self.advance()

    #     if (not self.reached_eof) and (self.current_chars_are("-") or self.get_char().isdigit()):
    #         self.advance()

    #     while not self.reached_eof and self.get_char().isdigit():
    #         self.advance()

    #     if self.current_chars_are("."):  # indicates it's a float value
    #         self.advance()

    #         while not self.reached_eof and self.get_char().isdigit():
    #             self.advance()

    #         result = self.get_locked_chars()
    #     else:
    #         result = self.get_locked_chars()

    #     token = Token(self.getTokenPos(), COORD, result)
    #     self.unlock()
    #     return token

    # def get_data_tag(self):
    #     """
    #     self.brackets represents how many closing brackets are required to escape this method

    #     initially starts at one because it requires one closing bracket to close
    #     note it doesn't account for any strings with curly brackets, so gl with that

    #     :return:
    #     """
    #     brackets = 0

    #     self.lock()
    #     tokenPos = self.getTokenPos()

    #     # result here to skip unnecessary whitespace and comments
    #     result = ""

    #     while not self.reached_eof:
    #         # handles whitespace right after newline and comments within datatags
    #         if self.current_chars_are(NEWLINE[VALUE]):
    #             # adds to result, unlocks, advances (skip whitespace and comment), relocks
    #             result += self.get_locked_chars()
    #             self.unlock()
    #             self.advance()

    #             if self.get_char().isspace():
    #                 self.skip_whitespace()

    #             self.handle_after_newline()
    #             self.lock()
    #             continue

    #         if self.current_chars_are("{"):
    #             brackets += 1
    #         if self.current_chars_are("}"):
    #             brackets -= 1
    #         if brackets == 0:
    #             self.advance()
    #             break

    #         self.advance()

    #     result += self.get_locked_chars()

    #     token = Token(tokenPos, DATATAG, result)
    #     self.unlock()
    #     return token

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

    def get_string(self):
        """
        Simply gets the current string until next whitespace

        Returns:
            str: concatenation of the current chars until the next whitespace
        """
        self.position.lock()
        while not self.reached_eof and not self.get_char().isspace():
            self.advance()

        result = self.get_locked_chars()
        self.position.unlock()

        return self.create_new_token(TokenType.STRING, result)

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
            print(repr(token))

if __name__ == "__main__":
    with open("test_lexer.txt") as file:
        text = file.read()
    lexer = Lexer(text)
    lexer.handle_newline(beginning_line=True)
    lexer.test()
