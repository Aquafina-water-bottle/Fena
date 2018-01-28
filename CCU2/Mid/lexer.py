import logging
from queue import Queue

from Mid.constants import *
from Common.lexicalToken import *


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

    def skipLineComment(self):
        """anything between "//" and "\n" is removed"""
        while not self.reachedEOF and not self.currentCharsAre("\n"):
            self.advance()
        
    def skipBlockComment(self):
        """anything between /* and */ is removed"""
        while not self.reachedEOF and not self.currentCharsAre(COMMENT_END[VALUE]):
            self.advance()
        self.advance(COMMENT_END[VALUE])

    def getDedents(self, dedents):
        """

        :param dedents: number of dedent tokens gotten
        :return: none
        """
        self.indentLength -= dedents
        for dedent in range(dedents):
            dedentToken = Token(self.getTokenPos(), DEDENT)
            self.storedTokens.put(dedentToken)

    def handleIndents(self):
        """
        handle existing indents, dedents and new lines

        note that this is called when the current character is "\n"
        :return: None, since all tokens created here will be added to the queue
        """

        newlineToken = Token(self.getTokenPos(), NEWLINE)
        self.storedTokens.put(newlineToken)
        self.advance()

        # note that index is indentLength-1 to 0
        for index in reversed(range(self.indentLength)):
            if self.currentCharsAre(TAB_INDENT):
                self.advance(TAB_INDENT)
            else:
                # dedents are detected here due to lack of indents
                # however, if the current token is literally a newline, does nothing and immediately breaks
                # this will go back to the beginning of this method, creating a newline token there
                if self.currentCharsAre("\n"):
                    return

                dedents = index+1
                self.getDedents(dedents)
                return

        # handle new indents
        if self.currentCharsAre(TAB_INDENT):
            self.indentLength += 1

            indentToken = Token(self.getTokenPos(), INDENT)
            self.storedTokens.put(indentToken)
            self.advance(TAB_INDENT)

        # if there is additional whitespace after an indent, error
        if self.currentCharsAre(TAB_INDENT):
            self.error("Invalid indent")

    def getNumber(self):
        """Return a (multidigit) integer or float consumed from the input."""
        self.lock()

        while not self.reachedEOF and self.getCurrentChars().isdigit():
            self.advance()

        if self.currentCharsAre("."):  # indicates it's a float value
            self.advance()

            while not self.reachedEOF and self.getCurrentChars().isdigit():
                self.advance()

            result = self.getLockStr()
            token = Token(self.getTokenPos(), FLOAT_LITERAL, float(result))
        else:
            result = self.getLockStr()
            token = Token(self.getTokenPos(), INT_LITERAL, int(result))

        self.unlock()
        return token

    def getIdentifier(self):
        """Handle identifiers and reserved keywords"""
        self.lock()
        while not self.reachedEOF and self.getCurrentChars().isalnum():
            self.advance()

        result = self.getLockStr()

        # if the reserved keyword is used, it is gotten
        # otherwise, it's an identifier
        token = None
        for keyword in ALL_KEYWORDS:
            if result == keyword[VALUE]:
                token = Token(self.getTokenPos(), keyword)
                break
        if token is None:
            token = Token(self.getTokenPos(), IDENTIFIER, result)
        self.unlock()
        return token

    def getNextToken(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while not self.reachedEOF:

            if not self.storedTokens.empty():
                return self.storedTokens.get()

            # skips all whitespace until \n
            if self.getCurrentChars().isspace() and not self.currentCharsAre("\n"):
                self.skipWhitespace()
                continue
            
            # handles indents and dedents
            if self.currentCharsAre("\n"):
                # gets either an indent token or dedent token
                # note that the dedent token carries a value of how many dedents happened
                self.handleIndents()
                continue
            
            # skips /* block comment */
            if self.currentCharsAre(COMMENT_START[VALUE]):
                self.advance(COMMENT_START[VALUE])
                self.skipBlockComment()
                continue
            
            # skips // line comment
            if self.currentCharsAre(LINE_COMMENT[VALUE]):
                self.advance(LINE_COMMENT[VALUE])
                self.skipLineComment()
                continue
            
            # gets an identifier if the first character is within the alphabet
            if self.getCurrentChars().isalpha():
                return self.getIdentifier()
            
            # gets a number if the first character is a digit
            if self.getCurrentChars().isdigit():
                return self.getNumber()
            
            # gets any predefined operator token
            for operator in OPERATORS:
                if self.currentCharsAre(operator[VALUE]):
                    tokenPos = self.getTokenPos()
                    self.advance(operator[VALUE])
                    return Token(tokenPos, operator)
                
            # gets any predefined delimiter token
            for delimiter in DELIMITERS:
                if self.currentCharsAre(delimiter[VALUE]):
                    tokenPos = self.getTokenPos()
                    self.advance(delimiter[VALUE])
                    return Token(tokenPos, delimiter)

            self.error()

        if self.indentLength > 0:
            self.getDedents(self.indentLength)

        if not self.storedTokens.empty():
            return self.storedTokens.get()

        return Token(EOF, self.getTokenPos())
