import os.path
import copy
import logging
from collections import deque
from config_data import ConfigData
from builder import Builder
from token_types import TokenType, SimpleToken

class CommandBuilder(Builder):
    """
    Holds branching simple commands using a builder model
    Args:
        prefix (str): Any prefix to objectives, teams or tags
        constobj (str)
        shortcuts (dict): All function shortcuts present in the file
            Maps function name to the function path

        states (list of strs): Displays the state of the current command builder as:
            "execute", "scoreboard", "function", "simple"

        execute (ExecuteBuilder)
        scoreboard (ScoreboardBuilder)
        function (FunctionBuilder)
        simple (SimpleBuilder)

    """
    config_data = ConfigData()
    prefix = ""
    constobj = ""
    shortcuts = {}

    @classmethod
    def initialize(cls, symbol_table, mcfunctions):
        """
        Sets the prefix, constobj and gets all function shortcuts
        """
        # default for prefix is "fena"
        if symbol_table.prefix is None:
            cls.prefix = "fena"
            logging.warning("Using the default prefix of {}".format(cls.prefix))
        else:
            cls.prefix = symbol_table.prefix
        
        # default for constobj is "constants"
        if symbol_table.constobj is None:
            cls.constobj = "constants"
        else:
            cls.constobj = symbol_table.constobj

        # gets all mcfunction shortcuts
        for mcfunction in mcfunctions:
            CommandBuilder._set_shortcut(mcfunction.path)

    @classmethod
    def _set_shortcut(cls, full_path):
        """
        Gets the function paths all the way until "functions"
        """
        # strips away ".mcfunction"
        path_without_ext, extension = os.path.splitext(full_path)
        name = os.path.basename(path_without_ext)
        assert extension == ".mcfunction"

        # gets the list of all directories including base file without extension
        path_list = os.path.normpath(path_without_ext).split(os.sep)

        # gets all directories of the shortcut including the function name
        # path_list should contain "functions" by the end, or else it will be an empty list
        directories = deque()
        while path_list and path_list[-1] != "functions":
            directories.appendleft(path_list.pop())

        if not path_list:
            raise SyntaxError("Path {} must contain a functions/ folder".format(full_path))

        if len(directories) <= 1:
            raise SyntaxError("Path {} must have a folder inside the functions/ folder".format(full_path))

        shortcut = directories.popleft() + ":"
        shortcut += "/".join(directories)

        cls.shortcuts[name] = shortcut

    def __init__(self):
        self.state = "execute"
        self.commands = []
        self._execute = None
        self._scoreboard = None
        self._function = None
        self._simple = None

        # self.execute = ExecuteBuilder()
        # self.scoreboard = ScoreboardBuilder()
        # self.function = FunctionBuilder()
        # self.simple = SimpleBuilder()

    @property
    def execute(self):
        if self._execute is None:
            self._execute = ExecuteBuilder()
        return self._execute

    @property
    def scoreboard(self):
        if self._scoreboard is None:
            self._scoreboard = ScoreboardBuilder()
        return self._scoreboard

    @property
    def function(self):
        if self._function is None:
            self._function = FunctionBuilder()
        return self._function

    @property
    def simple(self):
        if self._simple is None:
            self._simple = SimpleBuilder()
        return self._simple

    def copy(self):
        return copy.deepcopy(self)

    def build(self):
        """
        Builds itself so the string representation can be used
        """
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass

class ExecuteSlice:
    def __init__(self, token, execute_type):
        if execute_type == "as":
            assert token.matches(TokenType.SELECTOR)
        elif execute_type == "pos":
            assert token.matches(TokenType.COORDS)
        elif execute_type == "if":
            assert token.matches(TokenType.DETECT)
        elif execute_type is None:
            assert token is None
        else:
            raise SyntaxError("Invalid execute type of {}".format(repr(execute_type)))

        self.token = token
        self.type = execute_type

    @classmethod
    def empty(cls):
        return cls(None, None)

    def is_empty(self):
        return self.token is None and self.type is None

    def __str__(self):
        return "[token={}, type={}]".format(self.token, self.type)

    def __repr__(self):
        return "ExecuteSlice[token={}, type={}]".format(repr(self.token), repr(self.type))
        
class ExecuteBuilder(Builder):
    """
    Examples:
        >>> from token_position import TokenPosition
        >>> from lexical_token import Token
        >>> from token_types import TokenType
        >>> pos = TokenPosition(row=5, column=5, char_pos=5)

        >>> selector = Token(pos=pos, token_type=TokenType.SELECTOR, value="@a[tag=rr.ti]")
        >>> coords = Token(pos=pos, token_type=TokenType.COORDS, value="~ ~5 ~")
        >>> detect = Token(pos=pos, token_type=TokenType.DETECT, value="~ ~1 ~ stonebrick *")
        >>> detect2 = Token(pos=pos, token_type=TokenType.DETECT, value="~ ~2 ~ dirt 0")

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.add(selector)
        >>> execute_builder.add(coords, execute_type="pos")
        >>> execute_builder.build()
        'execute @a[tag=rr.ti] ~ ~5 ~'

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.add(selector)
        >>> execute_builder.add(coords, execute_type="pos")
        >>> execute_builder.add(coords, execute_type="pos")
        >>> execute_builder.build()
        Traceback (most recent call last):
            ...
        SyntaxError: Token['~ ~5 ~' at [row=5, col=5]]: Requires the beginning of an execute command to be a selector

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.build()
        Traceback (most recent call last):
            ...
        AssertionError: Empty builder

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.add(coords, execute_type="pos")
        >>> execute_builder.build()
        Traceback (most recent call last):
            ...
        SyntaxError: Token['~ ~5 ~' at [row=5, col=5]]: Requires the beginning of an execute command to be a selector

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.add(selector)
        >>> execute_builder.build()
        'execute @a[tag=rr.ti] ~ ~ ~'

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.add(selector)
        >>> execute_builder.add(detect, "if")
        >>> execute_builder.build()
        'execute @a[tag=rr.ti] ~ ~ ~ detect ~ ~1 ~ stonebrick *'

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.add(selector)
        >>> execute_builder.add(coords, "pos")
        >>> execute_builder.add(detect, "if")
        >>> execute_builder.build()
        'execute @a[tag=rr.ti] ~ ~5 ~ detect ~ ~1 ~ stonebrick *'

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.add(selector)
        >>> execute_builder.add(detect, "if")
        >>> execute_builder.add(detect2, "if")
        >>> execute_builder.build()
        'execute @a[tag=rr.ti] ~ ~ ~ detect ~ ~1 ~ stonebrick * execute @s ~ ~ ~ detect ~ ~2 ~ dirt 0'

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.add(selector)
        >>> execute_builder.add(coords, "pos")
        >>> execute_builder.add(detect, "if")
        >>> execute_builder.add(detect2, "if")
        >>> execute_builder.build()
        'execute @a[tag=rr.ti] ~ ~5 ~ detect ~ ~1 ~ stonebrick * execute @s ~ ~5 ~ detect ~ ~2 ~ dirt 0'

        >>> execute_builder = ExecuteBuilder()
        >>> execute_builder.add(detect, "if")
        >>> execute_builder.build()
        Traceback (most recent call last):
            ...
        SyntaxError: Token['~ ~1 ~ stonebrick *' at [row=5, col=5]]: Requires the beginning of an execute command to be a selector
    """
    def __init__(self):
        self.type = "as"
        self.slices = deque()
        self._execute_slice = ExecuteSlice.empty()

    def add(self, token, execute_type=None):
        """
        Args:
            token (Token)
            execute_type (str or None)
        """
        if execute_type is None:
            execute_type = self.type

        execute_slice = ExecuteSlice(token, execute_type)
        self.slices.append(execute_slice)

    def build(self):
        assert self.slices, "Empty builder"
        return self._execute_cmd()

    def _advance(self):
        """
        Returns:
            str: The previous token's value
        """
        if self._execute_slice.is_empty():
            raise SyntaxError("Should not advance if it is empty")
        previous_value = self._execute_slice.token.value

        if self.slices:
            self._execute_slice = self.slices.popleft()
        else:
            self._execute_slice = ExecuteSlice.empty()

        return previous_value

    def _execute_cmd(self):
        """
        execute_builder_cmd ::= SELECTOR && (COORDS)? && (DETECT)* && execute_builder_cmd
        """
        # gets the first command slice
        self._execute_slice = self.slices.popleft()
        string_builder = []

        while not self._execute_slice.is_empty():
            # SELECTOR
            if self._execute_slice.type != "as":
                raise SyntaxError("{}: Requires the beginning of an execute command to be a selector".format(self._execute_slice.token))
            selector_str = self._advance()
            
            # (COORDS)?
            if self._execute_slice.type == "pos":
                coords_str = self._advance()
            else:
                coords_str = "~ ~ ~"

            execute_begin_str = "execute {selector} {coords}".format(selector=selector_str, coords=coords_str)

            # (DETECT)*
            if self._execute_slice.type == "if":
                while True:
                    if not self._execute_slice.token.matches(TokenType.DETECT):
                        raise SyntaxError("{}: Requires the beginning of an if shortcut to be a block".format(self._execute_slice.token))
                    detect_str = self._advance()

                    string_builder.append("{execute} detect {detect}".format(execute=execute_begin_str, detect=detect_str))

                    if self._execute_slice.type != "if":
                        break

                    execute_begin_str = "execute @s {coords}".format(coords=coords_str)
            else:
                # No DETECT was found
                string_builder.append(execute_begin_str)
        
        return " ".join(string_builder)

class ScoreboardBuilder(Builder):
    valid_types = {"players_math", # "players_set", "players_add", "players_remove", "players_test",
                   "players_special", # "players_reset", "players_enable",
                   "teams", # "teams_join", "teams_empty", "teams_leave"
                   "tags", # "tag_add", "tag_remove"
                   "players_op" # "players_op_const", "players_op_objective"
                   }

    def __init__(self, scoreboard_type=None):
        if scoreboard_type is None:
            self._type = None
        else:
            self.type = scoreboard_type
        self.child_builder = None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, scoreboard_type):
        assert scoreboard_type in ScoreboardBuilder.valid_types, "Invalid type {}".format(repr(scoreboard_type))
        self._type = scoreboard_type

    def add(self, **tokens):
        """
        Args:
            tokens (tuple of Token objects)
        """
        assert self.type is not None, "{}: Cannot have a scoreboard builder with type as None".format(repr(self))
        assert self.child_builder is None, "Cannot add another child builder"

        # if self.type ==

    def build(self):
        assert self.type is not None
        return self.child_builder.build()

    def __repr__(self):
        return "ScoreboardBuilder[type={}, child_builder={}]".format(self.type, self.child_builder)

class FunctionBuilder(Builder):
    def __init__(self):
        self.path_shortcut = None

    def build(self):
        pass

class SimpleBuilder(Builder):
    def __init__(self):
        self.tokens = []

    def build(self):
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # from token_position import TokenPosition
    # from lexical_token import Token
    # from token_types import TokenType, ExecuteShortToken, SimpleToken

    # pos = TokenPosition(row=5, column=5, char_pos=5)

    # selector = Token(pos=pos, token_type=TokenType.SELECTOR, value="@a[tag=rr.ti]")
    # coords = Token(pos=pos, token_type=TokenType.COORDS, value="~ ~5 ~")
    # block = Token(pos=pos, token_type=TokenType.DETECT, value="stonebrick *")

    # execute_builder = ExecuteBuilder()
    # execute_builder.add(selector)
    # execute_builder.add(block, "if")
    # print(execute_builder.build())