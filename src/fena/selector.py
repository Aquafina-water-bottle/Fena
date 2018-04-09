"""
selector ::= DEFAULT_VAR & ("[" & selectorArgs & "]")?

selectorArgs ::= (singleArg)? | (singleArg & ("," & singleArg))?
singleArg ::= [simpleArg, rangeArg, tagArg]
simpleArg ::= DEFAULT_ARG & "=" & ("!")? & [STRING, INT]

tagArg ::= STRING
rangeArg ::= STRING & ("=" & range)?
range ::= [INTEGER, (INTEGER & ".."), (".." & INTEGER), (INTEGER & ".." & INTEGER)]
"""

# """
# A module for getting the selector shortcut from a selector token
# 
# This contains its own miniature lexer and interpreter to make
# error reporting and changing easier
# """
# 
# import logging
# 
# from lexicalToken import Token
# from config_data import options
# from constants import SELECTOR_TYPES, SELECTOR_VARIABLES
# 
# SELECTOR_TYPE = "selector type"
# SELECTOR_VAR = "selector variable"
# STRING = "string"
# INTEGER = "integer"
# 
# TYPE, VALUE = 0, 1
# OPEN_BRACKET = ("open bracket", "[")
# CLOSE_BRACKET = ("close bracket", "]")
# EQUALS = ("equals", "=")
# NOT = ("not", "!")
# RANGE = ("range", "..")
# COMMA = ("comma", ",")
# SIMPLE_TOKENS = (OPEN_BRACKET, CLOSE_BRACKET, EQUALS, NOT, RANGE, COMMA)
# 
# END = ("end", "end")
# 
# selectorVarShort = {
#     "limit": "c",
#     "gamemode": "m",
# }
# 
# selectorRangeShort = {
#     "dist": "distance",
#     "lvl": "level",
#     "x_rot": "x_rotation",
#     "y_rot": "y_rotation",
# }
# 
# selectorRangeLookup = {
#     "distance": ("rm", "r"),
#     "level": ("l", "lm"),
#     "x_rotation": ("rx", "rxm"),
#     "y_rotation": ("ry", "rym"),
# }
# 
# 
# class Lexer:
#     """
#     Miniature lexer for getting tokens for a selector
# 
#     Converts them into simple strings, separated into:
#         '[' as open bracket
#         ']' as close bracket
#         '..' as range
#         '=' as equal
# 
#         '@e', '@s', '@r', '@p', '@a' as type
#         'lvl', 'c', 'objective', ... as strings
#         '-5', '4', '0', ... as integers
#     """
# 
#     def __init__(self):
#         self.selector = None
#         self.pos = 0
#         self.posDisp = None
#         self.reachedEnd = False
# 
#     def setSelector(self, selector, posDisp):
#         self.selector = selector
#         self.pos = 0
#         self.posDisp = list(posDisp)
#         self.reachedEnd = False
# 
#     def getCurrentChars(self, length=1):
#         """
#         Args:
#             length (int, optional) number of characters from the current position
# 
#         Returns:
#             int: current characters from the current position given the length
#         """
#         return self.selector[self.pos: self.pos + length]
# 
#     def getPosRepr(self):
#         line, column = self.posDisp
#         return "Line {0} column {1}: ".format(line, column)
# 
#     def getTokenPos(self):
#         """
#         Note that this should only be used for creating tokens
# 
#         Returns:
#             tuple (int, int): position of the token
#         """
#         return tuple(self.posDisp)
# 
#     def advance(self, increment=1):
#         while increment > 0:
#             self.pos += 1
#             self.posDisp[1] += 1
# 
#             if self.pos > len(self.selector) - 1:
#                 self.reachedEnd = True
#                 break
# 
#             increment -= 1
# 
#     def getTokenList(self):
#         tokenList = []
#         while not self.reachedEnd:
#             token = self.getNextToken()
#             tokenList.append(token)
# 
#         return tokenList
# 
#     def getInteger(self):
#         result = ""
#         tokenPos = self.getTokenPos()
# 
#         if self.getCurrentChars() == "-":
#             result = "-"
#             self.advance()
#         
#         while not self.reachedEnd and self.getCurrentChars().isdigit():
#             result += self.getCurrentChars()
#             self.advance()
# 
#         return Token(tokenPos, INTEGER, int(result))
# 
#     def getString(self):
#         result = ""
#         tokenPos = self.getTokenPos()
# 
#         while not self.reachedEnd and (self.getCurrentChars().isalpha() or self.getCurrentChars().isdigit() or self.getCurrentChars() == "_"):
#             result += self.getCurrentChars()
#             self.advance()
# 
#         for selectorVar in options[SELECTOR_VARIABLES]:
#             if result == selectorVar:
#                 return Token(tokenPos, SELECTOR_VAR, selectorVar)
# 
#         return Token(tokenPos, STRING, result)
#     
#     def getNextToken(self):
#         if self.reachedEnd:
#             return Token(self.getTokenPos(), END)
# 
#         for token in SIMPLE_TOKENS:
#             if self.getCurrentChars(len(token[VALUE])) == token[VALUE]:
#                 tokenPos = self.getTokenPos()
#                 self.advance(len(token[VALUE]))
#                 return Token(tokenPos, token)
# 
#         if self.getCurrentChars(2) in options[SELECTOR_TYPES]:
#             tokenPos = self.getTokenPos()
#             selectorType = self.getCurrentChars(2)
#             self.advance(2)
#             return Token(tokenPos, SELECTOR_TYPE, selectorType)
# 
#         if self.getCurrentChars().isdigit() or self.getCurrentChars() == "-":
#             return self.getInteger()
# 
#         if self.getCurrentChars().isalpha() or self.getCurrentChars() == "_":
#             return self.getString()
# 
#         raise SyntaxError(self.getPosRepr() + "Invalid character {0}".format(repr(self.getCurrentChars())))
# 
# 
# 
# class Interpreter:
#     """
# 
#     Attributes:
#         selectorStr (str): The full selector shortcut string conversion
#         lexer (Lexer)
#         currentToken (Token)
#     """
# 
#     def __init__(self, lexer):
#         self.selectorStr = ""
#         self.lexer = lexer
#         self.currentToken = None
# 
#     def setSelector(self, selector, posDisp):
#         self.lexer.setSelector(selector, posDisp)
#         self.selectorStr = ""
#         self.currentToken = None
#         self.advance()
# 
#     def advance(self):
#         self.currentToken = self.lexer.getNextToken()
#         logging.debug("Advanced to selector {}".format(self.currentToken))
# 
#     def eat(self, *types, addToStr=False):
#         if self.currentToken.matchesOne(*types):
#             if addToStr:
#                 self.selectorStr += self.currentToken.value
# 
#             eatenToken = self.currentToken
#             self.advance()
# 
#             return eatenToken
#         else:
#             self.error("Invalid type while eating")
# 
#     def error(self, message, token=None):
#         if token is None:
#             logging.error("Error during selector shortcut creation at {0}: {1}".format(self.currentToken, message))
#         else:
#             logging.error("Error during selector shortcut creation at {0}: {1}".format(token, message))
#         raise SyntaxError
# 
#     def interpret(self, selector, posDisp):
#         """
#         selector ::= SELECTOR_TYPE & ("[" & selectorArgs & "]")?
#         """
#         self.setSelector(selector, posDisp)
#         
#         # expects a selector type always at first
#         self.eat(SELECTOR_TYPE, addToStr=True)
# 
#         if self.currentToken.matches(OPEN_BRACKET):
#             self.eat(OPEN_BRACKET, addToStr=True)
#             self.selectorArgs()
#             self.eat(CLOSE_BRACKET, addToStr=True)
# 
#         if not self.currentToken.matches(END):
#             self.error("Expected end of selector")
# 
#         return self.selectorStr
# 
#     def selectorArgs(self):
#         """
#         selectorArgs ::= (singleArg)? | (singleArg & ("," & singleArg))?
#         """
#         if not self.currentToken.matches(CLOSE_BRACKET):
#             self.singleArg()
# 
#         while not self.currentToken.matches(CLOSE_BRACKET):
#             self.eat(COMMA, addToStr=True)
#             self.singleArg()
# 
#     def singleArg(self):
#         """
#         singleArg ::= [simpleArg, rangeArg, tagArg]
#         """
#         if self.currentToken.matches(SELECTOR_VAR) or self.currentToken.value in selectorVarShort:
#             self.simpleArg()
#         elif self.currentToken.matches(STRING):
#             self.rangeArg()
#         elif self.currentToken.matches(NOT):
#             self.eat(NOT)
#             selectorStr = self.eat(STRING).value
#             self.tagArg(selectorStr, negate=True)
#         else:
#             self.error("Invalid token, expected a selector var or string")
# 
#     def simpleArg(self):
#         """
#         simpleArg ::= defaultVar & "=" & ("!")? & [STRING, INT]
#         """
# 
#         selectorVarStr = self.eat(SELECTOR_VAR, STRING).value
#         valueStr = ""
# 
#         # gets the shortcut version if it exists
#         selectorVarStr = selectorVarShort.get(selectorVarStr, selectorVarStr)
#         self.eat(EQUALS)
# 
#         # checks for "!"
#         if self.currentToken.matches(NOT):
#             self.eat(NOT)
#             valueStr += NOT[VALUE]
# 
#         # it can be either a string or integer, but not a range
#         valueStr += str(self.eat(STRING, INTEGER).value)
#         self.selectorStr += "{0}={1}".format(selectorVarStr, valueStr)
# 
#     def rangeArg(self):
#         """
#         rangeArg ::= STRING & ("=" & range)?
#         """
#         selectorVar = self.eat(STRING)
# 
#         if self.currentToken.matches(EQUALS):
#             self.eat(EQUALS)
#             self.range(selectorVar)
# 
#         else:
#             self.tagArg(selectorVar.value)
# 
#     def tagArg(self, tag, negate=False):
#         if negate:
#             self.selectorStr += "tag=!{}".format(tag)
#         else:
#             self.selectorStr += "tag={}".format(tag)
# 
#     def range(self, selectorVar):
#         """
#         range ::= [INTEGER, (INTEGER & ".."), (".." & INTEGER), (INTEGER & ".." & INTEGER)]
# 
#         Args:
#             selectorVar (Token)
#         """
#         # min within "min..max"
#         minToken = None
#         maxToken = None
# 
#         # whether the ".." actually exists or not
# 
#         if self.currentToken.matches(INTEGER):
#             minToken = self.eat(INTEGER)
#         if not self.currentToken.matches(RANGE):
#             maxToken = minToken
#         else:
#             self.eat(RANGE)
#             if self.currentToken.matches(INTEGER):
#                 maxToken = self.eat(INTEGER)
# 
#         # if both min and max are none, raises error since that shouldn't happen
#         if (minToken, maxToken).count(None) == 2:
#             self.error("Range has no integers")
# 
#         self.useRange(selectorVar, minToken, maxToken)
# 
#     def useRange(self, selectorVar, minToken, maxToken):
#         """
#         Converts the range to a string
# 
#         Args:
#             selectorVar (str)
#             minToken (Token or None)
#             maxToken (Token or None)
#         """
# 
#         # holds all var=value
#         argList = []
# 
#         # gets the shortcut version if it exists
#         selectorVarStr = selectorRangeShort.get(selectorVar.value, selectorVar.value)
# 
#         # checks whether the beginning and ending variables should be different
#         # due to conversion back to 1.12
#         begVar, endVar = selectorRangeLookup.get(selectorVarStr, ("score_{}_min".format(selectorVarStr), "score_{}".format(selectorVarStr)))
#         if minToken is not None:
#             argList.append(begVar + "=" + str(minToken.value))
# 
#         if maxToken is not None:
#             argList.append(endVar + "=" + str(maxToken.value))
# 
#         self.selectorStr += ",".join(argList)
# 
# 
# LEXER = Lexer()
# INTERPRETER = Interpreter(LEXER)
# def getSelector(selectorToken):
#     selector = selectorToken.value
#     pos = selectorToken.pos
#     return INTERPRETER.interpret(selector, pos)

import logging

class Selector:
    arg_shortcut = {
        "limit": "c",
        "gamemode": "m",
    }

    range_arg_shortcut = {
        "dist": "distance",
        "lvl": "level",
        "x_rot": "x_rotation",
        "y_rot": "y_rotation",
    }

    range_arg_downgrade = {
        "distance": ("rm", "r"),
        "level": ("l", "lm"),
        "x_rotation": ("rx", "rxm"),
        "y_rotation": ("ry", "rym"),
    }

    def __init__(self, tokens):
        """
        Attributes:
            tokens (List of Tokens): Contains all tokens for the selector
            selector_variable (str): Contains the selector variable
            default_selector_arguments (dict mapping strs to strs)
            objective_selector_arguments (dict mapping strs to ints)
            tag_selector_arguments (set of strs): The tags that can be held in the selector
                Currently, it only allows one object in the set since it is 1.12 It will be changed for 1.13.
            _selector_str (str): String representation of the selector which is made once build() is ran
        """
        self.tokens = tokens
        self.selector_variable = ""
        self.default_selector_arguments = {}
        self.objective_selector_arguments = {}

        self.tag_selector_arguments = set()
        # self.tag_selector_arguments = None
        self._selector_str = ""

    def build(self, prefix=None):
        """
        Builds so the string representation is made properly
        """
        pass

    def _add_default(self, default, value):
        """
        Args:
            default (Token): Default target selector argument
            value (Token): Selection criteria relating to the argument
        """
        pass

    def _add_objective(self, objective, value):
        """
        Args:
            objective (Token): Target selector argument as a scoreboard objective
            value (Token): Selection criteria relating to the argument
        """
        pass
    
    def _add_tag(self, tag, negated=False):
        """
        Args:
            tag (Token): Target selector argument as a scoreboard tag
            negated (bool): Whether the tag token was negated or not
        """
        if self.tag_selector_arguments:
            raise SyntaxError("There cannot be more than one tag in a selector ('{}' conflicts with '{}')".format(tag, self.tag_selector_arguments))
        negated_str = ("!" if negated else "")
        self.tag_selector_arguments.add(negated_str + tag.value)

    def __str__(self):
        # return self._selector_str
        return "".join(str(token.value) for token in self.tokens)

    def __repr__(self):
        return "Selector[selector_variable={}, selector_args=(default={}, objectives={}, tags={}), tokens={}]".format(
            repr(self.selector_variable), self.default_selector_arguments, self.objective_selector_arguments, self.tag_selector_arguments, self.tokens)
