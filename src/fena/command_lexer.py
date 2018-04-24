from common_lexer import CommonLexer
from token_types import SimpleToken, SIMPLE_TOKEN_VALUES, SelectorSimpleToken, NBTSimpleToken

class CommandLexer(CommonLexer):
    def __init__(self, lexer):
        """
        Args:
            text (str): full text file
            position (PositionRecorder)
        """
        # super().__init__(__class__.__name__, text=command.value, initial_pos=command.pos)
        super().from_lexer(__class__.__name__, lexer)
        self.reached_execute_end = False

    def __iter__(self):
        while not self.reached_eof:
            if self.get_char().isspace() and self.get_char() != "\n":
                self.skip_whitespace()
                continue

            # gets : , ( ) as delimiter tokens
            if self.current_chars_are(SIMPLE_TOKEN_VALUES):
                token = self.create_new_token(SimpleToken(self.get_char()), advance=True)
            elif self.get_char() == SelectorSimpleToken.BEGIN.value:
                token = self.get_selector()
            elif self.get_char() == NBTSimpleToken.BEGIN.value:
                token = self.get_data_tag()
            else:
                token = self.get_string()

            yield token

    def skip_quotes(self):
        r"""
        Used when inside datatags and selectors

        Skips the following:
            "{\"text\":\"asdf\"}"
        """
        pass

    def skip_enclosed_brackets(self):
        r"""
        Skips the following: (only when skipping quotes)
            "\{"text":"\"asdf\""\}" --> "{\"text\":\"\\\"asdf\\\"\"}"
        """
        pass

    def get_selector(self):
        pass

    def get_data_tag(self):
        pass

    def get_string(self):
        pass
        
    def __repr__(self):
        pass

if __name__ == "__main__":
    pass
    # from lexical_token import Token
    # from token_position import TokenPosition
    # from token_types import TokenType

    # def test(command):
    #     position = TokenPosition(row=5, column=3, char_pos=0)
    #     cmd_token = Token(position, TokenType.COMMAND, value=command)
    #     lexer = CommandLexer(cmd_token)

    #     for token in lexer:
    #         print(repr(token))
    #     print()

    # test("@a[_ti=1] _ti = 0")
    # test(r'tellraw @a[some_tag] {"text":"{\"text\":\"asdf\"}"}')
