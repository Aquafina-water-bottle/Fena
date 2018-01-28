import os
import logging

from Post.constants import *
from Post.lexicalToken import Token

"""
program ::= suite
suite ::= [statement, command]*

statement ::= "!" && [path_stmt, mfunc_stmt]
path_stmt ::= "path" && STR
mfunc_stmt ::= "mfunc" && STR && NEWLINE & INDENT && suite && DEDENT

command ::= [leading_cmd]* && ending_cmd 
leading_cmd ::= [execute_cmd, (LEADING_START && (STR)*)]
execute_cmd ::= "execute"? && selector && coords? && (["detect", "ifblock"] && coords? && block && [INT, STR]? &&)?

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


class McFunction:
    """
    Contains all commands within a single defined mcfunction
    """

    def __init__(self, path):
        self.path = path
        self.commands = []

        # might be implemented in the future, idk
        self.nick = None

    def addCommand(self, command):
        """
        adds the given command to the commands list

        :param command: string representing the command
        """
        self.commands.append(command)


class Command:
    """
    contains list of tokens for one command
    """
    def __init__(self):
        self.tokenList = []

    def addToken(self, token):
        self.tokenList.append(token)

    def __str__(self):
        return Token.toCommand(self.tokenList)

    def __repr__(self):
        return Token.toCommandRepr(self.tokenList)

    def getTokensAround(self, pos, min, max):
        """
        Gets the tokens around the given position.

        eg. index=5, min=-2, max=3:
            token_index=3, 4, 5, 6, 7, 8

        :param pos: position inside the command
        :param min: how many tokens before the position
        :param max: how many tokens after the position
        :return: token list or None
        """

        listLength = len(self.tokenList)
        if pos+min >= 0 and pos+max < listLength:
            return self.tokenList[pos+min: pos+max+1]

        return None

    def getTokenAt(self, pos):
        """
        Gets the token at the given position

        :param pos: position inside the command
        :return: token or None
        """
        listLength = len(self.tokenList)
        if 0 <= pos < listLength:
            return self.tokenList[pos]

        return None

    def replaceTokens(self, pos, min, max, newTokenList):
        """
        Removes all tokens given the position and inserts the new token list in its place

        :param pos: position inside the command
        :param min: how many tokens before the position
        :param max: how many tokens after the position
        :param newTokenList: all the tokens to be placed after deletion
        :return:
        """

        del self.tokenList[pos + min: pos + max + 1]
        self.tokenList[pos+min: pos+min] = newTokenList

    def replaceToken(self, pos, newTokenList):
        if not isinstance(newTokenList, list):
            newTokenList = [newTokenList]
        self.tokenList[pos: pos+1] = newTokenList

    def insertToken(self, pos, newTokenList):
        if not isinstance(newTokenList, list):
            newTokenList = [newTokenList]
        self.tokenList[pos: pos] = newTokenList


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        # requires an mcfunction to be set for commands to be used
        # and an mcfunction cannot be set if one has already been set
        self.currentFunction = None
        self.currentCommand = None
        self.currentToken = None

        # the full path to the mcfunction file output
        # defaults to /mcfunctions/
        # self.filePath = "mcfunctions"

        # list of all mcfunctions avaliable
        self.mcfunctions = []

        self.advance()

    def parse(self):
        self.suite()
        # self._debug()

    def error(self, message=None):
        if message is None:
            logging.error(repr(self.currentToken) + ": Invalid syntax")
        else:
            logging.error(repr(self.currentToken) + ": {}".format(message))
        raise SyntaxError

    def eat(self, type, value=None):
        """
        Allows the following options:
            -no parameters: eats any token
            -type: eats given type
            -type, value: eats given type and value

        :param type:
        :param value:
        :return:
        """

        if value is None and self.currentToken.type == type:
            self.advance()

        elif (value is None and isinstance(type, tuple) and
                type[0] == self.currentToken.type and type[1] == self.currentToken.value):
            self.advance()

        elif (type is not None and value is not None and
                self.currentToken.type == type and self.currentToken.value == value):
            self.advance()

        else:
            self.error()

    def advance(self):
        """
        simply gets the next token from the lexer

        :return:
        """
        self.currentToken = self.lexer.getNextToken()
        logging.debug("Advanced to {}".format(repr(self.currentToken)))

    def suite(self):
        """ suite ::= [statement, command]* """

        # does this in the beginning since no newline

        # ignores pure newlines
        if self.currentToken.matches(NEWLINE):
            pass
        elif self.currentToken.matches(STATEMENT):
            # advances "!"
            self.advance()
            self.statement()
        else:
            self.command()

        while self.currentToken.matches(NEWLINE):
            self.eat(NEWLINE)

            # breaks if it's a dedent
            if self.currentToken.matches(DEDENT) or self.currentToken.matches(EOF):
                break

            # ignores pure newlines
            if self.currentToken.matches(NEWLINE):
                continue

            if self.currentToken.matches(STATEMENT):
                # advances "!"
                self.advance()
                self.statement()
            else:
                self.command()

        logging.debug("End compound at {}".format(repr(self.currentToken)))

    def statement(self):
        """
        Handles any post-processor statements
        """
        # all here should end in a newline
        if self.currentToken.matches(MFUNC):
            self.mfunc_stmt()
        # elif self.currentToken.matches(PATH):
        #     self.path_stmt()
        else:
            self.error("Invalid statement")

    # def path_stmt(self):
    #     self.eat(PATH)
    #     self.filePath = self.currentToken.value
    #     self.eat(STRING)

    def mfunc_stmt(self):
        self.eat(MFUNC)

        # if there is no mcfunction, then success
        # otherwise, error
        if self.currentFunction is None:
            name = self.currentToken.value + ".mcfunction"
            # fullPath = os.path.join(self.filePath, name)
            # self.currentFunction = McFunction(fullPath)
            self.currentFunction = McFunction(name)
        else:
            self.error("Cannot define a mcfunction inside an mcfunction")

        self.eat(STRING)
        self.eat(NEWLINE)
        self.eat(INDENT)
        self.suite()
        self.eat(DEDENT)

        # resets the current function
        self.mcfunctions.append(self.currentFunction)
        self.currentFunction = None

    def command(self):
        # checks whether the command can actually be added to an mcfunction or not
        if self.currentFunction is None:
            self.error("No assigned mcfunction for command")

        if self.currentCommand is not None:
            self.error("Unknown error: Cannot create a new command as one already exists")

        self.currentCommand = Command()
        while (not self.lexer.reachedEOF and
               not self.currentToken.matches(NEWLINE) and not self.currentToken.matches(DEDENT)):
            self.currentCommand.addToken(self.currentToken)
            self.advance()

        self.currentFunction.addCommand(self.currentCommand)
        self.currentCommand = None

    def _debug(self):
        logging.debug("McFunctions assigned: {}".format(len(self.mcfunctions)))
        for mcfunction in self.mcfunctions:
            logging.debug("")
            logging.debug(mcfunction.path)
            for command in mcfunction.commands:
                logging.debug(command)
