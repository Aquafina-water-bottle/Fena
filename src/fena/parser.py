import os
import logging

from token_types import TokenType, SimpleToken, WhitespaceToken, StatementToken, ALL_TOKENS
from mcfunction import McFunction

"""
program ::= suite
suite ::= [statement, command]*

statement ::= "!" && [folder_stmt, mfunc_stmt]
path_stmt ::= "folder" && STR && NEWLINE & INDENT && suite && DEDENT
mfunc_stmt ::= "mfunc" && STR && NEWLINE & INDENT && suite && DEDENT

command ::= [leading_cmd]* && ending_cmd 
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

        # requires an mcfunction to be set for commands to be used
        # and an mcfunction cannot be set if one has already been set
        self.current_function = None
        self.current_command = []
        self.current_token = None

        self.file_path = file_path

        # the full path to the mcfunction file output
        # defaults to /mcfunctions/
        # self.file_path = "mcfunctions"

        # list of all mcfunctions avaliable
        self.mcfunctions = []

        self.advance()

    def parse(self):
        self.suite()
        logging.debug("")
        # self._debug()

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

        if (value is None or self.current_token.value == value) and self.current_token.type.matches(token_type):
            self.advance()

        else:
            self.error(error_message)

    def advance(self):
        """
        Gets the next token from the lexer without checking any type
        """
        self.current_token = self.lexer.get_next_token()
        logging.debug("Advanced to {}".format(repr(self.current_token)))

    def suite(self):
        """
        suite ::= [statement, command]*
        """

        # ignores pure newlines
        if self.current_token.matches(NEWLINE):
            pass
        elif self.current_token.matches(STATEMENT):
            # advances "!"
            self.advance()
            self.statement()
        else:
            self.command()

        while self.current_token.matches(NEWLINE):
            self.eat(NEWLINE)

            # breaks if it's a dedent
            if self.current_token.matches(DEDENT) or self.current_token.matches(EOF):
                break

            # ignores pure newlines
            if self.current_token.matches(NEWLINE):
                continue

            if self.current_token.matches(STATEMENT):
                # advances "!"
                self.advance()
                self.statement()
            else:
                self.command()

        logging.debug("End compound at {}".format(repr(self.current_token)))

    def statement(self):
        """
        Handles any post-processor statements
        """
        # all here should end in a newline
        if self.current_token.matches(MFUNC):
            self.mfunc_stmt()
        # elif self.current_token.matches(PATH):
        #     self.path_stmt()
        else:
            self.error("Invalid statement")

    # def path_stmt(self):
    #     self.eat(PATH)
    #     self.file_path = self.current_token.value
    #     self.eat(STRING)

    def mfunc_stmt(self):
        self.eat(MFUNC)

        # if there is no mcfunction, then success
        # otherwise, error
        if self.current_function is None:
            name = self.current_token.value + ".mcfunction"
            fullPath = os.path.join(self.file_path, name)
            self.current_function = McFunction(fullPath)
            # self.current_function = McFunction(name)
        else:
            self.error("Cannot define a mcfunction inside an mcfunction")

        self.eat(STRING)
        self.eat(NEWLINE)
        self.eat(INDENT)
        self.suite()
        self.eat(DEDENT)

        # resets the current function
        self.mcfunctions.append(self.current_function)
        self.current_function = None

    def command(self):
        # checks whether the command can actually be added to an mcfunction or not
        if self.current_function is None:
            self.error("No assigned mcfunction for command at {}")

        if self.current_command:
            self.error("Unknown error: Cannot create a new command as one already exists")

        while (not self.lexer.reachedEOF and
               not self.current_token.matches(NEWLINE) and not self.current_token.matches(DEDENT)):
            self.current_command.append(self.current_token)
            self.advance()

        self.current_function.addCommand(self.current_command[:])
        self.current_command.clear()

    def _debug(self):
        logging.debug("McFunctions assigned: {}".format(len(self.mcfunctions)))
        for mcfunction in self.mcfunctions:
            logging.debug("")
            logging.debug(mcfunction.path)
            for command in mcfunction.commands:
                logging.debug(command)
