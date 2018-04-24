if __name__ == "__main__":
    import logging_setup

import os
import logging

from token_types import TokenType, SimpleToken, WhitespaceToken, StatementToken, ALL_TOKENS, STATEMENT_TOKEN_VALUES
from mcfunction import McFunctionBuilder
from command_builder import CommandBuilder
from scoped_symbol_table import ScopedSymbolTable
from common_parser import CommonParser

"""
Organizes all lines into their respective mcfunctions

program ::= (NEWLINE)* & (statement)* & (NEWLINE)*

statement ::= "!" && [folder_stmt, mfunc_stmt, prefix_stmt, constobj_stmt]
folder_stmt ::= "folder" && STR && (NEWLINE)* & INDENT && suite && DEDENT
mfunc_stmt ::= "mfunc" && STR && (NEWLINE)* & INDENT && suite && DEDENT
prefix_stmt ::= "prefix" && STR
constobj_stmt ::= "constobj" && STR
suite ::= [statement, command, NEWLINE]+
command ::= (STR)+ && (":" & (NEWLINE)* & INDENT && command_suite && DEDENT)?
command_suite ::= [command, NEWLINE]+

leading_cmd ::= [execute_cmd, (LEADING_START && (STR)*)]
execute_cmd ::= ("execute"? && selector && coords?) && (["detect", "ifblock"] && coords? && block && [INT, STR]?)?

ending_cmd ::= [players_cmd, teams_cmd, tag_cmd, regular_cmd]
players_cmd ::= [players_math_cmd, players_test_cmd, players_obj_cmd]
players_math_cmd ::= selector && STR && ["+", "-", "="] && INT && (DATATAG)?
players_test_cmd ::= selector && STR && ["?"] && INT && (INT)?
players_obj_cmd ::= selector && ["reset", "enable"] && STR

teams_cmd ::= [team_join_cmd, team_leave_cmd, team_empty_cmd]
team_join_cmd ::= "join" && STR && selector
team_leave_cmd ::= "leave" && selector
team_empty_cmd ::= "empty" && STR

tag_cmd ::= selector && ["+", "-"] && STR && (DATATAG)?

regular_cmd ::= REGULAR_START && [selector, STR]*
"""

class Parser(CommonParser):
    def __init__(self, lexer, file_path):
        super().__init__(__class__.__name__, lexer)

        # requires an mcfunction to be set for commands to be used
        # and an mcfunction cannot be set if one has already been set
        self.symbol_table = ScopedSymbolTable()
        self.file_path = file_path

        # list of all mcfunctions avaliable
        self.mcfunctions = []

    def parse(self):
        logging.debug("Original symbol table: {}".format(repr(self.symbol_table)))
        self.program()
        logging.debug("Final symbol table: {}".format(repr(self.symbol_table)))
        logging.debug("")
        logging.debug("Begin building")

        # builds all mcfunctions
        CommandBuilder.initialize(self.symbol_table, self.mcfunctions)
        # built_mcfunctions = []
        # for mcfunction in self.mcfunctions:
        #     built_mcfunctions.append(mcfunction.build())

        # self.mcfunctions = built_mcfunctions
        logging.debug("End building")

    def advance(self):
        super().advance()
        logging.debug("Advanced to {}".format(repr(self.current_token)))

    def program(self):
        """
        program ::= (statement)*
        """
        logging.debug("Begin program at {}".format(repr(self.current_token)))

        while self.current_token is not None and self.current_token.matches_any_of(WhitespaceToken.NEWLINE, SimpleToken.STATEMENT_SPECIFIER):
            # skips all newlines
            if self.current_token.matches(WhitespaceToken.NEWLINE):
                self.eat(WhitespaceToken.NEWLINE)
                continue

            # otherwise, suite
            self.statement()

        logging.debug("End program at {}".format(repr(self.current_token)))

    def suite(self, commands_only=False):
        """
        suite ::= [statement, command]*
        """
        logging.debug("Begin compound at {}".format(repr(self.current_token)))
        logging.debug("with scoped symbol table = {}".format(repr(self.symbol_table)))

        # note that this is essentially a do-while since it never starts out as a newline
        met_newline = True
        while met_newline:
            if not commands_only and self.current_token.matches(SimpleToken.STATEMENT_SPECIFIER):
                # does a continue since the statement might be a compound and not end in a newline
                self.statement()
                continue

            elif self.current_token.matches_any_of(TokenType.COMMAND):
                self.command()
                continue

            # base case is if a newline is not met
            met_newline = self.current_token.matches(WhitespaceToken.NEWLINE)
            if met_newline:
                self.eat(WhitespaceToken.NEWLINE)

        logging.debug("End compound at {}".format(repr(self.current_token)))

    def command_suite(self):
        """
        command_suite ::= [command, NEWLINE]+
        """
        self.suite(commands_only=True)

    def statement(self):
        """
        Handles any post-processor statements

        statement ::= "!" && [folder_stmt, mfunc_stmt]
        """
        # all here should start with "!"
        self.eat(SimpleToken.STATEMENT_SPECIFIER)

        if self.current_token.value in STATEMENT_TOKEN_VALUES:
            self.current_token.cast(StatementToken)

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

        if not self.current_token.matches(TokenType.STRING):
            self.error("Expected a string after a mfunc statement")

        name = self.current_token.value + ".mcfunction"
        if self.symbol_table.folders is not None:
            full_path = os.path.join(self.file_path, self.symbol_table.folders, name)
        else:
            full_path = os.path.join(self.file_path, name)

        # new scoped symbol table for the mcfunction stmt
        self.symbol_table = ScopedSymbolTable(enclosing_scope=self.symbol_table)
        self.symbol_table.function = McFunctionBuilder(full_path)

        # guaranteed string token here
        self.advance()

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

        # requires a string as the prefix
        if not self.current_token.matches(TokenType.STRING):
            self.error("Expected a string after a prefix statement")

        # requires the prefix to be defined in the global scope
        if not self.symbol_table.is_global:
            self.error("Cannot define a prefix when the scope is not global")

        self.symbol_table.prefix = self.current_token.value
        self.advance()

    def constobj_stmt(self):
        """
        constobj_stmt ::= "constobj" && STR
        """
        self.eat(StatementToken.CONSTOBJ)

        # requires a string as the initials
        if not self.current_token.matches(TokenType.STRING):
            self.error()

        if not self.symbol_table.is_global:
            self.error("The constobj cannot be set outside the global context")

        if self.symbol_table.constobj is not None:
            self.error("The constobj cannot be set twice")

        self.symbol_table.constobj = self.current_token.value
        self.advance()

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
        folder = self.current_token.value
        self.symbol_table.add_folder(folder)
        self.eat(TokenType.STRING)

        # skips any and all newlines right after a folder statement
        while self.current_token.matches(WhitespaceToken.NEWLINE):
            self.eat(WhitespaceToken.NEWLINE)

        self.eat(WhitespaceToken.INDENT)
        self.suite()
        self.eat(WhitespaceToken.DEDENT)

        # resets the current folder
        self.symbol_table = self.symbol_table.enclosing_scope

    def command(self):
        """
        command ::= (STR)+ && (":" & (NEWLINE)* & INDENT && command_suite && DEDENT)?
        """
        # checks whether the command can actually be added to an mcfunction or not
        if self.symbol_table.function is None:
            self.error("No assigned mcfunction for command")

        # command = self.current_token.value
        # print(command)
        command = self.eat(TokenType.COMMAND)

        # checks whether a command suite can be used by seeing if the last token of a command is a colon
        # the reason why it has a colon is because a colon is valid in the middle of a command when used as an execute shortcut
        if command.value[-1] == ":":
            self.symbol_table = ScopedSymbolTable(enclosing_scope=self.symbol_table)
            self.symbol_table.add_command_slice(command)

            # skips any and all newlines
            while self.current_token.matches(WhitespaceToken.NEWLINE):
                self.eat(WhitespaceToken.NEWLINE)

            self.eat(WhitespaceToken.INDENT)
            self.command_suite()
            self.eat(WhitespaceToken.DEDENT)

            self.symbol_table = self.symbol_table.enclosing_scope

        else:
            command.value = self.symbol_table.command_slices + command.value
            self.symbol_table.function.add_command(command)
    
    def __repr__(self):
        return "Parser[common={}, symbol_table={}, file_path={}, mcfunctions={}]".format(
            super().__repr__(), self.symbol_table, self.file_path, self.mcfunctions)

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
