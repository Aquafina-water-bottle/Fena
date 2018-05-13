if __name__ == "__main__":
    import logging_setup

import os
import logging

from lexical_token import Token
from token_classes import SimpleToken, WhitespaceSimpleToken, StatementSimpleToken, SelectorSimpleToken, ExecuteSimpleToken
from token_classes import TypedToken, SelectorTypedToken, TokenValues
from token_classes import ALL_TYPED_TOKEN_TYPES
from nodes import ProgramNode, McFunctionNode, FolderNode, PrefixNode, ConstObjNode, FenaCmdNode
from nodes import ScoreboardCmdMathNode, ScoreboardCmdMathValueNode, ScoreboardCmdSpecialNode, FunctionCmdNode, SimpleCmdNode
from nodes import ExecuteCmdNode, ExecuteSubIfBlockArg, ExecuteSubLegacyArg
from nodes import SelectorNode, SelectorTagArgNode, SelectorScoreArgNode
from nodes import SelectorDefaultArgNode, SelectorDefaultArgValueNode, SelectorDefaultGroupArgValueNode
from nodes import BossbarAddNode, BossbarRemoveNode, BossbarGetNode
from nodes import CoordsNode, Vec3Node, Vec2Node
from node_visitors import NodeBuilder, NodeVisitor
from coord_utils import is_coord_token, are_coords
from config_data import ConfigData
from number_utils import is_signed_int, is_nonneg_int, is_pos_int, is_number

"""
Organizes all lines into their respective mcfunctions

program ::= statement_suite
statement_suite ::= [NEWLINE, (statement, NEWLINE)]*

statement ::= "!" && [folder_stmt, mfunc_stmt, prefix_stmt, constobj_stmt]
folder_stmt ::= "folder" && STR && (NEWLINE)* & INDENT && statement_suite && DEDENT
mfunc_stmt ::= "mfunc" && STR && (NEWLINE)* & INDENT && command_suite && DEDENT
prefix_stmt ::= "prefix" && STR
constobj_stmt ::= "constobj" && STR

command_suite ::= [NEWLINE, (command, NEWLINE)]*
command ::= (execute_cmd)? && [sb_cmd, simple_cmd]
simple_cmd ::= [bossbar_cmd, data_cmd, effect_cmd, function_cmd, tag_cmd, team_cmd, (COMMAND_KEYWORD && (STR)*)]

execute_cmd_1_12 ::= selector && (vec3)? && (exec_sub_if)? && (execute_cmd_1_12)? && ":"
execute_cmd_1_13 ::= [selector, vec3, exec_sub_cmds]+ && ":"

exec_sub_cmd_keywords ::= ("as", "pos", "at", "facing", "rot", "anchor", "in", "ast", "if", "ifnot", "unless", "result" ,"success")
exec_sub_cmds ::= [rio.rule("exec_sub_" + rule) for (str rule) in exec_sub_cmd_keywords]
for (str rule) in exec_sub_cmd_keywords:
    rule_arg ::= rio.rule("exec_sub_" + rule + "_arg)
    rio.rule("exec_sub_" + "rule") ::= rule && "(" && rule_arg && ("," && rule_arg)* && ")"

exec_sub_as_arg ::= selector
exec_sub_pos_arg ::= vec3

exec_sub_at_arg ::= [exec_sub_at_arg_anchor, exec_sub_at_arg_selctor, exec_sub_at_arg_axes, exec_sub_at_arg_pos]
exec_sub_at_arg_anchor ::= ["feet", "eyes"]
exec_sub_at_arg_selctor ::= selector
exec_sub_at_arg_axes ::= rio.rand.combo("xyz")
exec_sub_at_arg_pos ::= vec3 && vec2

exec_sub_facing_arg ::= [vec3, selector && ("eyes", "feet")?]
exec_sub_rot_arg ::= entity_vec3
exec_sub_anchor_arg ::= ["feet", "eyes"]
exec_sub_in_arg ::= ["overworld", "nether", "end"]
exec_sub_ast_arg ::= selector

exec_sub_if_arg ::= [exec_sub_if_arg_selector, exec_sub_if_arg_block, exec_sub_if_arg_blocks, exec_sub_if_arg_compare, exec_sub_if_arg_range]
exec_sub_if_arg_selector ::= selector
exec_sub_if_arg_block ::= block && (vec3)?
exec_sub_if_arg_blocks ::= vec3 && vec3 && "==" && vec3 && ["all", "masked"]?
exec_sub_if_arg_compare ::= (target)? && STR && ["==", "<", "<=", ">", ">="] && (target && STR) | (INT)
exec_sub_if_arg_range ::= (target)? && STR && in && int_range
exec_sub_ifnot_arg ::= exec_sub_if_arg
exec_sub_unless_arg ::= exec_sub_if_arg

exec_sub_result_arg ::= [exec_sub_result_arg_data, exec_sub_result_arg_score, exec_sub_result_arg_bossbar]
exec_sub_result_arg_data ::= entity_vec3 && STR && (data_type)? && signed_int
exec_sub_result_arg_score ::= selector && STR
exec_sub_result_arg_bossbar ::= STR && ["max", "value"]
exec_sub_success_arg ::= exec_sub_result_arg 

sb_cmd ::= [sb_players_math, sb_players_special]
sb_players_math ::= target && STR && ["=", "<=", ">=", "swap", "+=", "-=", "*=", "/=", "%="] && (signed_int | target && (STR)?)
sb_players_special ::= target && ["enable", "reset", "<-"] && STR

bossbar_cmd ::= "bossbar" && [bossbar_add, bossbar_remove, bossbar_get, bossbar_set]
bossbar_add ::= "add" && STR && [json, STR]?
bossbar_remove ::= "remove" && STR
bossbar_get ::= STR && "<-" && ["max", "value", "players", "visible"]
bossbar_set ::= STR && bossbar_arg && bossbar_arg_value
# bossbar_option_arg, bossbar_option_arg_value are defined in the bossbar_version.json

# bossbar_set ::= [bossbar_set_max, bossbar_set_value, bossbar_set_players, bossbar_set_visible, bossbar_set_color, bossbar_set_style]
# bossbar_set_max ::= STR && "max" && "=" && pos_int
# bossbar_set_value ::= STR && "value" && "=" && nonneg_int
# bossbar_set_players ::= STR && "players" && "=" && selector
# bossbar_set_visible ::= STR && "=" && ["visible", "invisible"]
# bossbar_set_color ::= STR && "color" && "=" && ["white", "pink", "red", "yellow", "green", "blue", "purple"]
# bossbar_set_style ::= STR && "style" && "=" && ["0", "6", "10", "12", "20"]

data_cmd ::= "data" && [data_get, data_merge, data_remove]
data_get ::= entity_vec3 && "<-" && (STR && (signed_int)?)?
data_merge ::= entity_vec3 && "+" && nbt_tag
data_remove ::= entity_vec3 && "-" && STR

effect_cmd ::= "effect" && [effect_give, effect_clear]
effect_clear ::= selector && "-" && ["all", effect_id]
effect_give ::= selector && "+" && effect_id && (pos_int && ((nonneg_int)? && ["true", "false"]? )? )?
# effect_id are defined under effects_version.txt

function_cmd ::= "function" && STR

tag_cmd ::= "tag" && [tag_add, tag_remove]
tag_add ::= selector && "+" && STR
tag_remove ::= selector && "-" && STR

team_cmd ::= "team" && [team_add, team_join, team_leave, team_empty, team_option, team_remove]
team_add ::= "add" && STR && (STR)*
team_join ::= STR && "+" && target
team_leave ::= "leave" && target
team_empty ::= "empty" && STR
team_option ::= STR && json_parse
team_option ::= STR && team_option_arg && "=" && team_option_arg_value
# team_option_arg, team_option_arg_value are defined in the team_options_version.json
team_remove ::= "remove" && STR

selector ::= selector_var & ("[" & selector_args & "]")?
selector_var ::= "@" & selector_var_specifier
# selector_var_specifier is defined under selector_version.json as "selector_variable_specifiers"
selector_args ::= (single_arg)? | (single_arg & ("," & single_arg)*)?
single_arg ::= [simple_arg, score_arg, tag_arg]

simple_arg ::= default_arg & "=" & default_arg_value_group
# default_arg is defined under selector_version.json as "selector_arguments"
default_arg_value_group = ("!")? & (default_arg_value | ("(" && default_arg_values && ")"))
default_arg_values ::= (default_arg_value)? | (single_arg & ("," & single_arg)*)?
# default_arg_value is defined under selector_version.json as "selector_argument_details"
tag_arg ::= STR
score_arg ::= STR & ("=" & int_range)?

nbt_tag ::= pass
json_tag ::= pass

nonneg_int ::= INT  # Z nonneg
signed_int ::= ("-")? && INT  # Z
pos_int ::= INT, ::/= 0  # Z+

float ::= (INT)? && "." && INT  # R, R <= 0
signed_float ::= ("-")? && float  # R

int_range ::= [signed_int, (signed_int & ".."), (".." & signed_int), (signed_int & ".." & signed_int)]
number_range ::= [signed_float, (signed_float & ".."), (".." & signed_float), (signed_float & ".." & signed_float)]

target ::= [selector, STR]
entity_vec3 ::= [selector, vec3]

vec2 ::= coord && coord
vec3 ::= coord && coord && coord
data_type ::= ["byte", "short", "int", "long", "float", "double"]
coord ::= ("^", "~")? & [signed_int, signed_float]
block ::= block_type & ("[" & (block_states)? & "]")? & (nbt_tag)?
"""

class Parser:
    """
    Makes the mcfunction builders while building all datatags and selectors

    Attributes:
        lexer (Lexer)
        symbol_table (ScopedSymbolTable): Stores all symbols acquired dealing with statements and statement scopes
        file_path (str): Main output file path of the mcfunctions
        mcfunctions (list): All mcfunction builders made by the parser
    """

    config_data = ConfigData()
    sb_special_operators = frozenset({"enable", "reset", "<-"})
    sb_math_operators = frozenset({"=", "<=", ">=", "swap", "+=", "-=", "*=", "/=", "%="})
    json_parse_options = frozenset({"bossbar", "team_options", "selector"})

    def __init__(self, lexer, file_path):
        self.iterator = iter(lexer)
        self.current_token = None
        self.advance()

        # self.symbol_table = ScopedSymbolTable()
        # self.in_file_config = InFileConfig()
        # self.file_path = file_path
        # self.mcfunctions = []

    def parse(self):
        """
        Returns:
            ProgramNode: The parse tree parent
        """
        # logging.debug("Original symbol table: {}".format(repr(self.symbol_table)))
        parse_tree = self.program()
        # logging.debug("Final symbol table: {}".format(repr(self.symbol_table)))
        logging.debug("")

        return parse_tree

    def error(self, message=None):
        if message is None:
            message = "Invalid syntax"
        raise SyntaxError("{}: {}".format(self.current_token, message))

    def advance(self):
        """
        Gets the next token from the lexer without checking any type
        """
        previous_token = self.current_token
        self.current_token = next(self.iterator)
        logging.debug("Advanced to {}".format(repr(self.current_token)))
        return previous_token

    def eat(self, *token_types, values=None, value=None, error_message=None):
        """
        Advances given the token type and values match up with the current token

        Args:
            token_types (any token type)
            values (any or None): Any specified value that should exist within the body of a typed token
            error_message (str or None): What the error message should say in case there is a syntax error

        Returns:
            Token: The token that was just 'eaten'

        Raises:
            SyntaxError: if the current token doesn't match any of the given token types or values
        """
        # makes sure that there exists at least one token type
        assert token_types, "Requires at least one token type"
        assert values is None or value is None

        if (self.current_token.matches_any_of(*token_types) and
                (values is None or (self.current_token.value in values)) and
                (value is None or (self.current_token.value == value)) and
                self.current_token.type in ALL_TYPED_TOKEN_TYPES):
            return self.advance()

        if error_message is None:
            if len(token_types) == 1:
                error_message = "Expected {}".format(token_types[0])
            else:
                error_message = "Expected one of {}".format(token_types)

        if values is not None:
            error_message += " with any value from {}".format(values)
        elif value is not None:
            error_message += " with a value of {}".format(value)

        self.error(error_message)

    def json_parse_arg(self, json_type):
        """
        Args:
            json_type (str)

        Returns:
            dict: pass
        """
        assert json_type in Parser.json_parse_options 

        config_data_attr_dict = {
            "bossbar": "bossbar",
            "team_options": "team_options",
            "selector": "selector_argument_details"
        }

        config_data_attr = config_data_attr_dict.get(json_type)
        json_object = getattr(Parser.config_data, config_data_attr)

        if self.current_token.value in json_object:
            token = self.eat(TypedToken.STRING)
            return json_object[token.value]

        self.error("Expected a token inside {}".format(list(json_object)))

    def json_parse_arg_value(self, arg_details):
        """
        Does whatever the parse type is, and uses other string objects depending on the parse type

        "parse_type":
            "VALUES": It has a "values" attribute that should have a containment check on it
                - This might also have a "value_replace" attribute
            "STR": Anything contained inside a string containing [A-Za-z_.-]
            "SIGNED_INT": Any (possibly negative) integer value (Z)
            "POS_INT": Any positive integer value (Z+)
            "NONNEG_INT": Any nonnegatie integer value (Z nonneg)
            "INT_RANGE": Any signed integer around ".." (either one on the LHS, one on the RHS or around both)
            "NUMBER": Any signed integer or signed decimal number
            "NUMBER_RANGE": Any number around ".." (either one on the LHS, one on the RHS or around both)
            "ENTITIES": Matches any entity specified under ``entities``
            "SELECTOR": Matches a selector
            "ADVANCEMENT_GROUP": Special parsing type specifically for advancements
            "SHORTCUT_ERROR": Raises an error because a shortcut should be able to take care of this
        "group": (only for selector arguments)
            "negation": A group with round brackets is possible with a "!" before it
                eg. type=!(pig, armor_stand, player)
        "values": A list of all possible selector argument values
        "value_replace": A dictionary mapping all possible shorthands to the corresponding selector argument value

        Args:
            arg_details (dict)
        """
        parse_type = arg_details["parse_type"]

        # determines if the value is within the group of specified values
        # as long as the replacement dictionary is applied
        if parse_type == "VALUES":
            arg_value = self.current_token.value
            assert "values" in arg_details, "If the parse type is 'VALUES', a 'values' list must be present in the json"
            valid_values = arg_details["values"]

            # checks whether there are any values that have to be replaced
            if "value_replace" in arg_details:
                replacement_values = arg_details["value_replace"]
                arg_value = replacement_values.get(arg_value, arg_value)

            # checks if the arg value is actually in the default given "values"
            if arg_value not in arg_details["values"]:
                if "value_replace" in arg_details:
                    self.error(f"Expected one of {valid_values} if shorthands are {replacement_values})")
                self.error(f"Expected one of {valid_values})")

            arg_value_token = self.eat(TypedToken.STRING)
            arg_value_token.replacement = arg_value
            return arg_value_token

        # the value can be literally one of anything
        if parse_type == "STR":
            return self.eat(TypedToken.STRING)

        # requires a form of integer, and then stored as an integer
        if parse_type == "SIGNED_INT":
            return self.signed_int()

        if parse_type == "POS_INT":
            return self.pos_int()

        if parse_type == "NONNEG_INT":
            return self.nonneg_int()

        # requires an integer or floating point value
        # note that this doesn't convert it into a float to prevent loss in precision
        if parse_type == "NUMBER":
            arg_value = self.current_token.value
            if not is_number(arg_value):
                self.error("Expected a real number (sadly, no complex numbers are allowed in minecraft)")
            arg_value_token = self.eat(TypedToken.STRING)
            arg_value_token.cast(TypedToken.FLOAT)
            return arg_value_token

        if parse_type == "INT_RANGE":
            return self.int_range()

        if parse_type == "NUMBER_RANGE":
            return self.number_range()

        # checks if the value is a valid entity, and then returns it as a string token
        if parse_type == "ENTITIES":
            arg_value = self.current_token.value
            if arg_value not in Parser.config_data.entities:
                self.error("Expected an entity type")
            return self.eat(TypedToken.STRING)

        if parse_type == "SELECTOR":
            return self.selector()

        if parse_type == "ADVANCEMENT_GROUP":
            raise NotImplementedError 

        if parse_type == "SHORTCUT_ERROR":
            self.error("Shortcut error (There is most likely a shortcut version of this that should be used)")

        self.error("Unknown default value")

    def program(self):
        """
        program ::= (statement)*

        Returns:
            ProgramNode: The parse tree parent
        """
        logging.debug("Begin program at {}".format(repr(self.current_token)))
        statement_nodes = self.statement_suite()
        logging.debug("End program at {}".format(repr(self.current_token)))

        program = ProgramNode(statement_nodes)
        return program

    def statement_suite(self):
        """
        statement_suite ::= [NEWLINE, (statement, NEWLINE)]*

        Returns:
            list of McFunctionNode, FolderNode, PrefixNode, ConstObjNode objects
        """
        logging.debug("Begin statement compound at {}".format(repr(self.current_token)))
        # logging.debug("with scoped symbol table = {}".format(repr(self.symbol_table)))

        statement_nodes = []

        # note that this is essentially a do-while since it never starts out as a newline
        while self.current_token.matches_any_of(WhitespaceSimpleToken.NEWLINE, StatementSimpleToken.STATEMENT_SPECIFIER):
            # base case is if a newline is not met
            if self.current_token.matches(WhitespaceSimpleToken.NEWLINE):
                self.eat(WhitespaceSimpleToken.NEWLINE)

            elif self.current_token.matches(StatementSimpleToken.STATEMENT_SPECIFIER):
                statement_node = self.statement()
                statement_nodes.append(statement_node)

            else:
                self.error("Expected a newline or statement specifier")

        logging.debug("End statement compound at {}".format(repr(self.current_token)))

        return statement_nodes

    def command_suite(self):
        """
        command_suite ::= [NEWLINE, (command, NEWLINE)]*

        Returns:
            list of FenaCmdNode objects
        """
        logging.debug("Begin command compound at {}".format(repr(self.current_token)))
        # logging.debug("with scoped symbol table = {}".format(repr(self.symbol_table)))

        command_nodes = []

        # note that this is essentially a do-while since it never starts out as a newline
        while self.current_token.matches_any_of(WhitespaceSimpleToken.NEWLINE, TypedToken.STRING, SelectorSimpleToken.BEGIN):
            # base case is if a newline is not met
            if self.current_token.matches(WhitespaceSimpleToken.NEWLINE):
                self.eat(WhitespaceSimpleToken.NEWLINE)

            elif self.current_token.matches_any_of(TypedToken.STRING, SelectorSimpleToken.BEGIN):
                command_node = self.command()
                command_nodes.append(command_node)

            else:
                self.error("Expected a newline, command or statement specifier")

        logging.debug("End command compound at {}".format(repr(self.current_token)))

        return command_nodes

    def statement(self):
        """
        Handles any post-processor statements

        statement ::= "!" && [folder_stmt, mfunc_stmt, prefix_stmt, constobj_stmt]

        Returns:
            McFunctionNode: if the statement was the beginning of a mcfunction declaration
            FolderNode: if the statement was a folder declaration
            PrefixNode: if the statement was a prefix statement
            ConstObjNode: if the statement was a constobj statement
        """
        # all here should start with "!"
        self.eat(StatementSimpleToken.STATEMENT_SPECIFIER)

        if self.current_token.matches(StatementSimpleToken.MFUNC):
            return self.mfunc_stmt()
        if self.current_token.matches(StatementSimpleToken.FOLDER):
            return self.folder_stmt()
        if self.current_token.matches(StatementSimpleToken.PREFIX):
            return self.prefix_stmt()
        if self.current_token.matches(StatementSimpleToken.CONSTOBJ):
            return self.constobj_stmt()

        self.error("Invalid statement")

    def mfunc_stmt(self):
        """
        mfunc_stmt ::= "mfunc" && STR && (NEWLINE)* & INDENT && suite && DEDENT

        Returns:
            McFunctionNode: The mcfunction node to define the mcfunction in the parse tree
        """
        self.eat(StatementSimpleToken.MFUNC)

        # if self.symbol_table.function is not None:
        #     self.error("Cannot define a mcfunction inside an mcfunction")

        mfunc_name = self.eat(TypedToken.STRING, error_message="Expected a string after a mfunc statement")

        # if self.symbol_table.folders is None:
        #     full_path = os.path.join(self.file_path, name)
        # else:
        #     full_path = os.path.join(self.file_path, self.symbol_table.folders, name)

        # skips any and all newlines right after a mfunc statement
        while self.current_token.matches(WhitespaceSimpleToken.NEWLINE):
            self.eat(WhitespaceSimpleToken.NEWLINE)

        self.eat(WhitespaceSimpleToken.INDENT)
        command_nodes = self.command_suite()
        self.eat(WhitespaceSimpleToken.DEDENT)

        return McFunctionNode(mfunc_name, command_nodes)

    def folder_stmt(self):
        """
        folder_stmt ::= "folder" && STR && (NEWLINE)* & INDENT && suite && DEDENT

        Returns:
            FolderNode
        """
        self.eat(StatementSimpleToken.FOLDER)

        # requires there to be no current mcfunction since a folder statement
        # always occurs outside a mfunc statement
        # if self.symbol_table.function is not None:
        #     self.error("Cannot parse a folder statement inside an mcfunction")

        # sets the current folder
        # self.symbol_table = ScopedSymbolTable(enclosing_scope=self.symbol_table)
        # self.symbol_table.add_folder(folder_token.value)
        folder_token = self.eat(TypedToken.STRING)

        # skips any and all newlines right after a folder statement
        while self.current_token.matches(WhitespaceSimpleToken.NEWLINE):
            self.eat(WhitespaceSimpleToken.NEWLINE)

        self.eat(WhitespaceSimpleToken.INDENT)
        statement_nodes = self.statement_suite()
        self.eat(WhitespaceSimpleToken.DEDENT)

        # resets the current folder
        # self.symbol_table = self.symbol_table.enclosing_scope

        return FolderNode(folder_token, statement_nodes)

    def prefix_stmt(self):
        """
        prefix_stmt ::= "prefix" && STR

        Returns:
            PrefixNode
        """
        self.eat(StatementSimpleToken.PREFIX)
        prefix_token = self.eat(TypedToken.STRING, error_message="Expected a string after a prefix statement")

        # requires the prefix to be defined in the global scope
        # if not self.symbol_table.is_global:
        #     self.error("Cannot define a prefix when the scope is not global")

        # self.in_file_config.prefix = prefix_token
        return PrefixNode(prefix_token)

    def constobj_stmt(self):
        """
        constobj_stmt ::= "constobj" && STR

        Returns:
            ConstObjNode
        """
        self.eat(StatementSimpleToken.CONSTOBJ)
        constobj_token = self.eat(TypedToken.STRING, error_message="Expected a string after a constobj statement")

        # requires the constobj to be defined in the global scope
        # if not self.symbol_table.is_global:
        #     self.error("The constobj cannot be set outside the global context")

        # self.in_file_config.constobj = constobj_token
        return ConstObjNode(constobj_token)

    def command(self):
        """
        command ::= (execute_cmd && ":")? && [sb_cmd, function_cmd, simple_cmd]

        Returns:
            FenaCmdNode
        """
        command_segment_nodes = []

        # gets either the execute command or a scoreboard shortcut command
        if self.current_token.matches(SelectorSimpleToken.BEGIN):
            selector_begin_node = self.selector_begin_cmd()
            command_segment_nodes.append(selector_begin_node)
        elif (Parser.config_data.version == "1.13" and 
                self.current_token.value in TokenValues.get(ExecuteSimpleToken) or is_coord_token(self.current_token)):
            execute_node = self.execute_cmd()
            command_segment_nodes.append(execute_node)

        if not self.current_token.matches(WhitespaceSimpleToken.NEWLINE):
            # guaranteed to be a scoreboard shortcut command with a selector
            if self.current_token.matches(SelectorSimpleToken.BEGIN):
                sb_cmd_node = self.sb_cmd()
                command_segment_nodes.append(sb_cmd_node)

            # string can be a target no matter the context
            elif self.current_token.matches(TypedToken.STRING):
                if self.current_token.value not in Parser.config_data.command_names:
                    # if the string is not a command specified in the config data, guaranteed scoreboard shortcut
                    command_node = self.sb_cmd()
                else:
                    command_node = self.simple_cmd()
                command_segment_nodes.append(command_node)

            else:
                self.error("Expected a newline, selector or start of a simple command")

        return FenaCmdNode(command_segment_nodes)

    def selector_begin_cmd(self):
        """
        Intermediary function to determine whether a selector at the beginning
        of a command is part of a scoreboard shortcut or execute shortcut

        It is an execute shortcut if the second token is a selector, coordinate, part of the ExecuteSimpleToken class or a colon
        It is (assumed to be) a scoreboard shortcut otherwise

        Returns:
            ExecuteCmdNode: if the selector is part of an execute shortcut
            ScoreboardCmdMathNode: if the selector is part of a scoreboard math shortcut
            ScoreboardCmdSpecialNode: if the selector is part of a scoreboard special shortcut
        """
        selector_node = self.selector()
        # assumes scoreboard objectives will not be the same as the execute shortcut simple tokens
        if (self.current_token.value in TokenValues.get(ExecuteSimpleToken) or is_coord_token(self.current_token) or 
                self.current_token.matches_any_of(SelectorSimpleToken.BEGIN, SimpleToken.COLON)):
            return self.execute_cmd(begin_selector=selector_node)
        return self.sb_cmd(begin_target=selector_node)

    def execute_cmd(self, begin_selector=None):
        """
        Does a specific function depending on the version provided
        execute_cmd ::= {"1.12": execute_cmd_1_12, "1.13": execute_cmd_1_13}

        Returns:
            ExecuteCmdNode_1_12
            ExecuteCmdNode_1_13
        """

        if Parser.config_data.version == "1.12":
            return self.execute_cmd_1_12(begin_selector)
        elif Parser.config_data.version == "1.13":
            return self.execute_cmd_1_13(begin_selector)
        else:
            self.error("Unknown version")

    def execute_cmd_1_12(self, begin_selector=None):
        """
        execute_cmd_1_12 ::= selector && (vec3)? && (exec_sub_if)? && (execute_cmd)? && ":"

        Returns:
            ExecuteCmdNode_1_12: Node containing a list of ExecuteCmdSubNode_1_12 objects
        """
        execute_nodes = []

        while True:
            # begin_selector is always set back to none at the beginning
            if begin_selector is None:
                selector_node = self.selector() 
            else:
                selector_node = begin_selector

            if is_coord_token(self.current_token):
                coords_node = self.vec3()
            else:
                coords_node = None

            if self.current_token.value == "if":
                exec_sub_if_nodes = self.exec_sub_if_arg()
            else:
                exec_sub_if_nodes = None

            # this execute node format is specific to 1.12
            execute_node = ExecuteSubLegacyArg(selector=selector_node, coords=coords_node, sub_if=exec_sub_if_nodes)
            execute_nodes.append(execute_node)

            begin_selector = None
            if self.current_token.matches(SimpleToken.COLON):
                self.advance()
                break

            return ExecuteCmdNode(execute_nodes)

    def execute_cmd_1_13(self, begin_selector=None):
        """
        execute_cmd_1_13 ::= [selector, vec3, exec_sub_cmds]+ && ":"

        Returns:
            ExecuteCmdNode_1_13: 1.13 execute command node containing a list of SelectorNode, Vec3Node, and any ExecuteSub{type}Node
        """
        execute_nodes = []

        if begin_selector is not None:
            execute_nodes.append(begin_selector)

        while True:
            if self.current_token.value in TokenValues.get(ExecuteSimpleToken):
                exec_sub_node = self.exec_sub_cmds()
                execute_nodes.append(exec_sub_node)

            elif self.current_token.matches(SelectorSimpleToken.BEGIN):
                selector_node = self.selector()
                execute_nodes.append(selector_node)

            elif is_coord_token(self.current_token):
                coords_node = self.vec3()
                execute_nodes.append(coords_node)
        
            elif self.current_token.matches(SimpleToken.COLON):
                self.advance()
                break

            else:
                self.error("Unknown argument for an execute shortcut")

        execute_node = ExecuteCmdNode(execute_nodes)
        return execute_node

    def exec_sub_cmds(self):
        """
        exec_sub_cmd_keywords ::= ("as", "pos", "at", "facing", "rot", "anchor", "in", "ast", "if", "ifnot", "unless", "result" ,"success")
        exec_sub_cmds ::= [rio.rule("exec_sub_" + rule) for (str rule) in exec_sub_cmd_keywords]

        Chooses a method between each token value in token_classes.ExecuteSimpleToken
        This assumes that the current token value matches one token value inside the ExecuteSimpleToken

        Returns:
            list of ExecSubArg Nodes
        """
        assert Parser.config_data.version == "1.13"

        # skips past the first part of the execute sub command
        self.advance()
        self.eat(SimpleToken.OPEN_PARENTHESES)

        # gets the attribute of "exec_sub_(sub_command)"
        method_name = "exec_sub_{}_arg".format(self.current_token.value)
        exec_sub_arg_method = getattr(self, method_name) 

        # contains the list of nodes gotten from the arg method
        exec_sub_arg_nodes = []

        while True:
            exec_sub_arg_node = exec_sub_arg_method()
            exec_sub_arg_nodes.append(exec_sub_arg_node)

            if self.current_token.matches(SimpleToken.COLON):
                self.advance()
            elif self.current_token.matches(SimpleToken.CLOSE_PARENTHESES):
                break

        self.eat(SimpleToken.CLOSE_PARENTHESES)

        # gets the proper node for the execute sub command
        return exec_sub_arg_nodes

    def exec_sub_if_arg(self):
        """
        exec_sub_if_arg ::= [exec_sub_if_arg_selector, exec_sub_if_arg_block, exec_sub_if_arg_blocks, exec_sub_if_arg_compare, exec_sub_if_arg_range]

        exec_sub_if_arg_selector ::= selector
        exec_sub_if_arg_block ::= block && (vec3)?
        exec_sub_if_arg_blocks ::= vec3 && vec3 && "==" && vec3 && ["all", "masked"]?
        exec_sub_if_arg_compare ::= (target)? && STR && ["==", "<", "<=", ">", ">="] && (target && STR) | (INT)
        exec_sub_if_arg_range ::= (target)? && STR && in && range

        1.12
        Returns:
            ExecuteSubIfArgBlock
        """
        if Parser.config_data.version == "1.12":
            if self.current_token.value not in Parser.config_data.blocks:
                self.error("Expected a block inside the if argument")

            self.current_token.cast(TypedToken.BLOCK)
            block_token = self.advance()

            if is_coord_token(self.current_token):
                coord_node = self.vec3()
            else:
                coord_node = None

            return ExecuteSubIfBlockArg(block_token, coord_node)

        else:
            raise NotImplementedError
            

    def sb_cmd(self, begin_target=None):
        """
        sb_cmd ::= [sb_players_math, sb_players_special]

        Returns:
            ScoreboardCmdMathNode: if the selector is part of a scoreboard math shortcut
            ScoreboardCmdSpecialNode: if the selector is part of a scoreboard special shortcut
        """
        if begin_target is None:
            begin_target = self.target()

        if self.current_token.value in Parser.sb_special_operators:
            self.sb_players_math(begin_target=begin_target)
        else:
            self.sb_players_special(target=begin_target)

    def sb_players_math(self, begin_target):
        """
        sb_players_math ::= target && STR && ["=", "<=", ">=", "swap", "+=", "-=", "*=", "/=", "%="] && (signed_int | target && (STR)?)

        Returns:
            ScoreboardCmdMathNode: pass
            ScoreboardCmdMathValueNode: pass
        """

        begin_objective = self.eat(TypedToken.STRING)
        operator = self.eat(TypedToken.STRING, values=Parser.sb_math_operators)

        if self.current_token.matches(SelectorSimpleToken.BEGIN):
            end_target = self.selector
        else:
            # target might be a signed int if it is a string
            end_target = self.eat(TypedToken.STRING)

        # gets the optional ending objective
        # this means that the target is not a constant number
        if self.current_token.matches(TypedToken.STRING):
            end_objective = self.eat(TypedToken.STRING)
            return ScoreboardCmdMathNode(begin_target, begin_objective, operator, end_target, end_objective)

        # checks whether the target is just a signed int, meaning the target is just a constant number
        if isinstance(end_target, Token) and is_signed_int(end_target.value):
            return ScoreboardCmdMathValueNode(begin_target, begin_objective, operator, end_target)
        return ScoreboardCmdMathNode(begin_target, begin_objective, operator, end_target)


    def sb_players_special(self, target):
        """
        sb_players_special ::= target && ["enable", "reset", "<-"] && STR
        """

        sub_cmd = self.eat(TypedToken.STRING, values=Parser.sb_special_operators)
        objective = self.eat(TypedToken.STRING)

        return ScoreboardCmdSpecialNode(target, sub_cmd, objective)

    def simple_cmd(self):
        """
        simple_cmd ::= [team_cmd, tag_cmd, data_cmd, bossbar_cmd, effect_cmd, function_cmd, (COMMAND_KEYWORD && (STR, selector, tag)*)]

        Note that a simple command can turn into a scoreboard command
        because "tp" can be a fake player name being set to a scoreboard value
        This will only happen if the 3rd token is a scoreboard operator
        """
        command_name = self.current_token.value
        if command_name not in self.config_data.command_names:
            self.error("Expected a command name (specifed under fena/src/config/command_names_{version}.txt")

        # advances the command name
        command_token_value = self.advance()

        if command_name == "bossbar":
            return self.bossbar_cmd()

        if command_name == "data":
            return self.data_cmd()

        if command_name == "effect":
            return self.effect_cmd()

        if command_name == "function":
            return self.function_cmd()

        if command_name == "tag":
            return self.tag_cmd()

        if command_name == "team":
            return self.team_cmd()

        # should get all values until the next newline
        # note that the second token is automatically gotten
        raise NotImplementedError

    def bossbar_cmd(self):
        """
        bossbar_cmd ::= "bossbar" && [bossbar_add, bossbar_remove, bossbar_get, bossbar_set]
        """

        sub_cmd = self.current_token.value
        if sub_cmd == "add":
            return self.bossbar_add()
        if sub_cmd == "remove":
            return self.bossbar_remove()

        bossbar_id = self.eat(TypedToken.STRING)

        if self.current_token == "<-":
            return self.bossbar_get(bossbar_id)
        return self.bossbar_set(bossbar_id)

    def bossbar_add(self):
        """
        bossbar_add ::= "add" && STR && [json, STR]?
        """
        self.eat(TypedToken.STRING, value="add")
        bossbar_id = self.eat(TypedToken.STRING)

        if self.current_token.matches(TypedToken.JSON):
            # TODO change to json node
            json_token = self.eat(TypedToken.JSON)
            return BossbarAddNode(bossbar_id, json=json_token)

        if self.current_token.matches(TypedToken.STRING):
            display_name = self.eat(TypedToken.STRING)
            return BossbarAddNode(bossbar_id, display_name=display_name)

    def bossbar_remove(self):
        """
        bossbar_remove ::= "remove" && STR
        """
        self.eat(TypedToken.STRING, value="remove")
        bossbar_id = self.eat(TypedToken.STRING)
        return BossbarRemoveNode(bossbar_id)

    def bossbar_get(self, bossbar_id):
        """
        bossbar_get ::= STR && "<-" && ["max", "value", "players", "visible"]
        """
        self.eat(TypedToken.STRING, value="<-")
        sub_cmd = self.eat(TypedToken.STIRNG, values=Parser.bossbar_get_sub_cmds)

        return BossbarGetNode(bossbar_id, sub_cmd)

    def bossbar_set(self, bossbar_id):
        """
        bossbar_set ::= STR && bossbar_arg && bossbar_arg_value
        # bossbar_option_arg, bossbar_option_arg_value are defined in the bossbar_version.json
        """
        sub_cmd = self.current_token.value
        if sub_cmd not in Parser.bossbar_set_sub_cmds:
            self.error("Expected token in {} for a bossbar set shortcut".format(Parser.bossbar_set_sub_cmds))

        if sub_cmd == "max":
            return self.bossbar_set_max(bossbar_id)
        if sub_cmd == "value":
            return self.bossbar_set_value(bossbar_id)
        if sub_cmd == "players":
            return self.bossbar_set_players(bossbar_id)
        if sub_cmd == "=":
            return self.bossbar_set_visible(bossbar_id)
        if sub_cmd == "color":
            return self.bossbar_set_color(bossbar_id)
        if sub_cmd == "style":
            return self.bossbar_set_style(bossbar_id)

    def bossbar_set_max(self, bossbar_id):
        """
        bossbar_set_max ::= STR && "max" && "=" && pos_int
        """
        self.eat(TypedToken.STRING, value="max")
        max_value = self.pos_int()
        return BossbarSetMaxNode(bossbar_id, max_value)

    def bossbar_set_value(self, bossbar_id):
        """
        bossbar_set_value ::= STR && "value" && "=" && nonneg_int
        """
        self.eat(TypedToken.STRING, value="value")
        value = self.nonneg_int()
        return BossbarSetMaxNode(bossbar_id, value)

    def bossbar_set_players(self, bossbar_id):
        """
        bossbar_set_players ::= STR && "players" && "=" && selector
        """
        self.eat(TypedToken.STRING, value="players")
        players = self.selector()
        return BossbarSetMaxNode(bossbar_id, players)

    def bossbar_set_visible(self, bossbar_id):
        """
        bossbar_set_visible ::= STR && "=" && ["visible", "invisible"]
        """
        self.eat(TypedToken.STRING, value="=")
        self.eat(TypedToken.STRING, values={"visible", "invisible"})

    def bossbar_set_color(self, bossbar_id):
        """
        bossbar_set_color ::= STR && "color" && "=" && ["white", "pink", "red", "yellow", "green", "blue", "purple"]
        """
        self.eat(TypedToken.STRING, value="color")

    def bossbar_set_style(self, bossbar_id):
        """
        bossbar_set_style ::= STR && "style" && "=" && ["0", "6", "10", "12", "20"]
        """
        self.eat(TypedToken.STRING, value="style")


    def data_cmd(self):
        raise NotImplementedError

    def effect_cmd(self):
        raise NotImplementedError

    def function_cmd(self):
        raise NotImplementedError

    def tag_cmd(self):
        raise NotImplementedError

    def team_cmd(self):
        raise NotImplementedError

    def selector(self):
        """
        selector ::= selector_var & ("[" & selector_args & "]")?

        Returns:
            SelectorNode
        """
        selector_var = self.eat(SelectorSimpleToken.BEGIN)

        if self.current_token.matches(SelectorSimpleToken.OPEN_BRACKET):
            self.eat(SelectorSimpleToken.OPEN_BRACKET)
            selector_args = self.selector_args()
            self.eat(SelectorSimpleToken.CLOSE_BRACKET)

        return SelectorNode(selector_var, selector_args)

    def selector_args(self):
        """
        selector_args ::= (single_arg)? | (single_arg & ("," & single_arg)*)?

        Returns:
            list of Selector{type}ArgNode objects
        """
        selector_args = []

        while not self.current_token.matches(SelectorSimpleToken.CLOSE_BRACKET) and self.current_token.matches(SelectorSimpleToken.COMMA):
            selector_arg = self.single_arg()
            selector_args.append(selector_arg)

        return selector_args

    def single_arg(self):
        """
        single_arg ::= [simple_arg, score_arg, tag_arg]
        """
        selector_arg_token = self.current_token.eat(TypedToken.STRING)
        if not self.current_token.matches(SelectorSimpleToken.EQUALS):
            return self.tag_arg(selector_arg_token)

        # gets any replacements
        selector_arg = selector_arg_token.value
        selector_arg = Parser.config_data.selector_replacements.get(selector_arg, selector_arg)

        if selector_arg in Parser.config_data.selector_arguments:
            self.simple_arg(selector_arg_token, selector_arg)

    def tag_arg(self, tag_arg):
        """
        tag_arg ::= STR

        Args:
            tag_arg (Token)

        Returns:
            SelectorTagArgNode
        """
        return SelectorTagArgNode(tag_arg)

    def score_arg(self, objective_arg):
        """
        score_arg ::= STR & ("=" & int_range)?

        Returns:
            SelectorScoreArgNode
        """
        self.eat(SelectorSimpleToken.EQUALS)
        int_range = self.int_range()
        return SelectorScoreArgNode(objective_arg, int_range)

    def simple_arg(self, simple_arg_token, simple_arg):
        """
        simple_arg ::= default_arg & "=" & default_arg_value_group
        """
        default_arg = self.default_arg()
        self.eat(SelectorSimpleToken.EQUALS)
        arg_details = Parser.config_data.selector_argument_details[default_arg.value]
        default_arg_value = self.default_arg_value_group(arg_details)
        return SelectorDefaultArgNode(default_arg, default_arg_value)

    def default_arg_value_group(self, arg_details):
        """
        default_arg_value_group = ("!")? & (default_arg_value | ("(" && default_arg_values && ")"))

        Args:
            arg_details (dict): pass

        Returns:
            SelectorDefaultArgValueNode: if the value is a range, number or string
            SelectorDefaultGroupArgValueNode: if the value is actually a group surrounded by "(" and ")"
        """
        # checks for negation
        if (arg_details.get("negation", False) and self.current_token.matches(SelectorSimpleToken.NOT)):
            self.advance()
            negated = True
        else:
            negated = False

        # checks for group
        if arg_details.get("group", False) and self.current_token.matches(SimpleToken.OPEN_PARENTHESES):
            if ((arg_details["group"] == "negation" and negated) or
                    (arg_details["group"] == "default" and not negated) or
                    (arg_details["group"] == "any")):
                group = True
            else:
                # open parenthesis shows there is a group defined in the wrong context
                self.error("Unknown base case for group")
        else:
            group = False

        # gets group values
        if group:
            self.eat(SimpleToken.OPEN_PARENTHESES)
            value_nodes = self.default_arg_values(arg_details)
            self.eat(SimpleToken.CLOSE_PARENTHESES)

            return SelectorDefaultGroupArgValueNode(value_nodes, negated)

        # gets one single argument
        arg_value_token = self.default_arg_value(arg_details)
        return SelectorDefaultArgValueNode(arg_value_token, negated)

    def default_arg_values(self, arg_details):
        """
        default_arg_values ::= (default_arg_value)? | (single_arg & ("," & single_arg)*)?

        Returns:
            list: Contains any combination of Token, IntRangeNode and, NumberRangeNode objects
        """
        default_arg_values = []
        while not self.current_token.matches(SimpleToken.CLOSE_PARENTHESES):
            value = self.default_arg_value(arg_details)
            default_arg_values.append(value)

        return default_arg_values

    def default_arg(self):
        """
        # default_arg is defined under selector_version.json as "selector_arguments"
        """
        if self.current_token.value not in Parser.config_data.selector_arguments:
            self.error("Unknown selector argument")

        return self.eat(TypedToken.STRING)

    def default_arg_value(self, arg_details):
        """
        # default_arg_value is defined under selector_version.json as "selector_argument_details"

        Args:
            arg_details (dict): Holds all information for the specific selector argument

        Returns:
            Token: if the parse type was not a range or selector
            SelectorNode: if the parse type was a selector
            IntRangeNode: if the parse type is an int range
            NumberRangeNode: if the parse type is a number range
        """

        # parse_type = arg_details["parse_type"]

        # # determines if the value is within the group of specified values
        # # as long as the replacement dictionary is applied
        # if parse_type == "VALUES":
        #     arg_value = self.current_token.value
        #     assert "values" in arg_details, "If the parse type is 'VALUES', a 'values' list must be present in the json"
        #     valid_values = arg_details["values"]

        #     # checks whether there are any values that have to be replaced
        #     if "value_replace" in arg_details:
        #         replacement_values = arg_details["value_replace"]
        #         arg_value = replacement_values.get(arg_value, arg_value)

        #     # checks if the arg value is actually in the default given "values"
        #     if arg_value not in arg_details["values"]:
        #         if "value_replace" in arg_details:
        #             self.error(f"Expected one of {valid_values} if shorthands are {replacement_values})")
        #         self.error(f"Expected one of {valid_values})")

        #     arg_value_token = self.eat(TypedToken.STRING)
        #     arg_value_token.replacement = arg_value
        #     return arg_value_token

        # # the value can be literally one of anything
        # if parse_type == "STR":
        #     return self.eat(TypedToken.STRING)

        # # requires a form of integer, and then stored as an integer
        # if parse_type == "SIGNED_INT":
        #     return self.signed_int()
        # if parse_type == "POS_INT":
        #     return self.pos_int()
        # if parse_type == "NONNEG_INT":
        #     return self.nonneg_int()

        # # requires an integer or floating point value
        # # note that this doesn't convert it into a float to prevent loss in precision
        # if parse_type == "NUMBER":
        #     arg_value = self.current_token.value
        #     if not is_number(arg_value):
        #         self.error("Expected a real number (sadly, no complex numbers are allowed in minecraft)")
        #     arg_value_token = self.eat(TypedToken.STRING)
        #     arg_value_token.cast(TypedToken.FLOAT)
        #     return arg_value_token

        # if parse_type == "INT_RANGE":
        #     return self.int_range()

        # if parse_type == "NUMBER_RANGE":
        #     return self.number_range()

        # # checks if the value is a valid entity, and then returns it as a string token
        # if parse_type == "ENTITIES":
        #     arg_value = self.current_token.value
        #     if arg_value not in Parser.config_data.entities:
        #         self.error("Expected an entity type")
        #     return self.eat(TypedToken.STRING)

        # if parse_type == "SELECTOR":
        #     return self.selector()

        # if parse_type == "ADVANCEMENT_GROUP":
        #     raise NotImplementedError 

        # if parse_type == "SHORTCUT_ERROR":
        #     self.error("Shortcut error (There is most likely a shortcut version of this that should be used)")

        # self.error("Unknown default value")

        self.json_parse_arg_value(arg_details)

    def nonneg_int(self):
        """
        nonneg_int ::= INT  # Z nonneg
        """
        if not is_nonneg_int(self.current_token.value):
            self.error("Expected a nonnegative integer (all integers greater than or equal to 0)")

    def signed_int(self):
        """
        signed_int ::= ("-")? && INT  # Z
        """
        if not is_signed_int(self.current_token.value):
            self.error("Expected a signed integer (possibly negative integer)")

        return self._get_int()

    def pos_int(self):
        """
        pos_int ::= INT, != 0  # Z+
        """
        if not is_pos_int(self.current_token.value):
            self.error("Expected a positive integer (all integers greater than 0)")

        return self._get_int()

    def _get_int(self):
        """
        Returns:
            Token: Token with type TypedToken.INT
        """
        token = self.eat(TypedToken.STRING)
        token.cast(TypedToken.INT)
        return token

    def nonneg_float(self):
        """
        nonneg_float ::= (INT)? && "." && INT  # R, R <= 0
        """
        if is_number(self.current_token.value):
            self.error("Expected any proper number")

        if float(self.current_token.value) < 0:
            self.error("Expected a number greater than or equal to 0")

        return self.eat(TypedToken.STRING)

    def signed_float(self):
        """
        signed_float ::= ("-")? && nonneg_float  # R
        """
        if is_number(self.current_token.value):
            self.error("Expected any proper number")

        return self.eat(TypedToken.STRING)

    def int_range(self):
        raise NotImplementedError

    def number_range(self):
        raise NotImplementedError

    def target(self):
        """
        target ::= [selector, STR]
        """
        if self.current_token.matches(SelectorSimpleToken.BEGIN):
            return self.selector()

        return self.eat(TypedToken.STRING)

    def entity_vec3(self):
        """
        entity_vec3 ::= [selector, vec3]
        """
        if self.current_token.matches(SelectorSimpleToken.BEGIN):
            return self.selector()

        return self.vec3()
    
    def vec2(self):
        """
        Returns:
            Vec2Node
        """
        coords_node = self._coords(3)
        assert isinstance(coords_node, Vec3Node)
        return coords_node

    def vec3(self):
        """
        Returns:
            Vec3Node
        """
        coords_node = self._coords(3)
        assert isinstance(coords_node, Vec3Node)
        return coords_node

    def _coords(self, coord_num):
        assert coord_num in (2, 3)

        coords = []
        for _ in range(coord_num):
            if is_coord_token(self.current_token):
                coord = self.eat(TypedToken.STRING)
                coord.cast(TypedToken.COORD)
                coords.append(coord)
            else:
                self.error("Expected a coord token")

        if not are_coords(*coords):
            coords_str = " ".join(str(c) for c in coords)
            self.error("Expected a proper coord type given all coordinates ({})".format(coords_str))

        return CoordsNode(coords)

    def __repr__(self):
        return "Parser[iterator={}, current_token={}]".format(repr(self.iterator), repr(self.current_token))

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

    # mcfunctions = parser.mcfunctions
    # for mcfunction in mcfunctions:
    #     logging.debug("")
    #     logging.debug(str(mcfunction))
    #     for command in mcfunction.commands:
    #         logging.debug(repr(command))
