if __name__ == "__main__":
    import logging_setup

import os
import logging

from token_types import TokenType, SimpleToken, WhitespaceToken, StatementToken, ALL_TOKENS, STATEMENT_TOKEN_VALUES
from mcfunction import McFunction
from commands import Command, SimpleCommand, ExecuteCommand, ScoreboardCommand, FunctionCommand
from config_data import ConfigData

"""
Organizes all lines into their respective mcfunctions

program ::= (NEWLINE)* & (statement)* & (NEWLINE)*

statement ::= "!" && [folder_stmt, mfunc_stmt, prefix_stmt]
folder_stmt ::= "folder" && STR && (NEWLINE)* & INDENT && suite && DEDENT
mfunc_stmt ::= "mfunc" && STR && (NEWLINE)* & INDENT && suite && DEDENT
prefix_stmt ::= "prefix" && STR
suite ::= [statement, command, NEWLINE]+
command ::= (STR)+ && (":" & (NEWLINE)* & INDENT && command_block && DEDENT)?
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


class Parser:
    def __init__(self, lexer, file_path):
        self.lexer = lexer

        self.config_data = ConfigData()

        # requires an mcfunction to be set for commands to be used
        # and an mcfunction cannot be set if one has already been set
        self.current_token = None

        self.current_function = None
        self.current_prefix = None
        self.current_folders = []
        self.current_command_slices = []

        self.file_path = file_path

        # the full path to the mcfunction file output
        # defaults to /mcfunctions/
        # self.file_path = "mcfunctions"

        # list of all mcfunctions avaliable
        self.mcfunctions = []

        self.advance()

    def parse(self):
        self.program()
        logging.debug("")

    def error(self, message=None):
        if message is None:
            message = "Invalid syntax"
        raise SyntaxError("{} : {}".format(repr(self.current_token), message))

    def eat(self, token_type, value=None, error_message=None):
        """
        Advances given the token type and values match up with the current token

        Args:
            token_type (any token type)
            value (any, defaults to None)
        """

        if (value is None or self.current_token.value == value) and self.current_token.matches(token_type):
            self.advance()

        else:
            self.error(error_message)

    def advance(self):
        """
        Gets the next token from the lexer without checking any type
        """
        self.current_token = self.lexer.get_next_token()
        logging.debug("Advanced to {}".format(repr(self.current_token)))

    def program(self):
        """
        program ::= (statement)*
        """
        logging.debug("Begin program at {}".format(repr(self.current_token)))

        while self.current_token.matches_any_of(WhitespaceToken.NEWLINE, SimpleToken.STATEMENT):
            # skips all newlines
            if self.current_token.matches(WhitespaceToken.NEWLINE):
                self.eat(WhitespaceToken.NEWLINE)
                continue

            # otherwise, suite
            self.statement()

        logging.debug("End program at {}".format(repr(self.current_token)))

    def suite(self):
        """
        suite ::= [statement, command]*
        """
        logging.debug("Begin compound at {}".format(repr(self.current_token)))

        # note that this is essentially a do-while since it never starts out as a newline
        met_newline = True
        while met_newline:
            if self.current_token.matches(SimpleToken.STATEMENT):
                # does a continue since the statement might be a compound and not end in a newline
                self.statement()
                continue

            elif self.current_token.matches_any_of(TokenType.STRING, TokenType.SELECTOR):
                self.command()

            met_newline = self.current_token.matches(WhitespaceToken.NEWLINE)
            if met_newline:
                self.eat(WhitespaceToken.NEWLINE)

        logging.debug("End compound at {}".format(repr(self.current_token)))

    def statement(self):
        """
        Handles any post-processor statements

        statement ::= "!" && [folder_stmt, mfunc_stmt]
        """
        # all here should start with "!"
        self.eat(SimpleToken.STATEMENT)

        if self.current_token.value in STATEMENT_TOKEN_VALUES:
            self.current_token.cast(StatementToken)

        if self.current_token.matches(StatementToken.MFUNC):
            self.mfunc_stmt()
        elif self.current_token.matches(StatementToken.PREFIX):
            self.prefix_stmt()
        elif self.current_token.matches(StatementToken.FOLDER):
            self.folder_stmt()
        else:
            self.error("Invalid statement")

    def mfunc_stmt(self):
        """
        mfunc_stmt ::= "mfunc" && STR && (NEWLINE)* & INDENT && suite && DEDENT
        """
        self.eat(StatementToken.MFUNC)

        # if there is an mcfunction already, there is an error
        if self.current_function is not None:
            self.error("Cannot define a mcfunction inside an mcfunction")

        if not self.current_token.matches(TokenType.STRING):
            self.error("Expected a string after a mfunc statement")

        name = self.current_token.value + ".mcfunction"
        full_path = os.path.join(self.file_path, *self.current_folders, name)
        self.current_function = McFunction(full_path, self.current_prefix)

        # guaranteed string token here
        self.advance()

        # skips any and all newlines right after a mfunc statement
        while self.current_token.matches(WhitespaceToken.NEWLINE):
            self.eat(WhitespaceToken.NEWLINE)

        self.eat(WhitespaceToken.INDENT)
        self.suite()
        self.eat(WhitespaceToken.DEDENT)

        # resets the current function
        self.mcfunctions.append(self.current_function)
        self.current_function = None

    def prefix_stmt(self):
        """
        prefix_stmt ::= "prefix" && STR
        """
        self.eat(StatementToken.PREFIX)

        # requires a string as the initials
        if not self.current_token.matches(TokenType.STRING):
            self.error()

        self.current_prefix = self.current_token.value
        self.advance()

    def folder_stmt(self):
        """
        folder_stmt ::= "folder" && STR && (NEWLINE)* & INDENT && suite && DEDENT
        """
        self.eat(StatementToken.FOLDER)

        # requires there to be no current mcfunction since a folder statement
        # always occurs outside a mfunc statement
        if self.current_function is not None:
            self.error("Cannot parse a folder statement inside an mcfunction")

        # sets the current folder
        folder = self.current_token.value
        self.current_folders.append(folder)
        self.eat(TokenType.STRING)

        # skips any and all newlines right after a folder statement
        while self.current_token.matches(WhitespaceToken.NEWLINE):
            self.eat(WhitespaceToken.NEWLINE)

        self.eat(WhitespaceToken.INDENT)
        self.suite()
        self.eat(WhitespaceToken.DEDENT)

        # resets the current folder
        self.current_folders.pop()

    def command(self):
        # checks whether the command can actually be added to an mcfunction or not
        if self.current_function is None:
            self.error("No assigned mcfunction for command")

        # gets all execute shortcuts or scoreboard shortcut
        # while self.current_token.matches(TokenType.SELECTOR) or self.current_token.matches(TokenType.STRING, value="execute"):

        #     # checks whether it is actually part of a scoreboard shortcut
        #     if self.current_token.matches(TokenType.STRING):
        #         execute = self.current_token
        #         self.advance()

        #         # if the next token is not a selector, it is expected to be part of a scoreboard shortcut
        #         # otherwise, the execute part is just simply removed since the execute command doesn't require that part
        #         if not self.current_token.matches(TokenType.SELECTOR):
        #             scoreboard_shortcut = self.cmd_scoreboard(execute)
        #             command.add_scoreboard(scoreboard_shortcut)

        #     selector = self.current_token
        #     self.advance()

        #     # checks whether it is actually a scoreboard shortcut
        #     if self.current_token.matches

        command_tokens = []
        while not (self.lexer.reached_eof or self.current_token.matches_any_of(WhitespaceToken.NEWLINE, WhitespaceToken.DEDENT)):
            command_tokens.append(self.current_token)
            self.advance()
        
        # checks whether a command suite can be used by seeing if the last token is a colon
        if command_tokens[-1].matches(SimpleToken.COLON):
            # self.current_command_slices.append(command_tokens[:-1])

            # # skips any and all newlines
            # while self.current_token.matches(WhitespaceToken.NEWLINE):
            #     self.eat(WhitespaceToken.NEWLINE)

            # self.eat(WhitespaceToken.INDENT)
            # self.suite(commands_only=True)
            # self.eat(WhitespaceToken.DEDENT)
            pass

        else:
            command = Command(command_tokens)
            self.current_function.add_command(command)

    def _debug(self):
        logging.debug("McFunctions assigned: {}".format(len(self.mcfunctions)))
        for mcfunction in self.mcfunctions:
            logging.debug("")
            logging.debug(mcfunction.path)
            for command in mcfunction.commands:
                logging.debug(command)

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
        mcfunction.debug_commands()
