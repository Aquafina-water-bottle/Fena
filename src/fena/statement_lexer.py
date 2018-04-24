from token_types import StatementToken, SimpleToken, TokenType, WhitespaceToken, STATEMENT_TOKEN_VALUES
from common_lexer import CommonLexer
from token_position import TokenPosition

class StatementLexer(CommonLexer):
    """
    Args:
        token_num (int): What token position the lexer is currently at
    """
    def __init__(self):
        super().__init__(__class__.__name__, text=None)
        self.token_num = 0
        self.reached_eof = True

    def reset(self, text, position):
        self.recorder.position = position
        self.recorder.char_pos = 0
        self.text = text
        self.token_num = 0
        self.reached_eof = False

    def __iter__(self):
        """
        Gets the token "!", StatementToken, string tokens

        Returns:
            Token
        """
        while not self.reached_eof:
            if self.get_char().isspace() and self.get_char() != "\n":
                self.skip_whitespace()
                continue

            if self.token_num == 0:
                if self.get_char() == "!":
                    token = self.create_new_token(SimpleToken.STATEMENT_SPECIFIER, advance=True)
                else:
                    self.error()

            elif self.token_num == 1:
                token = self.get_string()
                if token.value in STATEMENT_TOKEN_VALUES:
                    token.cast(StatementToken)
                else:
                    self.error("Invalid Statement")

            else:
                token = self.get_string()

            self.token_num += 1
            yield token

    def get_string(self):
        """
        Simply gets the current string until next whitespace

        Returns:
            Token: String token containing the string between two whitespaces
        """
        self.recorder.lock()

        # otherwise, it just stops when it is a whitespace character or it isn't a special delimiter character
        while not self.reached_eof and not self.get_char().isspace() and self.get_char() != "\n":
            self.advance()

        # checks if the result is a 0 length string: error
        if not self.get_locked_chars():
            self.error("Got a 0 length string")

        return self.create_new_token(TokenType.STRING, unlock=True)

    def __repr__(self):
        return "StatementLexer[common={}, token_num={}]".format(super().__repr__(), self.token_num)

if __name__ == "__main__":
    statement_lexer = StatementLexer()
    position = TokenPosition(row=1, column=1, char_pos=0)

    def test(text):
        statement_lexer.reset(text, position)
        for token in statement_lexer:
            print(repr(token))
        # while not statement_lexer.reached_eof:
        #     print(repr(statement_lexer))
        #     print(repr(statement_lexer.get_next_token()))

    test("!mfunc ayylmao")
    test("!folder ayylmao")
    test("!prefix ayylmao")
    test("!constobj ayylmao")
    # test("!lolol ayylmao")

