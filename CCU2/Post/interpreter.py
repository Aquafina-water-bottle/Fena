import logging

from Post.constants import *
from Post.lexicalToken import Token
from Post.configData import options


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.selectorVarReplace = {
            "limit": "c",
            "gamemode": "m",
        }

        self.selectorRangeShort = {
            "dist": "distance",
            "lvl": "level",
            "x_rot": "x_rotation",
            "y_rot": "y_rotation",
        }

        self.selectorRangeLookup = {
            "distance": ("r", "rm"),
            "level": ("l", "lm"),
            "x_rotation": ("rx", "rxm"),
            "y_rotation": ("ry", "rym"),
        }

    def interpret(self):
        self.parser.parse()
        for mcfunction in self.parser.mcfunctions:
            for command in mcfunction.commands:
                logging.debug("INITIAL: {}".format(str(command)))
                self.keywords(command)
                self.scoreboardShortcut(command)
                self.executeShortcut(command)
                self.selectorShortcut(command)
                logging.debug("FINAL: {}".format(str(command)))
                logging.debug("")

        return self.parser.mcfunctions

    @staticmethod
    def error(message):
        logging.error("Error during shortcut creation: {}".format(message))
        raise SyntaxError

    def keywords(self, command):
        """
        Replaces default keywords
        """

        keywords = {
            "ScOP": [Token(None, COMMAND, "scoreboard"), Token(None, STRING, "players"), Token(None, STRING, "operation")],
            "ScTA": [Token(None, COMMAND, "scoreboard"), Token(None, STRING, "teams"), Token(None, STRING, "add")],
            "ScTO": [Token(None, COMMAND, "scoreboard"), Token(None, STRING, "teams"), Token(None, STRING, "option")],
            "ScTR": [Token(None, COMMAND, "scoreboard"), Token(None, STRING, "teams"), Token(None, STRING, "remove")],
            "ScOA": [Token(None, COMMAND, "scoreboard"), Token(None, STRING, "objectives"), Token(None, STRING, "add")],
            "ScSS": [Token(None, COMMAND, "scoreboard"), Token(None, STRING, "objectives"),
                     Token(None, STRING, "setdisplay"), Token(None, STRING, "sidebar")],
            "ScOS": [Token(None, COMMAND, "scoreboard"), Token(None, STRING, "objectives"),Token(None, STRING, "setdisplay")],
            "ScOR": [Token(None, COMMAND, "scoreboard"), Token(None, STRING, "objectives"), Token(None, STRING, "remove")],
        }

        for index in range(len(command.tokenList)):
            token = command.tokenList[index]

            # if the token is a string, it could be a keyword
            if token.matches(STRING):
                strValue = token.value

                # if the strValue is inside the dictionary, it will return a string
                # otherwise, it will return None
                newValue = keywords.get(strValue)
                if newValue is not None:

                    command.replaceToken(index, newValue)
                    logging.debug(" -> {}".format(str(command)))

    def scoreboardShortcut(self, command):
        for index in range(len(command.tokenList)):
            token = command.tokenList[index]

            # immediately exits after reaching a command
            if token.matches(COMMAND):
                break

            if token.matchesOne(PLUS, MINUS, EQUALS):
                # selector objective [+, -, =] int
                # scoreboard players [add, remove, set] selector objective int
                # token[2] is operator
                tokens = command.getTokensAround(index, -2, 1)
                if tokens is not None and (tokens[0].matchesOne(SELECTOR, STRING, INT) and
                                           tokens[1].matches(STRING) and tokens[3].matches(INT)):
                    scoreboard = Token(None, COMMAND, "scoreboard")
                    players = Token(None, STRING, "players")

                    # whether it's add, remove or set
                    if token.matches(PLUS):
                        math = Token(None, STRING, "add")
                    elif token.matches(MINUS):
                        math = Token(None, STRING, "remove")
                    elif token.matches(EQUALS):
                        math = Token(None, STRING, "set")
                    else:
                        Interpreter.error("Unknown error")

                    # removes [+, -, =]
                    tokens.pop(2)

                    # adds "scoreboard players add"
                    tokens[0:0] = [scoreboard, players, math]
                    logging.debug("{}".format(str(command)))
                    command.replaceTokens(index, -2, 1, tokens)
                    logging.debug(" -> {}".format(str(command)))

                    # breaks since no other scoreboard shortcut can happen
                    break

            if token.matchesOne(PLUS, MINUS, EQUALS):
                # selector [+, -] tag
                # scoreboard players tag selector [add, remove] tag
                # token[1] is operator
                tokens = command.getTokensAround(index, -1, 1)
                if tokens is not None and tokens[0].matchesOne(SELECTOR, STRING, INT) and tokens[2].matches(STRING):
                    scoreboard = Token(None, COMMAND, "scoreboard")
                    players = Token(None, STRING, "players")
                    tag = Token(None, STRING, "tag")

                    # whether it's add or remove
                    if token.matches(PLUS):
                        math = Token(None, STRING, "add")
                    elif token.matches(MINUS):
                        math = Token(None, STRING, "remove")
                    else:
                        Interpreter.error("Unknown error")

                    # adds "add" and removes "+"
                    tokens.insert(2, math)
                    tokens.pop(1)

                    # adds "scoreboard players tag"
                    tokens[0:0] = [scoreboard, players, tag]
                    logging.debug("{}".format(str(command)))
                    command.replaceTokens(index, -1, 1, tokens)
                    logging.debug(" -> {}".format(str(command)))
                    break

            if token.matchesOne(RESET, ENABLE):
                # selector [reset, enable] objective
                # scoreboard players [reset, enable] selector objective
                # token[1] is operator
                tokens = command.getTokensAround(index, -1, 1)
                if tokens is not None and tokens[0].matchesOne(SELECTOR, STRING, INT) and tokens[2].matches(STRING):
                    scoreboard = Token(None, COMMAND, "scoreboard")
                    players = Token(None, STRING, "players")

                    # whether it's add or remove
                    if token.matches(RESET):
                        operator = Token(None, STRING, RESET[VALUE])
                    elif token.matches(ENABLE):
                        operator = Token(None, STRING, ENABLE[VALUE])
                    else:
                        Interpreter.error("Unknown error")

                    # removes operator
                    tokens.pop(1)

                    # adds "scoreboard players enable/reset"
                    tokens[0:0] = [scoreboard, players, operator]
                    logging.debug("{}".format(str(command)))
                    command.replaceTokens(index, -1, 1, tokens)
                    logging.debug(" -> {}".format(str(command)))
                    break

            if token.matches(TEST):
                # selector objective ? score (score)?
                # scoreboard players test selector objective score score
                # token[0]=selector, token[1]=objective, token[2]=test, token[3]=score
                tokens = command.getTokensAround(index, -2, 1)
                if (tokens is not None and tokens[0].matchesOne(SELECTOR, STRING, INT)
                        and tokens[1].matches(STRING) and tokens[3].matches(INT)):
                    scoreboard = Token(None, COMMAND, "scoreboard")
                    players = Token(None, STRING, "players")
                    test = Token(None, STRING, "test")

                    # removes operator
                    tokens.pop(2)

                    # adds "scoreboard players test"
                    tokens[0:0] = [scoreboard, players, test]
                    logging.debug("{}".format(str(command)))
                    command.replaceTokens(index, -2, 1, tokens)
                    logging.debug(" -> {}".format(str(command)))
                    break

            if token.matches(JOIN):
                # join team_name selector
                # scoreboard teams join team_name selector
                # token[0] is team_name, token[1] is selector
                tokensCheck = command.getTokensAround(index, 1, 2)
                if tokensCheck is not None and tokensCheck[0].matches(STRING) and tokensCheck[1].matchesOne(SELECTOR, STRING, INT):
                    scoreboard = Token(None, COMMAND, "scoreboard")
                    teams = Token(None, STRING, "teams")
                    join = Token(None, STRING, JOIN[VALUE])

                    # replaces "join" with "scoreboard teams join"
                    insertedTokens = [scoreboard, teams, join]
                    logging.debug("JOIN: {}".format(str(command)))
                    command.replaceToken(index, insertedTokens)
                    logging.debug(" -> {}".format(str(command)))
                    break

            if token.matches(LEAVE):
                # leave selector
                # scoreboard teams leave selector
                # check if the token after "leave" is a string, selector or int
                tokenCheck = command.getTokenAt(index+1)
                if tokenCheck is not None and tokenCheck.matchesOne(SELECTOR, STRING, INT):
                    scoreboard = Token(None, COMMAND, "scoreboard")
                    teams = Token(None, STRING, "teams")
                    leave = Token(None, STRING, LEAVE[VALUE])

                    # replaces "leave" with "scoreboard teams leave"
                    insertedTokens = [scoreboard, teams, leave]
                    logging.debug("LEAVE: {}".format(str(command)))
                    command.replaceToken(index, insertedTokens)
                    logging.debug(" -> {}".format(str(command)))
                    break

            if token.matches(EMPTY):
                # empty team_name
                # scoreboard teams empty team_name
                # check if the token after "empty" is a string
                tokenCheck = command.getTokenAt(index+1)
                if tokenCheck is not None and tokenCheck.matches(STRING):
                    scoreboard = Token(None, COMMAND, "scoreboard")
                    teams = Token(None, STRING, "teams")
                    empty = Token(None, STRING, EMPTY[VALUE])

                    # replace "empty" with "scoreboard teams empty"
                    insertedTokens = [scoreboard, teams, empty]
                    logging.debug("EMPTY: {}".format(str(command)))
                    command.replaceToken(index, insertedTokens)
                    logging.debug(" -> {}".format(str(command)))
                    break

    def executeShortcut(self, command):
        index = 0
        while index < len(command.tokenList):
            token = command.tokenList[index]

            # immediately exits after reaching a command
            if token.matches(COMMAND):
                break

            # all execute commands are based off of the first selector
            # does the "execute" and coords after the selector
            if token.matches(SELECTOR):
                # "execute"? selector coords?
                # tokenCheck is supposed to be coords
                tokenCheck = command.getTokenAt(index+1)

                # this isn't a valid command if it cannot get the next token
                if tokenCheck is None:
                    Interpreter.error("Expected a command after the selector around {}".format(repr(token)))

                if not tokenCheck.matchesOne(COORD, INT):
                    # adds 3 different coordinate tokens
                    coordinates = []
                    for _ in range(3):
                        coord = Token(None, COORD, "~")
                        coordinates.append(coord)

                    logging.debug("EXEC 1: {}".format(str(command)))
                    command.insertToken(index+1, coordinates)
                    logging.debug(" -> {}".format(str(command)))

                # "execute"? selector coords
                # tokenCheck is supposed to be "execute"
                tokenCheck = command.getTokenAt(index-1)
                if tokenCheck is None:
                    executeToken = Token(None, LEADING_COMMAND, "execute")

                    logging.debug("EXEC 2.1: {}".format(str(command)))
                    command.insertToken(index, executeToken)
                    logging.debug(" -> {}".format(str(command)))

                elif not tokenCheck.matches(LEADING_COMMAND, "execute"):
                    executeToken = Token(None, LEADING_COMMAND, "execute")

                    logging.debug("EXEC 2.2: {}".format(str(command)))
                    # replaces selector with ["execute", selector]
                    command.insertToken(index, executeToken)
                    logging.debug(" -> {}".format(str(command)))

            # detect block
            if token.matchesOne(DETECT, IFBLOCK):
                # see if there are coords by checking whether the token after "DETECT" or "IFBLOCK"
                # is an int or coord
                # ifblock [coord?]
                tokenCheck = command.getTokenAt(index+1)

                if not tokenCheck.matchesOne(COORD, INT):
                    coordinates = []
                    for _ in range(3):
                        coord = Token(None, COORD, "~")
                        coordinates.append(coord)

                    logging.debug("EXEC 3: {}".format(str(command)))
                    command.insertToken(index+1, coordinates)
                    logging.debug(" -> {}".format(str(command)))

                # check if after the coordinates, whether the tokens are STR, and (INT or STR)
                # index is at "DETECT", "IFBLOCK"
                # ifblock coord1 coord2 coord3 [block number?]
                tokensCheck = command.getTokensAround(index, 4, 5)
                if (tokensCheck is not None and
                        tokensCheck[0].matches(STRING) and not tokensCheck[1].matchesOne(INT, STRING)):
                    starToken = Token(None, STRING, "*")
                    logging.debug("EXEC 4: {}".format(str(command)))
                    command.insertToken(index+5, starToken)
                    logging.debug(" -> {}".format(str(command)))

                # replaces IFBLOCK and DETECT with their string tokens
                detectToken = Token(None, STRING, DETECT[VALUE])
                command.replaceToken(index, detectToken)

            index += 1

    def selectorRange(self, var, value):
        """
        Gets the argument as a string for any given range, and returns the parsed version

        :param var: the variable of a selector argument
        :param value: the value range of a selector argument, which is # OR ..# OR #.. OR #..#
        :return: parsed argument string
        """

        # will store each argument as a var=key pair
        argumentList = []

        # for variables that aren't a score
        # so they are put under the dictionary
        if var in self.selectorRangeLookup:
            begVar, endVar = self.selectorRangeLookup[var]
        else:
            # guaranteed to be a score value
            begVar = "score_{}_min".format(var)
            endVar = "score_{}".format(var)

        # if ".." isn't present, that means both are set to the same value
        if ".." not in value:
            begRange = endRange = value
        else:
            begRange, endRange = value.split("..")

        # checks if the beginning range is actually bigger for some reason
        if begRange and endRange and int(begRange) > int(endRange):
            self.error("Beginning range cannot be larger than the end range")

        # does the following if begRange is not empty
        if begRange:
            arg = "{var}={value}".format(var=begVar, value=begRange)
            argumentList.append(arg)

        if endRange:
            arg = "{var}={value}".format(var=endVar, value=endRange)
            argumentList.append(arg)

        argStr = ",".join(argumentList)
        logging.debug("Changed '{0}={1}' to '{2}'".format(var, value, argStr))
        return argStr

    def joinSelector(self, beg, args, end):
        """

        :param beg:
        :param args:
        :param end:
        :return:
        """
        pass

    def selectorShortcut(self, command):
        """
        selectors have @x[arg, arg, ...], where arg: var=value

        :param command:
        :return:
        """
        for index in range(len(command.tokenList)):
            token = command.tokenList[index]
            if token.matches(SELECTOR):
                selectorStr = token.value

                # checks if it has square brackets
                if "[" not in selectorStr or "]" not in selectorStr:
                    continue

                # checks if the token literally ends with 2 square brackets, meaning parsing the
                # inside is a waste of time
                if selectorStr[-2:] == "[]":
                    continue

                # gets the values within the selector
                selectorBeg = token.value[0:3]
                selectorEnd = "]"
                selectorArgs = token.value[3: -1].split(",")

                for argIndex in range(len(selectorArgs)):
                    selectorArg = selectorArgs[argIndex]
                    selectorArg = selectorArg.strip()

                    # if there is no "=", it means it's a tag=
                    if "=" not in selectorArg:
                        selectorArg = "tag=" + selectorArg
                        selectorArgs[argIndex] = selectorArg
                        logging.debug("Added tag: {}".format(selectorArg))
                        continue

                    var, value = selectorArg.split("=")

                    # if the var is within the shorthand for a normal selector variable,
                    # it is set as the replacement and then ignored
                    if var in self.selectorVarReplace:
                        newVar = self.selectorVarReplace[var]
                        selectorArg = "{var}={value}".format(var=newVar, value=value)
                        logging.debug("Modified 1.13 replacement: {}".format(selectorArg))
                        selectorArgs[argIndex] = selectorArg
                        continue

                    # if the var is within the normal selector variables, it is entirely ignored
                    if var in options[SELECTOR_VARIABLES]:
                        continue

                    # if the var is within the shorthand for ranges
                    if var in self.selectorRangeShort:
                        var = self.selectorRangeShort[var]

                    # If the code has made it here, the variable is either
                    # a score or within the selector range lookup
                    selectorArgs[argIndex] = self.selectorRange(var, value)

                # Joins all modified selector arguments and puts it back into the string
                token.value = selectorBeg + (",".join(selectorArgs)) + selectorEnd

