"""
Returns a list of tokens
    operators:
        "+" -> add OR tag @x add
        "-" -> remove OR tag @x remove
        "?" -> test
        "=" -> set
        "reset" -> reset
        "enable" -> enable

        "join" team name
        "empty" team
        "leave" name

    selector
    int
    coordinates
    datatag
    string
    command
    execute
    block
"""

import logging

from queue import Queue

from Post.constants import *
from Post.configData import options
from Post.lexicalToken import Token


class Lexer:
    def __init__(self, text, fileName):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        self.fileName = fileName

        # self.pos is an index into self.text
        self.pos = 0

        # whether the end of the file has been reached or not
        self.reachedEOF = False

        # row, column
        self.posInFile = [1, 1]

        # temporary value for setting the locked position
        self.locked = False
        self.lockedPos = None
        self.lockedPosInFile = None

        # list of indent strings
        # 1 indent is either 4 spaces or 1 tab space
        self.indentLength = 0

        self.storedTokens = Queue()

        if len(self.text) == 0:
            logging.error("File does not contain anything")
            raise EOFError

        # this is here because the first statement has to be handled
        self.handleAfterNewline()

    def getPosRepr(self):
        line, column = self.posInFile
        return "Line {0} column {1}: ".format(line, column)

    def getTokenPos(self):
        """
        Note that this should only be used for creating tokens

        :return: position of the token
        """

        if self.locked:
            posInFile = (self.posInFile[0], self.lockedPosInFile[1])
            return tuple(posInFile)
        else:
            return tuple(self.posInFile)

    def error(self, message=None):
        if message is None:
            logging.error(self.getPosRepr() + "Invalid character '{}'".format(self.getCurrentChars()))
        else:
            logging.error(self.getPosRepr() + message)
        raise TypeError

    def advance(self, number=1):
        """
        Advance the "pos" pointer and set the "current_char" variable.

        number can either be a string or an integer, where
        the number incremented will be the string length
        """

        if isinstance(number, str):
            number = len(number)

        # while loop to increment the self.posInFile variable
        while number > 0:

            # if the current character is \n, goes to a new line
            # note that the position increments after this, meaning
            # that "\n" is actually the previous character
            if self.currentCharsAre("\n"):
                self.posInFile[0] += 1
                self.posInFile[1] = 1
            else:
                self.posInFile[1] += 1

            # if the current character is \t, adds 3 to the length
            if self.currentCharsAre("\t"):
                self.posInFile[1] += 3

            self.pos += 1

            if self.pos > len(self.text) - 1:
                self.reachedEOF = True
                break

            number -= 1

    def getCurrentChars(self, length=1):
        """
        :param length: number of characters from the current position
        :return: current characters from the current position given the length
        """
        return self.text[self.pos: self.pos + length]

    def currentCharsAre(self, chars):
        """
        :param chars: characters provided to compare to the current string
        :return: returns whether the characters provided equal to the current string
        """
        length = len(chars)
        return chars == self.getCurrentChars(length)

    def lock(self):
        """
        Locks the starting position to process a multi-character string

        Note that this doesn't actually lock the pos attribute.
        """

        # if not originally locked, does normal thing
        if not self.locked:
            self.locked = True
            self.lockedPos = self.pos
            self.lockedPosInFile = self.posInFile[:]  # slicing to clone the list
        else:  # otherwise, warning
            logging.warning("Unexpected lock before unlock at " + self.getPosRepr())

    def getLockStr(self):
        return self.text[self.lockedPos: self.pos]

    def unlock(self):
        self.locked = False
        self.lockedPos = None
        self.lockedPosInFile = None

    def skipWhitespace(self):
        while not self.reachedEOF and self.getCurrentChars().isspace() and not self.currentCharsAre("\n"):
            self.advance()

    def skipComment(self):
        while not self.reachedEOF and not self.currentCharsAre(NEWLINE[VALUE]):
            self.advance()

    def getDedents(self, dedents):
        """
        always adds a newline after for better processing

        :param dedents: number of dedent tokens gotten
        :return: none
        """

        self.indentLength -= dedents
        for dedent in range(dedents):
            dedentToken = Token(self.getTokenPos(), DEDENT)
            self.storedTokens.put(dedentToken)

    def handleAfterNewline(self):
        if self.currentCharsAre("#"):
            self.skipComment()
            # self.getComment()
            return

        if self.currentCharsAre(STATEMENT[VALUE]):
            statementToken = Token(self.getTokenPos(), STATEMENT)
            self.storedTokens.put(statementToken)

            # advances after '!"
            self.advance()
            self.getPostStmts()
            return

    def getComment(self):
        """
        gets the comment token

        only called when handling indents as that's when newlines are processed
        :return:
        """
        self.lock()
        while not self.reachedEOF and not self.currentCharsAre(NEWLINE[VALUE]):
            self.advance()

        result = self.getLockStr()
        tokenPos = self.getTokenPos()
        self.unlock()

        self.storedTokens.put(Token(tokenPos, COMMENT, result))

    def getPostStmts(self):
        """
        assumes first character is after "!"

        adds relevant tokens to the stored tokens list
        """

        if self.currentCharsAre(PATH[VALUE]):
            # creates new PATH token
            self.storedTokens.put(Token(self.getTokenPos(), PATH))
            self.advance(PATH[VALUE])

        elif self.currentCharsAre(MFUNC[VALUE]):
            # creates new MFUNC token
            self.storedTokens.put(Token(self.getTokenPos(), MFUNC))
            self.advance(MFUNC[VALUE])

        else:
            self.error()

        self.skipWhitespace()

        # gets full path string and stores as string token
        self.lock()
        while not self.reachedEOF and not self.currentCharsAre(NEWLINE[VALUE]):
            self.advance()

        result = self.getLockStr()
        self.storedTokens.put(Token(self.getTokenPos(), STRING, result))

        self.unlock()
        return

    def handleIndents(self):
        """
        handle existing indents, dedents and new lines

        note that this is called when the current character is "\n"
        :return: None, since all tokens created here will be added to the queue
        """

        # newline tokens cannot be put in the beginning because there must be
        # a string detected for a newline to register
        # self.storedTokens.put(newlineToken)
        self.advance()

        # note that index is indentLength-1 to 0
        for index in reversed(range(self.indentLength)):
            if self.currentCharsAre(INDENT[VALUE]):
                self.advance(INDENT[VALUE])
            else:
                # dedents are detected here due to lack of indents
                # however, if the current token is literally a newline, does nothing and immediately breaks
                # this will go back to the beginning of this method, creating a newline token there
                if self.currentCharsAre("\n"):
                    return

                dedents = index+1
                self.getDedents(dedents)

                # adds the newline token here because newline tokens should come after dedent tokens
                newlineToken = Token(self.getTokenPos(), NEWLINE)
                self.storedTokens.put(newlineToken)
                self.handleAfterNewline()
                return

        # if the immediate next character is just a newline, ends
        # this is for when there are no indents avaliable to go to the above
        if self.currentCharsAre("\n"):
            return

        # handle new indents
        newlineToken = Token(self.getTokenPos(), NEWLINE)
        self.storedTokens.put(newlineToken)
        if self.currentCharsAre(INDENT[VALUE]):
            self.indentLength += 1

            indentToken = Token(self.getTokenPos(), INDENT)
            self.storedTokens.put(indentToken)
            self.advance(INDENT[VALUE])

        # if there is additional whitespace after an indent, error
        if self.currentCharsAre(INDENT[VALUE]):
            self.error("Invalid indent")

        # handles newline after indent because indent character will take up its place if not
        self.handleAfterNewline()

    def getNumber(self):
        """Return a (multidigit) integer or float consumed from the input."""
        self.lock()

        if not self.reachedEOF and (self.currentCharsAre("-") or self.getCurrentChars().isdigit):
            self.advance()

        while not self.reachedEOF and self.getCurrentChars().isdigit():
            self.advance()

        if self.currentCharsAre("."):  # indicates it's a float value
            self.advance()

            while not self.reachedEOF and self.getCurrentChars().isdigit():
                self.advance()

            result = self.getLockStr()
            token = Token(self.getTokenPos(), FLOAT, float(result))
        else:
            result = self.getLockStr()
            token = Token(self.getTokenPos(), INT, int(result))

        self.unlock()
        return token

    def getCoord(self):
        """
        gets the coordinate token, as either "~" or "~[number]",
        where number can be an int or float

        :return:
        """

        self.lock()
        self.advance()

        if (not self.reachedEOF) and (self.currentCharsAre("-") or self.getCurrentChars().isdigit()):
            self.advance()

        while not self.reachedEOF and self.getCurrentChars().isdigit():
            self.advance()

        if self.currentCharsAre("."):  # indicates it's a float value
            self.advance()

            while not self.reachedEOF and self.getCurrentChars().isdigit():
                self.advance()

            result = self.getLockStr()
        else:
            result = self.getLockStr()

        token = Token(self.getTokenPos(), COORD, result)
        self.unlock()
        return token

    def getDataTag(self):
        """
        self.brackets represents how many closing brackets are required to escape this method

        initially starts at one because it requires one closing bracket to close
        note it doesn't account for any strings with curly brackets, so gl with that

        :return:
        """
        brackets = 0

        self.lock()
        tokenPos = self.getTokenPos()

        # result here to skip unnecessary whitespace and comments
        result = ""

        while not self.reachedEOF:
            # handles whitespace right after newline and comments within datatags
            if self.currentCharsAre(NEWLINE[VALUE]):
                # adds to result, unlocks, advances (skip whitespace and comment), relocks
                result += self.getLockStr()
                self.unlock()
                self.advance()

                if self.getCurrentChars().isspace():
                    self.skipWhitespace()

                self.handleAfterNewline()
                self.lock()
                continue

            if self.currentCharsAre("{"):
                brackets += 1
            if self.currentCharsAre("}"):
                brackets -= 1
            if brackets == 0:
                self.advance()
                break

            self.advance()

        result += self.getLockStr()

        token = Token(tokenPos, DATATAG, result)
        self.unlock()
        return token

    def getSelector(self):
        """
        Gets the entire selector

        :return: selector token
        """
        self.lock()

        # because all beginning selectors are 2 characters, @x
        self.advance()
        self.advance()

        if self.currentCharsAre("["):
            while not self.reachedEOF and not self.currentCharsAre("]"):
                self.advance()
            self.advance()  # to advance after "["

        result = self.getLockStr()
        token = Token(self.getTokenPos(), SELECTOR, result)
        self.unlock()

        return token

    def getString(self):
        """
        Simply gets the current string until next whitespace

        :return: String token
        """
        self.lock()
        while not self.reachedEOF and not self.getCurrentChars().isspace() and not self.currentCharsAre("\\\n"):
            self.advance()

        result = self.getLockStr()
        tokenPos = self.getTokenPos()
        self.unlock()

        # gets any predefined simple token
        for simpleToken in SIMPLE_TOKENS:
            if result == simpleToken[VALUE]:
                return Token(tokenPos, simpleToken)

        # gets leading commands
        for command in options[LEADING_COMMANDS]:
            if result == command:
                return Token(tokenPos, LEADING_COMMAND, command)

        # gets any command
        for command in options[COMMANDS]:
            if result == command:
                return Token(tokenPos, COMMAND, command)

        return Token(tokenPos, STRING, result)

    def getNextToken(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while not self.reachedEOF:

            # returns any stored tokens
            if not self.storedTokens.empty():
                return self.storedTokens.get()

            # line break when "\" is found at the end of a line lol
            if self.currentCharsAre("\\\n"):
                self.advance(2)
                self.skipWhitespace()
                continue

            # skips all whitespace until \n
            if self.getCurrentChars().isspace() and not self.currentCharsAre("\n"):
                self.skipWhitespace()
                continue

            # handles indents and dedents
            if self.currentCharsAre(NEWLINE[VALUE]):
                # gets either an indent token or dedent token
                # note that the dedent token carries a value of how many dedents happened
                self.handleIndents()
                continue

            # gets a number if the first character is a digit or -DIGIT
            # it gets the first 2 current chars, and gets the second current char to see if it's a digit
            if self.getCurrentChars().isdigit() or (self.currentCharsAre("-") and self.getCurrentChars(2)[1].isdigit()):
                return self.getNumber()

            # gets coordinate
            if self.currentCharsAre("~"):
                return self.getCoord()

            # gets selector
            if self.getCurrentChars(2) in options[SELECTOR_TYPES]:
                return self.getSelector()

            # gets datatag
            if self.currentCharsAre("{"):
                return self.getDataTag()

            return self.getString()

        if self.indentLength > 0:
            self.getDedents(self.indentLength)

        if not self.storedTokens.empty():
            return self.storedTokens.get()

        return Token(self.getTokenPos(), EOF)
