import logging
import os
import sys

if __name__ == "__main__":
    sys.path.append("..")

# from fenalib.command_builder import CommandBuilder_1_12, CommandBuilder_1_13
from fenalib.command_builder import CommandBuilder_1_12
from fenalib.config_data import ConfigData
from fenalib.lexer import Lexer
from fenalib.parser import Parser

config_data = ConfigData()
full_dir_path = os.path.realpath("functions/fena")

# global variable (oh no) that determines whether output should be printed or not

def test_builder(string, lexer_method, parser_method, expected=None, expect_error=False, print_ast=False):
    # if config_data.version == "1.12":
    #     CommandBuilder = CommandBuilder_1_12
    # elif config_data.version == "1.13":
    #     CommandBuilder = CommandBuilder_1_13
    # else:
    #     raise RuntimeError
    CommandBuilder = CommandBuilder_1_12

    try:
        lexer = Lexer(string)
        parser = Parser(lexer, method_name=lexer_method)
        ast = parser.parse(method_name=parser_method)
        command_builder = CommandBuilder(ast, full_dir_path)
        output = command_builder.interpret()

        if expected is None:
            expected = string

    except Exception as e:
        # simply outputs the result of the error
        if expect_error:
            logging.debug(f"input={string!r}, output={e!r}")

        else:
            # otherwise, unexpected error
            logging.error(f"input={string!r}, output={e!r} as UNEXPECTED ERROR")

            # uses traceback from previous exception as found in:
            # https://docs.python.org/3/library/exceptions.html#BaseException
            tb = sys.exc_info()[2]
            raise e.with_traceback(tb)
    else:
        logging.debug(f"input={string!r}, output={output!r}")

        if print_ast:
            logging.debug(ast)

        if expect_error:
            raise RuntimeError(f"""
            Input:    {string!r}
            Expected: 'ERROR'
            Output:   {output!r}
            AST:      {ast!r}""")

        if expected != output:
            raise RuntimeError(f"""
            Input:    {string!r}
            Expected: {expected!r}
            Output:   {output!r}
            AST:      {ast!r}""")


def test_lexer(text, expected_token_types=(), expect_error=False):
    """
    Args:
        text (str)
        expected_token_types (iterable): if empty tuple, won't check for expected tokens
    """
    try:
        lexer = Lexer(text)
        received_tokens = []
        for token in lexer:
            logging.debug(token)
            received_tokens.append(token)

    except Exception as e:
        if not expect_error:
            logging.error(f"input={text!r}, output={e!r} as UNEXPECTED ERROR")
            tb = sys.exc_info()[2]
            raise e.with_traceback(tb)
    else:
        if expect_error:
            raise RuntimeError(f"""
            Input:    {text!r}
            Expected: 'ERROR'""")

        if expected_token_types:
            for index, token in enumerate(received_tokens):
                if not token.matches(expected_token_types[index]):
                    raise RuntimeError(f"""
                    Input:    {text!r}
                    Expected: {expected_token_types[index]!r}
                    Output:   {token!r}""")


def test_selector(selector, expected=None, **kwargs):
    test_builder(selector, "get_selector", "selector", expected=expected, **kwargs)

def test_json(json, expected=None, **kwargs):
    test_builder(json, "get_curly_bracket_tag", "json", expected=expected, **kwargs)

def test_nbt(nbt, expected=None, **kwargs):
    test_builder(nbt, "get_curly_bracket_tag", "nbt", expected=expected, **kwargs)

def test_cmd(cmd, expected=None, **kwargs):
    test_builder(cmd, "get_command", "command", expected=expected, **kwargs)

def test_block(block, expected=None, **kwargs):
    test_builder(block, "get_command", "block", expected=expected, **kwargs)

def test_coord(coord, expected=None, **kwargs):
    test_builder(coord, "get_until_space", "coord", expected=expected, **kwargs)

def test_vec2(vec2, expected=None, **kwargs):
    test_builder(vec2, "get_command", "vec2", expected=expected, **kwargs)

def test_vec3(vec3, expected=None, **kwargs):
    test_builder(vec3, "get_command", "vec3", expected=expected, **kwargs)

def test_data_path(vec3, expected=None, **kwargs):
    test_builder(vec3, "get_command", "data_path", expected=expected, **kwargs)
