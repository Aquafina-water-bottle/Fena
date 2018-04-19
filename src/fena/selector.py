"""
selector ::= DEFAULT_VAR & ("[" & selectorArgs & "]")?

selectorArgs ::= (singleArg)? | (singleArg & ("," & singleArg))?
singleArg ::= [simpleArg, rangeArg, tagArg]
simpleArg ::= DEFAULT_ARG & "=" & ("!")? & [STRING, INT]

tagArg ::= STRING
rangeArg ::= STRING & ("=" & range)?
range ::= [INTEGER, (INTEGER & ".."), (".." & INTEGER), (INTEGER & ".." & INTEGER)]
"""

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
        self._selector_str = ""

    def build(self, prefix=None):
        """
        Builds so the string representation is made properly
        """
        # lexer = SelectorLexer()
        # parser = SelectorParser()
        # parser.parse()
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
