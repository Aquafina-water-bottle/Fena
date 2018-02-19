import logging
import os

from Post.constants import (SELECTOR, PLUS, MINUS, EQUALS, TEST, ENABLE, RESET, COMMAND,
    PLUGIN_CONFLICT_COMMANDS, INT, STRING, LEADING_COMMAND, COORD, IFBLOCK, DETECT)
from Post.lexicalToken import Token
from Post.configData import options
from Post.selector import getSelector


class Interpreter:
    """
    Args:
        parser (Parser): the current parser

    Attributes:
        pos (int): the position incrementer for each full command
        cmd (list of Token(s)): the list of tokens representing a single full command
        token (Token): the current token being analyzed
        tokenStrs (list of str(s)): stores the token values as strings
        reachedEnd (bool): whether the end of the full command has been reached or not
        reachedCmd (bool): whether in the current full command, a command that cannot have
            a sub command has been reached or not
    """

    def __init__(self, parser):
        self.parser = parser

        self.pos = 0
        self.cmd = None
        self.token = None
        self.tokenStrs = []
        self.reachedEnd = False
        self.reachedCmd = False
        self.path = None

        self.operatorTo = {
            "+": "add",
            "-": "remove",
            "=": "set",
            "?": "test",
        }

        self.keywords = {
            "ScOP": "scoreboard players operation",
            "ScTA": "scoreboard teams add",
            "ScTO": "scoreboard teams option",
            "ScTR": "scoreboard teams remove",
            "ScOA": "scoreboard objectives addj",
            "ScSS": "scoreboard objectives setdisplay sidebar",
            "ScOS": "scoreboard objectives setdisplay",
            "ScOR": "scoreboard objectives remove",
            "join": "scoreboard teams join",
            "leave": "scoreboard teams leave",
            "empty": "scoreboard teams empty",
        }


    def interpret(self):
        self.parser.parse()

        for mcfunction in self.parser.mcfunctions:
            for command in mcfunction.commands:

                cmdStr = self.interpretCmd(command, mcfunction.path)
                mcfunction.cmd_strs.append(cmdStr)

                logging.debug("INITIAL: {}".format(Token.toCommand(command)))
                logging.debug("FINAL: {}".format(cmdStr))
                logging.debug("")

                # self.keywords(command)
                # self.scoreboardShortcut(command)
                # self.executeShortcut(command)
                # self.selectorShortcut(command)
                # logging.debug("FINAL: {}".format(str(command)))
                # logging.debug("")

        return self.parser.mcfunctions

    def error(self, message, token=None):
        if token is None:
            logging.error("Error during shortcut creation at {0}: {1}".format(repr(self.token), message))
        else:
            logging.error("Error during shortcut creation at {0}: {1}".format(repr(token), message))
        raise SyntaxError
    
    def advance(self, number=1):
        """
        Increments the position by one
        If the interpreter detects whether the end of the command
        was reached, it will set self.reachedEnd to True
        """
        while number > 0:
            self.pos += 1

            # checks if the end of the command has been reached
            if self.pos > len(self.cmd) - 1:
                self.reachedEnd = True
                break

            self.token = self.cmd[self.pos]
            logging.debug("Interpreter advanced to {}".format(repr(self.token)))
            number -= 1

    def checkRange(self, min, max):
        """
        Looks around the current position to see if tokens exist

        Args:
            min (int)
            max (int)

        Returns:
            bool: whether tokens exist between the min and max relative to
                the current position
        """
        return self.checkBefore(min) and self.checkAhead(max)

    def checkAhead(self, num):
        """
        Looks ahead of the current position to see if a token exists
        """
        assert num >= 0
        return not (self.pos + num > len(self.cmd) - 1)

    def checkBefore(self, num):
        """
        Looks before of the current position to see if a token exists
        """
        assert num >= 0
        return not (self.pos - num < 0)

    def lookAhead(self, num):
        """
        Looks ahead of the command to get the token

        Args:
            num: The relative position of the gotten token

        Returns:
            Token: the token with that relative position to the right of the token list
            None: if there is no token that can be gotten ahead
        """
        if self.checkAhead(num):
            return self.cmd[self.pos + num]
        return None

    def lookBehind(self, num):
        """
        Looks behind of the command to get the token

        Args:
            num: The relative position of the gotten token

        Returns:
            Token: the token with that relative position to the right of the token list
            None: if there is no token that can be gotten ahead
        """
        if self.checkBefore(num):
            return self.cmd[self.pos - num]
        return None

    def interpretCmd(self, cmd, path):
        """
        Converts the token list to a usable command string
        """
        # Resets all values
        self.pos = 0
        self.cmd = cmd
        self.token = self.cmd[self.pos]
        self.tokenStrs.clear()
        self.reachedEnd = False
        self.reachedCmd = False
        self.path = path

        logging.debug("First interpreter token set to {}".format(repr(self.token)))

        while not self.reachedEnd:
            tokenStr = str(self.getNextTokenStr())
            self.tokenStrs.append(tokenStr)

        return " ".join(self.tokenStrs)

    def getNextTokenStr(self):
        tokenVal = self.token.value

        # if a command has been reached, no other shortcuts can be used
        if self.reachedCmd:
            return self.default()

        # checks whether the current value is a keyword
        # if it is a keyword, then the keyword is added
        # note that all keywords start with "scoreboard", meaning
        # a command has been reached
        if tokenVal in self.keywords:
            tokenStr = self.keywords[tokenVal]
            self.reachedCmd = True
            self.advance()
            return tokenStr

        if self.token.matchesOne(DETECT, IFBLOCK):
            return self.executeBlock()

        if self.checkRange(0, 3) and self.lookAhead(2).matchesOne(PLUS, MINUS, EQUALS, TEST):
            return self.scoreboardMath()

        if self.checkRange(0, 2) and self.lookAhead(1).matchesOne(PLUS, MINUS):
            return self.scoreboardTag()

        if self.checkRange(0, 2) and self.lookAhead(1).matchesOne(RESET, ENABLE):
            return self.scoreboardSimple()

        # checks whether the current token is a command
        if self.token.matches(COMMAND):
            self.reachedCmd = True

            # checks whether the current token can be a function shortcut
            if tokenVal == "function":
                return self.function()

            elif tokenVal in options[PLUGIN_CONFLICT_COMMANDS]:
                self.advance()
                return "minecraft:" + tokenVal

        # default value if no shortcut has been found
        return self.default()                

    def default(self):
        """
        Returns itself and advances itself, but will use the 
        selector shortcut if the current token is a selector
        """

        # if the token is any old selector, selector shortcut
        if self.token.matches(SELECTOR):
            # if the token is a selector and no command has been reached yet, execute shortcut
            if not self.reachedCmd:
                tokenStr = self.executeBegin()
            else:
                tokenStr = self.selector()
        else:
            tokenStr = self.token.value

        self.advance()
        return tokenStr

    def selector(self, token=None):
        if token is None:
            return getSelector(self.token)
        return getSelector(token)

    def function(self):
        # just advances itself since it is at "function" already
        self.advance()

        if not self.token.matches(STRING):
            self.error("Expected a string token when getting an argument for a /function command")

        # if a colon is not present, that means it is a shortcut
        if ":" in self.token.value:
            return "function {}".format(self.default())
        else:
            eventName = os.path.basename(os.path.dirname(self.path))
            return "function ego:{event}/{name}".format(event=eventName, name=self.default())

    def name(self, token):
        """
        name ::= [COMMAND, STRING, INT, selector]
        """
        if token.matches(SELECTOR):
            return self.selector(token)
        return token.value

    def scoreboardMath(self):
        """
        grammar: name objective [+, -, =, ?] score
        return value: scoreboard players [add, remove, set, test] name objective score
        """

        # checks whether the grammar makes sense or not
        if (self.token.matchesOne(COMMAND, SELECTOR, STRING, INT) and
                self.lookAhead(1).matches(STRING) and
                self.lookAhead(3).matches(INT)):

            name = self.name(self.token)
            objective = self.lookAhead(1).value
            operator = self.operatorTo[self.lookAhead(2).value]
            score = self.lookAhead(3).value

            self.reachedCmd = True
            self.advance(4)

            return "scoreboard players {0} {1} {2} {3}".format(operator, name, objective, score)
        return self.default()

    def scoreboardTag(self):
        """
        grammar: name [+, -, =, ?] tag
        return value: scoreboard players tag name [add, remove] tag
        """
        if (self.token.matchesOne(COMMAND, SELECTOR, STRING, INT) and 
                self.lookAhead(2).matches(STRING)):

            name = self.name(self.token)
            operator = self.operatorTo[self.lookAhead(1).value]
            tag = self.lookAhead(2).value

            self.reachedCmd = True
            self.advance(3)

            return "scoreboard players tag {0} {1} {2}".format(name, operator, tag)
        return self.default()

    def scoreboardSimple(self):
        """
        name [reset, enable] objective
        scoreboard players [reset, enable] name objective
        """
        if (self.token.matchesOne(COMMAND, SELECTOR, STRING, INT) and 
                self.lookAhead(2).matches(STRING)):

            operator = self.lookAhead(1).value
            name = self.name(self.token)
            objective = self.lookAhead(2).value

            self.reachedCmd = True
            self.advance(3)

            return "scoreboard players {0} {1} {2}".format(operator, name, objective)
        return self.default()

    def executeBegin(self):
        """
        Does the beginning part of the execute shortcut, which
        converts selectors into "execute selector coords"

        Note that this doesn't advance since the only time this is
        called is under Interpreter.default, which advances itself

        execute_cmd ::= ("execute"? && selector && coords?) && (["detect", "ifblock"] && coords? && block && [INT, STR]?)?
        """
        tokenStrs = []
        selectorStr = getSelector(self.token)
        tokenStrs.append(selectorStr)

        # invalid syntax for literally nothing is after a selector without a preceeding command
        if not self.checkAhead(1):
            self.error("Expected a command somewhere after the selector")

        # checks whether "execute" exists before the name
        if not self.checkBefore(1) or not self.lookBehind(1).matches(LEADING_COMMAND, "execute"):
            tokenStrs.insert(0, "execute")

        # checks whether coordinates exist after the name
        if not self.checkRange(0, 3) or not self.lookAhead(1).matchesOne(COORD, INT):
            tokenStrs.append("~ ~ ~")

        logging.debug("{0} --> {1}".format(self.token, "'{}'".format(" ".join(tokenStrs))))

        return " ".join(tokenStrs)

    def executeBlock(self):
        """
        Does the ending part of the execute command, which
        is only if "detect" or "ifblock" is detected

        execute_cmd ::= ("execute"? && selector && coords?) && (["detect", "ifblock"] && coords? && block && [INT, STR]?)?
        """
        tokenStrs = ["detect"]

        # if there is literally nothing after the detect, error since
        # there should be a block (at least) after it
        if not self.checkAhead(1):
            self.error("Expected a block after an 'execute detect' command")

        # checks if there are coordinates after the "detect" or "ifblock"
        # if not, creates coordinates
        self.advance()
        if self.token.matchesOne(COORD, INT):

            # gets the next 3 tokens as coordinates
            for _ in range(3):
                # makes sure the token is a coordinate
                if not self.token.matchesOne(COORD, INT):
                    self.error("Expected coordinates after one coordinate when detecting a block")
                tokenStrs.append(str(self.token.value))
                self.advance()

        else:
            tokenStrs.append("~ ~ ~")

        # the current position here should be at a block
        if not self.token.matches(STRING):
            self.error("Expected a block after an 'execute detect' command")

        # gets the block and advances
        tokenStrs.append(self.token.value)
        self.advance()

        # note that this allows integers OR strings because data values and 1.12 data states
        if not (self.token.matches(INT) or (self.token.matches(STRING, "*")) or (self.token.matches(STRING) and "=" in self.token.value)):
            tokenStrs.append("*")

        return " ".join(tokenStrs)
