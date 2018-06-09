import logging

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fena.command_builder import CommandBuilder_1_12, CommandBuilder_1_13
from fena.config_data import ConfigData
from fena.lexer import Lexer
from fena.parser import Parser

config_data = ConfigData()

# global variable (oh no) that determines whether output should be printed or not

def test_builder(string, lexer_method, parser_method, expected=None, expect_error=False, print_ast=False):
    if config_data.version == "1.12":
        CommandBuilder = CommandBuilder_1_12
    elif config_data.version == "1.13":
        CommandBuilder = CommandBuilder_1_13
    else:
        raise RuntimeError

    try:
        lexer = Lexer(string)
        parser = Parser(lexer, method_name=lexer_method)
        ast = parser.parse(method_name=parser_method)
        command_builder = CommandBuilder(ast)
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
            import sys
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
            Output:   {output!r}""")

def test_selector(selector, expected=None, **kwargs):
    test_builder(selector, "get_selector", "selector", expected=expected, **kwargs)

def test_json(json, expected=None, **kwargs):
    test_builder(json, "get_curly_bracket_tag", "json", expected=expected, **kwargs)

def test_nbt(nbt, expected=None, **kwargs):
    test_builder(nbt, "get_curly_bracket_tag", "nbt", expected=expected, **kwargs)