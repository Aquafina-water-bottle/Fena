if __name__ == "__main__":
    import logging_setup

import os
import logging

from token_types import TokenType, SimpleToken, WhitespaceToken, StatementToken, SelectorTokenType, SelectorSimpleToken, ExecuteShortToken
from token_types import ALL_TOKENS, STATEMENT_TOKEN_VALUES, EXECUTE_SHORTCUT_TOKEN_VALUES
from mcfunction import McFunctionBuilder
from command_builder import CommandBuilder
from scoped_symbol_table import ScopedSymbolTable
from corountine import coroutine

"""
Organizes all lines into their respective mcfunctions

program ::= (NEWLINE)* & (statement)* & (NEWLINE)*

statement ::= "!" && [folder_stmt, mfunc_stmt, prefix_stmt, constobj_stmt]
folder_stmt ::= "folder" && STR && (NEWLINE)* & INDENT && suite && DEDENT
mfunc_stmt ::= "mfunc" && STR && (NEWLINE)* & INDENT && suite && DEDENT
prefix_stmt ::= "prefix" && STR
constobj_stmt ::= "constobj" && STR

suite ::= [statement, command, NEWLINE]+
command ::= (execute_cmd && ":")? && [scoreboard_cmd, function_cmd, simple_cmd]

execute_cmd ::= selector && (vec3)? && exec_if && (execute_cmd)?
exec_if ::= "if" && "(" && (exec_if_args)+ && ")"
exec_if_args ::= block && (vec3)? && ("," && exec_if_args)?

scoreboard_cmd ::= [scoreboard_players_math, scoreboard_players_special, scoreboard_players_op, scoreboard_teams, scoreboard_tags]
scoreboard_players_math ::= [SELECTOR, STR] && STR && ["+", "-", "="] && INT && (NBT)?
scoreboard_players_special ::= [SELECTOR, STR] && ["enable", "reset", "get"] && STR
scoreboard_players_op ::= [SELECTOR, STR] && STR && ["=", "+", "-", "*", "/", "%"] && ((STR) | (SELECTOR) | 
scoreboard_teams ::= ("join" && STR && [SELECTOR, STR]+) | ("leave" && [SELECTOR, STR]+) | ("empty" && STR)
scoreboard_tags ::= [SELECTOR, STR] && ("+", "-") && STR

function_cmd ::= "function" && STR
simple_cmd ::= COMMAND_KEYWORD && (STR)*

vec3 ::= coord && coord && coord
coord ::= ("^", "~")? & ("-")? & [INT, FLOAT]
"""

class Parser:
    """
    Makes the mcfunction builders while building all datatags and selectors

    Attributes:
        lexer (Lexer)
        symbol_table (ScopedSymbolTable): Stores all symbols acquired dealing with statements and statement scopes
        file_path (str): Main output file path of the mcfunctions
        mcfunctions (list): All mcfunction builders made by the parser
    """

    def __init__(self, lexer, file_path):
        self.iterator = iter(lexer)
        self.current_token = None
        self.advance()

        self.symbol_table = ScopedSymbolTable()
        self.file_path = file_path
        self.mcfunctions = []

    def parse(self):
        logging.debug("Original symbol table: {}".format(repr(self.symbol_table)))
        self.program()
        logging.debug("Final symbol table: {}".format(repr(self.symbol_table)))
        logging.debug("")

    def error(self, message=None):
        if message is None:
            message = "Invalid syntax"
        raise SyntaxError("{}: {}".format(self.current_token, message))

    def advance(self):
        """
        Gets the next token from the lexer without checking any type
        """
        self.current_token = next(self.iterator, None)
        logging.debug("Advanced to {}".format(repr(self.current_token)))

    def eat(self, token_type, value=None, error_message=None):
        """
        Advances given the token type and values match up with the current token

        Args:
            token_type (any token type)
            value (any, defaults to None)
        """

        if (value is None or self.current_token.value == value) and self.current_token.matches(token_type):
            token = self.current_token
            self.advance()
            return token

        if error_message is None:
            error_message = "Expected {}".format(token_type)
        self.error(error_message)

    def build_functions(self):
        """
        Builds all mcfunctions

        Returns:
            list: All built mcfunctions
        """
        logging.debug("Begin building")
        CommandBuilder.initialize(self.symbol_table, self.mcfunctions)
        built_mcfunctions = []

        for mcfunction in self.mcfunctions:
            built_mcfunctions.append(mcfunction.build())
        logging.debug("End building")

        return built_mcfunctions

    def program(self):
        """
        program ::= (statement)*
        """
        logging.debug("Begin program at {}".format(repr(self.current_token)))

        while self.current_token is not None and self.current_token.matches_any_of(WhitespaceToken.NEWLINE, SimpleToken.STATEMENT_SPECIFIER):
            # skips all newlines
            if self.current_token.matches(WhitespaceToken.NEWLINE):
                self.eat(WhitespaceToken.NEWLINE)

            # otherwise, gets statement
            elif self.current_token.matches(SimpleToken.STATEMENT_SPECIFIER):
                self.statement()

            elif self.current_token is not None:
                self.error("Unexpected default case")

        logging.debug("End program at {}".format(repr(self.current_token)))

    def statement(self):
        """
        Handles any post-processor statements

        statement ::= "!" && [folder_stmt, mfunc_stmt, prefix_stmt, constobj_stmt]
        """
        # all here should start with "!"
        self.eat(SimpleToken.STATEMENT_SPECIFIER)

        if self.current_token.matches(StatementToken.MFUNC):
            self.mfunc_stmt()
        elif self.current_token.matches(StatementToken.FOLDER):
            self.folder_stmt()
        elif self.current_token.matches(StatementToken.PREFIX):
            self.prefix_stmt()
        elif self.current_token.matches(StatementToken.CONSTOBJ):
            self.constobj_stmt()
        else:
            self.error("Invalid statement")

    def mfunc_stmt(self):
        """
        mfunc_stmt ::= "mfunc" && STR && (NEWLINE)* & INDENT && suite && DEDENT
        """
        self.eat(StatementToken.MFUNC)

        if self.symbol_table.function is not None:
            self.error("Cannot define a mcfunction inside an mcfunction")

        mfunc_token = self.eat(TokenType.STRING, error_message="Expected a string after a mfunc statement")

        name = mfunc_token.value + ".mcfunction"
        if self.symbol_table.folders is None:
            full_path = os.path.join(self.file_path, name)
        else:
            full_path = os.path.join(self.file_path, self.symbol_table.folders, name)

        # new scoped symbol table for the mcfunction stmt
        self.symbol_table = ScopedSymbolTable(enclosing_scope=self.symbol_table)
        self.symbol_table.function = McFunctionBuilder(full_path)

        # skips any and all newlines right after a mfunc statement
        while self.current_token.matches(WhitespaceToken.NEWLINE):
            self.eat(WhitespaceToken.NEWLINE)

        self.eat(WhitespaceToken.INDENT)
        self.suite()
        self.eat(WhitespaceToken.DEDENT)

        # resets the current function
        self.mcfunctions.append(self.symbol_table.function)
        self.symbol_table = self.symbol_table.enclosing_scope

    def prefix_stmt(self):
        """
        prefix_stmt ::= "prefix" && STR
        """
        self.eat(StatementToken.PREFIX)

        # requires the prefix to be defined in the global scope
        if not self.symbol_table.is_global:
            self.error("Cannot define a prefix when the scope is not global")

        prefix_token = self.eat(TokenType.STRING, error_message="Expected a string after a prefix statement")

        self.symbol_table.prefix = prefix_token.value

    def constobj_stmt(self):
        """
        constobj_stmt ::= "constobj" && STR
        """
        self.eat(StatementToken.CONSTOBJ)

        constobj_token = self.eat(TokenType.STRING, error_message="Expected a string after a prefix statement")

        if not self.symbol_table.is_global:
            self.error("The constobj cannot be set outside the global context")

        if self.symbol_table.constobj is not None:
            self.error("The constobj cannot be set twice")

        self.symbol_table.constobj = constobj_token.value

    def folder_stmt(self):
        """
        folder_stmt ::= "folder" && STR && (NEWLINE)* & INDENT && suite && DEDENT
        """
        self.eat(StatementToken.FOLDER)

        # requires there to be no current mcfunction since a folder statement
        # always occurs outside a mfunc statement
        if self.symbol_table.function is not None:
            self.error("Cannot parse a folder statement inside an mcfunction")

        # sets the current folder
        self.symbol_table = ScopedSymbolTable(enclosing_scope=self.symbol_table)
        folder_token = self.eat(TokenType.STRING)
        self.symbol_table.add_folder(folder_token.value)

        # skips any and all newlines right after a folder statement
        while self.current_token.matches(WhitespaceToken.NEWLINE):
            self.eat(WhitespaceToken.NEWLINE)

        self.eat(WhitespaceToken.INDENT)
        self.suite()
        self.eat(WhitespaceToken.DEDENT)

        # resets the current folder
        self.symbol_table = self.symbol_table.enclosing_scope

    def suite(self):
        """
        suite ::= [statement, command]*
        """
        logging.debug("Begin compound at {}".format(repr(self.current_token)))
        logging.debug("with scoped symbol table = {}".format(repr(self.symbol_table)))

        # note that this is essentially a do-while since it never starts out as a newline
        while self.current_token.matches_any_of(
                WhitespaceToken.NEWLINE, StatementToken.STATEMENT_SPECIFIER, TokenType.STRING, SelectorTokenType.TARGET_SELECTOR_VARIABLE):
            # base case is if a newline is not met
            if self.current_token.matches(WhitespaceToken.NEWLINE):
                self.eat(WhitespaceToken.NEWLINE)

            elif self.current_token.matches(StatementToken.STATEMENT_SPECIFIER):
                self.statement()

            elif self.current_token.matches_any_of(TokenType.STRING, SelectorTokenType.TARGET_SELECTOR_VARIABLE):
                self.command()

            else:
                self.error("Expected a newline, command or statement specifier")

        logging.debug("End compound at {}".format(repr(self.current_token)))

    def get_command_builder(self):
        """
        Creates a new scope for a command builder to work out things

        Coroutine:
            Gets all tokens until a colon or newline is reached

        Returns:
            CommandBuilder: The full command in a command builder
            bool: Whether the last token before the line was a colon or not
                This signifies a command chain
        """
        self.symbol_table = ScopedSymbolTable(enclosing_scope=self.symbol_table)
        command_builder = self.symbol_table.command_builder
        
        while not self.current_token.matches(WhitespaceToken.NEWLINE):
            if self.current_token.matches(SelectorTokenType.TARGET_SELECTOR_VARIABLE):
                selector = self.get_selector()
                command_builder.execute.add(selector, execute_type="as")

            elif self.current_token.value in EXECUTE_SHORTCUT_TOKEN_VALUES:
                command_builder.execute.state = self.current_token.value
                self.eat("dank memes lololololllo")
                self.current_token.cast(ExecuteShortToken)
            # elif token
            else:
                self.current_token.cast(TokenType.COORD)

            if self.current_token.matches(WhitespaceToken.NEWLINE):
                break

        self.symbol_table = self.symbol_table.enclosing_scope
        return command_builder

    def command(self):
        """
        command ::= (STR)+ && (":" & (NEWLINE)* & INDENT && command_suite && DEDENT)?

        Returns:
            str: The full built command
        """
        # checks whether the command can actually be added to an mcfunction or not
        if self.symbol_table.function is None:
            self.error("No assigned mcfunction for command")

        # command = self.eat(TokenType.COMMAND)
        # command_builder = CommandBuilder()
        # while not self.current_token.matches(WhitespaceToken.NEWLINE):
        #     if self.current_token.matches(SelectorTokenType.TARGET_SELECTOR_VARIABLE):
        #         selector = self.selector(build=True)

        command_builder = self.get_command_builder()

        # checks whether a command suite can be used by seeing if the last token of a command is a colon
        # the reason why it has a colon is because a colon is valid in the middle of a command when used as an execute shortcut
        # if self.current_token.matches(SimpleToken.COLON):
        #     self.symbol_table = ScopedSymbolTable(enclosing_scope=self.symbol_table)
        #     self.symbol_table.command_builder = command_builder

        #     # skips any and all newlines
        #     while self.current_token.matches(WhitespaceToken.NEWLINE):
        #         self.eat(WhitespaceToken.NEWLINE)

        #     self.eat(WhitespaceToken.INDENT)
        #     self.command_suite()
        #     self.eat(WhitespaceToken.DEDENT)

        #     self.symbol_table = self.symbol_table.enclosing_scope

        # else:
        #     command.value = self.symbol_table.command_slices + command.value
        #     self.symbol_table.function.add_command(command)

    def selector(self):
        """
        Returns:
            SelectorBuilder: if the build option is false
            Token: with TokenType.SELECTOR if the build option is true
        """
        pass

    def get_selector(self, build=False):
        pass

    def _get_selector(self):
        pass
    
    def __repr__(self):
        return "Parser[iterator={}, current_token={}, symbol_table={}, file_path={}, mcfunctions={}]".format(
            repr(self.iterator), repr(self.current_token), self.symbol_table, self.file_path, self.mcfunctions)

if __name__ == "__main__":
    from lexer import Lexer

    logging_setup.format_file_name("test_lexer.txt")

    with open("test_lexer.txt") as file:
        text = file.read()
    lexer = Lexer(text)

    parser = Parser(lexer, r"C:\Users\Austin-zs\AppData\Roaming\.minecraft\saves\Snapshot 17w18b\data\functions\ego\event_name")

    try:
        parser.parse()
    except Exception as e:
        logging.exception(e)

    mcfunctions = parser.mcfunctions
    for mcfunction in mcfunctions:
        logging.debug("")
        logging.debug(str(mcfunction))
        for command in mcfunction.commands:
            logging.debug(repr(command))
