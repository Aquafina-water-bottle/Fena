import os
import logging
import inspect

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

    import fena.logging_setup as logging_setup

from fena.assert_utils import assert_type
from fena.lexical_token import Token
from fena.token_classes import TypedToken, DelimiterToken, WhitespaceToken
from fena.lexer import Lexer
# from fena.nodes import *
from fena.nodes import ProgramNode, McFunctionNode, FolderNode, PrefixNode, ConstObjNode, FenaCmdNode
from fena.nodes import ScoreboardCmdMathNode, ScoreboardCmdMathValueNode, ScoreboardCmdSpecialNode, FunctionCmdNode, SimpleCmdNode
from fena.nodes import ExecuteCmdNode, ExecuteSubIfBlockArg, ExecuteSubLegacyArg
from fena.nodes import SelectorNode, SelectorVarNode, SelectorArgsNode
from fena.nodes import SelectorDefaultArgNode, SelectorScoreArgNode, SelectorTagArgNode, SelectorNbtArgNode
from fena.nodes import SelectorScoreArgsNode, SelectorTagArgsNode, SelectorNbtArgsNode, SelectorAdvancementGroupArgNode
from fena.nodes import SelectorDefaultArgValueNode, SelectorDefaultGroupArgValueNode
from fena.nodes import JsonObjectNode, JsonMapNode, JsonArrayNode
from fena.nodes import NbtObjectNode, NbtMapNode, NbtArrayNode, NbtIntegerNode, NbtFloatNode
from fena.nodes import BossbarAddNode, BossbarRemoveNode, BossbarGetNode, BossbarSetNode
from fena.nodes import Vec3Node, Vec2Node, IntRangeNode, NumberRangeNode, BlockNode, NamespaceIdNode
from fena.node_visitors import NodeBuilder, NodeVisitor
from fena.coord_utils import is_coord_token, are_coords
from fena.config_data import ConfigData
from fena.number_utils import is_signed_int, is_nonneg_int, is_pos_int, is_number, is_json_number, is_nbt_float


"""
test parser logic

def parse8(self):
    # one place for error and parsing digit without boolean
    self.eat("(")

    if not self.current_char == ")":
        while self.current_char.isdigit():
            self.advance()

            if self.current_char == ",":
                self.advance()
            elif self.current_char == ")":
                break
            else:
                self.error("Expected a comma or closing square bracket")
        else:
            raise SyntaxError(f"Unexpected character {self.current_char}")

    self.eat(")")
"""

r"""
Organizes all tokens into nodes of an abstract syntax tree (AST)
Grammar:

program ::= statement_suite
statement_suite ::= [NEWLINE, (statement, NEWLINE)]*

statement ::= "!" && [folder_stmt, mfunc_stmt, prefix_stmt, constobj_stmt]
folder_stmt ::= "folder" && STR && ":" && (NEWLINE)* & INDENT && statement_suite && DEDENT
mfunc_stmt ::= "mfunc" && [STR, literal_str] && ":" && (NEWLINE)* & INDENT && command_suite && DEDENT
prefix_stmt ::= "prefix" && STR
constobj_stmt ::= "constobj" && STR

command_suite ::= [NEWLINE, (command, NEWLINE)]*
command ::= (execute_cmd)? && [sb_cmd, simple_cmd]
simple_cmd ::= [bossbar_cmd, effect_cmd, data_cmd, function_cmd, tag_cmd, team_cmd, xp_cmd, (COMMAND_KEYWORD && (STR, selector, nbt, json)*)]

execute_cmd_1_12 ::= selector && (vec3)? && (exec_sub_if)? && (execute_cmd_1_12)? && ":"
execute_cmd_1_13 ::= [selector, vec3, exec_sub_cmds]+ && ":"

exec_sub_cmd_keywords ::= ("as", "pos", "at", "facing", "rot", "anchor", "in", "ast", "if", "ifnot", "unless", "result" ,"success")
exec_sub_cmds ::= [rio.rule("exec_sub_" + rule) for (str rule) in exec_sub_cmd_keywords]
for (str rule) in exec_sub_cmd_keywords:
    rule_arg ::= rio.rule("exec_sub_" + rule + "_arg)
    rio.rule("exec_sub_" + rule) ::= rule && "(" && rule_arg && ("," && rule_arg)* && ")"

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
exec_sub_if_arg_compare ::= (target)? && STR && ["==", "<", "<=", ">", ">=" , "!="] && ((target && STR) | [signed_int, "*"])
exec_sub_if_arg_range ::= (target)? && STR && "in" && int_range
exec_sub_ifnot_arg ::= exec_sub_if_arg
exec_sub_unless_arg ::= exec_sub_if_arg

exec_sub_result_arg ::= [exec_sub_result_arg_data, exec_sub_result_arg_score, exec_sub_result_arg_bossbar]
exec_sub_result_arg_data ::= entity_vec3 && STR && (data_type)? && signed_int
exec_sub_result_arg_score ::= target && STR
exec_sub_result_arg_bossbar ::= STR && ["max", "value"]
exec_sub_success_arg ::= exec_sub_result_arg 

sb_cmd ::= [sb_players_math, sb_players_special]
sb_players_math ::= target && STR && ["=", "<=", ">=", "swap", "+=", "-=", "*=", "/=", "%="] && (signed_int | target && (STR)?)
sb_players_special ::= target && ["enable", "reset", "<-"] && STR

bossbar_cmd ::= "bossbar" && [bossbar_add, bossbar_remove, bossbar_get, bossbar_set]
bossbar_add ::= "add" && bossbar_id && [json, STR]?
bossbar_remove ::= "remove" && bossbar_id
bossbar_get ::= bossbar_id && "<-" && ["max", "value", "players", "visible"]
bossbar_set ::= bossbar_id && bossbar_arg && "=" && bossbar_arg_value
# bossbar_option_arg, bossbar_option_arg_value are defined in the bossbar_version.json

data_cmd ::= "data" && [data_get, data_merge, data_remove]
data_get ::= entity_vec3 && "<-" && (STR && (signed_int)?)?
data_merge ::= entity_vec3 && "+" && nbt
data_remove ::= entity_vec3 && "-" && STR

effect_cmd ::= "effect" && [effect_give, effect_clear]
effect_clear ::= selector && "-" && ["all", effect_id]
effect_give ::= selector && "+" && effect_id && (pos_int && ((nonneg_int)? && ["true", "false"]? )? )?
# effect_id are defined under effects.json

function_cmd ::= "function" && STR

tag_cmd ::= "tag" && [tag_add, tag_remove]
tag_add ::= selector && "+" && STR
tag_remove ::= selector && "-" && STR

team_cmd ::= "team" && [team_add, team_join, team_leave, team_empty, team_option, team_remove]
team_add ::= "add" && STR && (STR)*
team_join ::= STR && "+" && target
team_leave ::= "leave" && target
team_empty ::= "empty" && STR
# team_option ::= STR && json_parse
team_option ::= STR && team_option_arg && "=" && team_option_arg_value
# team_option_arg, team_option_arg_value are defined in the team_options_version.json
team_remove ::= "remove" && STR

xp_cmd ::= "xp" && [xp_math, xp_get]
xp_math ::= ["=", "+", "-"] && nonneg_int && ["points", "levels"]?
xp_get ::= "<-" && ["points", "levels"]

selector ::= selector_var & ("[" & selector_args & "]")?
selector_var ::= "@" & selector_var_specifier
# selector_var_specifier is defined under selector_version.json as "selector_variable_specifiers"
selector_args ::= (single_arg)? | (single_arg & ("," & single_arg)*)?
single_arg ::= [simple_arg, score_arg, tag_arg, nbt_arg]

# note that all selector argument values can have round brackets surrounding it
simple_arg ::= default_arg & "=" & default_arg_value_group
# default_arg is defined under selector_version.json as "selector_arguments"

# requires at least one value, otherwise completely useless
default_arg_value_group = ("!")? & (default_arg_value | ("(" && default_arg_values && ")"))
default_arg_values ::= default_arg_value | (default_arg_value & ("," & default_arg_value)*)?
# default_arg_value is defined under selector_version.json as "selector_argument_details"

tag_arg ::= ("!")? & STR
score_arg ::= (STR & "=" & score_arg_value)
score_arg_value ::= [int_range, "*"] | "(" & score_arg_value & ")"
nbt_arg ::= ("!")? & nbt

# note that this is part of the default_arg_values thing
# @a[adv=(story/mine_diamond=(diamond),story/iron_tools)]
adv_arg_group ::= "(" && adv_args && ")"
adv_args ::= (adv_arg)? | (adv_arg & ("," & adv_arg)*)
adv_arg ::= ("!")? & STR & ("=" & "(" & adv_arg_values & ")")?
adv_arg_values ::= adv_arg_value & ("," & adv_arg_value?)
adv_arg_value ::= ("!")? & STR

nbt ::= nbt_object
nbt_object ::= "{" && ((nbt_map)? | (nbt_map && ("," && nbt_map)*)) && "}"
nbt_map ::= STR && ":" && nbt_value
nbt_array ::= "[" && (nbt_array_begin && ";")? && nbt_value)? | (nbt_value && ("," && nbt_value)*) && "]"
nbt_array_begin ::= ["I", "L", "B"]
nbt_value ::= [literal_str, nbt_number, nbt_object, nbt_array]
nbt_number = (signed_int & ["b", "s", "L"]?) | json_number & ["d", "f"]?

# specified under https://www.json.org
# json objects = dictionaries, json arrays = lists
json ::= json_object
json_object ::= "{" && ((json_map)? | (json_map && ("," && json_map)*)) && "}"
json_map ::= literal_str && ":" && json_value
json_array ::= "[" && ((json_value)? | (json_value && ("," && json_value)*)) && "]"
json_value ::= [literal_str, json_number, "true", "false", "null", json_object, json_array]
json_number ::= ("-")? && INT && ("." && INT)? && (["e", "E"] && ["+", "-"] && INT)?

nonneg_int ::= INT  # Z nonneg
signed_int ::= ("-")? && INT  # Z
pos_int ::= INT, ::/= 0  # Z+

float ::= (INT)? && "." && INT  # R, R <= 0
signed_float ::= ("-")? && float  # R

number ::= [signed_float, signed_int]
int_range ::= [signed_int, (signed_int & ".."), (".." & signed_int), (signed_int & ".." & signed_int)]
number_range ::= [signed_float, (signed_float & ".."), (".." & signed_float), (signed_float & ".." & signed_float)]
literal_str ::= "\"" && ([\A, "\\\"", "\\\\"])* &&  && "\""

target ::= [selector, STR]
entity_vec3 ::= [selector, vec3]
entity_id ::= ("minecraft" & ":")? & entity_name
# entity_name is defined under entites.json

vec2 ::= coord && coord
vec3 ::= coord && coord && coord
coord ::= ("^", "~")? & [signed_int, signed_float]

block ::= block_id & ("[" & (block_states)? & "]")? & (nbt)?
block_id ::= ("minecraft" && ":")? && block_type
# block_type is defined under blocks.json
block_states ::= (block_state)? | (block_state & ("," & block_state)*)?
block_state ::= STR && "=" && STR

data_type ::= ["byte", "short", "int", "long", "float", "double"]
namespace_id ::= STR && (":" && STR)?
"""

class Parser:
    """
    Makes the mcfunction builders while building all datatags and selectors

    Args:
        lexer (iterator function or iterator)
            
    Attributes:
        lexer (Lexer)
        current_token (Token or None)
        iterator (iterator object)
        return_eof (bool): Whether the parser should manually return an EOF token as the last token or not
            - This is not necessary unless the iterator is a method of the lexer
            - The lexer as an iterator itself should return an EOF
            - This defaults to False
            - If set to True, once it returns an EOF token, it is set back to false
    """

    config_data = ConfigData()

    nbt_int_ends = frozenset({"b", "s", "L"})
    nbt_number_ends = frozenset({"b", "s", "L", "f", "d"})
    nbt_array_start = frozenset({"I", "B", "L"})
    sb_special_operators = frozenset({"enable", "reset", "<-"})
    sb_math_operators = frozenset({"=", "<=", ">=", "swap", "+=", "-=", "*=", "/=", "%="})
    statement_keywords = frozenset({"mfunc", "folder", "prefix", "constobj"})
    execute_keywords = frozenset({"as", "pos", "at", "facing", "ast", "if", "ifnot", "unless", "result", "success"})

    json_parse_options = {
        "bossbar_set": "bossbar_set",
        # "bossbar_get": "bossbar_get",
        "team_options": "team_options",
        "selector": "selector_argument_details"
    }

    def __init__(self, lexer, method_name=None):
        assert_type(lexer, Lexer)

        self.lexer = lexer
        if method_name is None:
            self.iterator = iter(lexer)
            self.return_eof = False

        else:
            assert_type(method_name, str)
            lexer_method = getattr(lexer, method_name, lexer.invalid_method)

            # note that try/except with iter() actually primes the function and only raises the error once the method reaches "return"
            # therefore, using inspect.isgeneratorfunction to prevent unnecessary priming
            if inspect.isgeneratorfunction(lexer_method):
                self.iterator = iter(lexer_method())
            else:
                # simply makes some the method a generator that only yields one object
                def temp():
                    yield lexer_method()
                self.iterator = iter(temp())

            self.return_eof = True

        self.current_token = None
        self.advance()

    def parse(self, method_name="program"):
        """
        Returns:
            ProgramNode: The parse tree parent
        """
        assert_type(method_name, str)
        parser_method = getattr(self, method_name, self.invalid_method)
        ast = parser_method()
        logging.debug("")

        if not self.current_token.matches(WhitespaceToken.EOF):
            self.error("Expected the EOF token at the end of parsing")

        if not self.lexer.reached_eof:
            self.error("Expected the lexer to reach the EOF")

        return ast

    def error(self, message="Invalid syntax"):
        """
        Raises a generic syntax error with an optional message
        """
        assert_type(message, str)
        raise SyntaxError(f"{self.current_token}: {message}")

    def invalid_method(self, *args, **kwargs):
        raise NotImplementedError(f"Invalid parser method")

    def advance(self):
        """
        Gets the next token from the lexer without checking any type

        Returns:
            Token: The token that was just advanced over

        Raises:
            SyntaxError: if the there are no more tokens to advance to (the token after the EOF token)
        """
        previous_token = self.current_token
        self.current_token = next(self.iterator, None)

        if self.current_token is None:
            # Returns only 1 EOF token
            if self.return_eof:
                self.return_eof = False
                self.current_token = self.lexer.create_new_token(WhitespaceToken.EOF)
            else:
                # otherwise, creates error
                self.error("Cannot advance past the last token")

        logging.debug(f"Advanced to {self.current_token!r}")
        return previous_token

    def eat(self, *token_types, values=None, value=None, error_message=None):
        """
        Advances given the token type and values match up with the current token

        Args:
            token_types (any token type): Any token type that can be advanced
            value (any or None): Any specified value that should equal the value of a typed token
            values (any or None): Any specified values that should equal the value of a typed token
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
                (values is None or (self.current_token.value in values and self.current_token.token_type in TypedToken)) and
                (value is None or (self.current_token.value == value) and self.current_token.token_type in TypedToken)):
            return self.advance()

        if error_message is None:
            if len(token_types) == 1:
                expected_type = token_types[0]
                error_message = f"Expected {expected_type!r}"
            else:
                error_message = f"Expected one of {token_types}"

            if values is not None:
                error_message += f" with any value from {values}"
            elif value is not None:
                error_message += f" with a value of {value}"

        self.error(error_message)

    def json_parse_arg(self, json_type, arg_token=None):
        """
        Get the argument of a generic json parse type specified in a config file

        Args:
            json_type (str)
            arg_token (Token or None)

        Returns:
            Token: Token that was gotten to determine the json arg details if an arg_token was not provided already
            dict: json arg details to see the parse type and other information

        Raises:
            SyntaxError: if the token value is not within the specified json type arguments 
        """
        assert json_type in Parser.json_parse_options 

        config_data_attr = Parser.json_parse_options.get(json_type)
        json_object = getattr(Parser.config_data, config_data_attr, self.invalid_method)
        assert json_object != "error", config_data_attr

        provided_token = True
        if arg_token is None:
            arg_token = self.eat(TypedToken.STRING)
            provided_token = False
        
        # gets the replacement if it exists, otherwise gets the value
        arg_str = arg_token.replacement if (arg_token.replacement is not None) else str(arg_token.value)

        if arg_str in json_object:
            if provided_token:
                return json_object[arg_str]
            return arg_token, json_object[arg_str]

        self.error(f"Expected {arg_str} value inside {list(json_object)}")

    def json_parse_arg_value(self, arg_details):
        """
        Parses the argument value according to the specified parse_type found in the arg_details dict

        "parse_type":
            "VALUES": It has a "values" attribute that should have a containment check on it
                - This might also have a "value_replace" attribute as a dictionary to replace strings as shorthands
            "STR": Anything contained inside a string containing [A-Za-z_.-]
            "LITERAL_STR": Anything contained inside two quotations
            "JSON": A general json object
            "SIGNED_INT": Any (possibly negative) integer value (Z)
            "POS_INT": Any positive integer value (Z+)
            "NONNEG_INT": Any nonnegative integer value (Z nonneg)
            "INT_RANGE": Any signed integer range
            "INT_RANGE_BRACKET": Any signed integer range with round brackets around it
            "NUMBER": Any signed integer or signed decimal number
            "NUMBER_RANGE": Any number range
            "NUMBER_RANGE_BRACKET": Any number range with round brackets around it
            "ENTITIES": Matches any entity specified under ``entities``
            "SELECTOR": Matches a selector
            "ADVANCEMENT_GROUP": Special parsing type specifically for advancements
            "SHORTCUT_ERROR": Raises an error because a shortcut should be able to take care of this
        "values": A list of all possible selector argument values
        "value_replace": A dictionary mapping all possible shorthands to the corresponding selector argument value

        Args:
            arg_details (dict)

        Returns:
            SelectorNode: if the parse type was "JSON"
            SelectorNode: if the parse type was "SELECTOR"
            IntRangeNode: if the parse type is "INT_RANGE"
            NumberRangeNode: if the parse type is "NUMBER_RANGE"
            Token: if the parse type was not any of the above
        """
        parse_type = arg_details["parse_type"]

        # determines if the value is within the group of specified values
        # as long as the replacement dictionary is applied
        if isinstance(parse_type, list):
            # currently, only supports two possible options (literal_str or str)
            if ("LITERAL_STR" in parse_type and self.current_token.matches(TypedToken.LITERAL_STRING) or
                    "STR" in parse_type and self.current_token.matches(TypedToken.STRING)):
                return self.advance()
            self.error("Something stupid happened")
            
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

            # self.current_token.cast(TypedToken.STRING)
            arg_value_token = self.advance()
            arg_value_token.replacement = arg_value
            return arg_value_token

        if parse_type == "JSON":
            return self.json()

        # the value can be literally one of anything
        if parse_type == "STR":
            return self.eat(TypedToken.STRING)

        if parse_type == "LITERAL_STR":
            return self.eat(TypedToken.LITERAL_STRING)

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
            arg_value_token = self.eat(TypedToken.INT, TypedToken.FLOAT)
            # arg_value_token.cast(TypedToken.FLOAT)
            return arg_value_token

        if parse_type == "INT_RANGE":
            return self.int_range(args=tuple(arg_details["range_replace"]))

        if parse_type == "INT_RANGE_BRACKET":
            return self.int_range_bracket(args=tuple(arg_details["range_replace"]))

        if parse_type == "NUMBER_RANGE":
            return self.number_range()

        if parse_type == "NUMBER_RANGE_BRACKET":
            return self.number_range_bracket()

        # checks if the value is a valid entity, and then returns it as a string token
        if parse_type == "ENTITIES":
            return self.entity_id()

        if parse_type == "SELECTOR":
            return self.selector()

        if parse_type == "ADVANCEMENT_GROUP":
            return self.adv_arg_group()

        if parse_type == "SHORTCUT_ERROR":
            self.error("Shortcut error (There is most likely a shortcut version of this that should be used)")

        self.error("Unknown default value")

    def program(self):
        """
        program ::= statement_suite

        Returns:
            ProgramNode: The parse tree parent
        """
        logging.debug(f"Begin program at {self.current_token!r}")
        statement_nodes = self.statement_suite()
        logging.debug(f"End program at {self.current_token!r}")

        program = ProgramNode(statement_nodes)
        return program

    def statement_suite(self):
        """
        statement_suite ::= [NEWLINE, (statement, NEWLINE)]*

        Returns:
            list of McFunctionNode, FolderNode, PrefixNode, ConstObjNode objects
        """
        logging.debug(f"Begin statement compound at {self.current_token!r}")
        # logging.debug("with scoped symbol table = {}".format(repr(self.symbol_table)))

        statement_nodes = []

        # note that this is essentially a do-while since it never starts out as a newline
        while self.current_token.matches_any_of(WhitespaceToken.NEWLINE, DelimiterToken.EXCLAMATION_MARK):
            # base case is if a newline is not met
            if self.current_token.matches(WhitespaceToken.NEWLINE):
                self.eat(WhitespaceToken.NEWLINE)

            elif self.current_token.matches(DelimiterToken.EXCLAMATION_MARK):
                statement_node = self.statement()
                statement_nodes.append(statement_node)

            else:
                self.error("Expected a newline or statement specifier")

        logging.debug(f"End statement compound at {self.current_token!r}")

        return statement_nodes

    def command_suite(self):
        """
        command_suite ::= [NEWLINE, (command, NEWLINE)]*

        Returns:
            list of FenaCmdNode objects
        """
        logging.debug(f"Begin command compound at {self.current_token!r}")
        # logging.debug("with scoped symbol table = {}".format(repr(self.symbol_table)))

        command_nodes = []

        # note that this is essentially a do-while since it never starts out as a newline
        while self.current_token.matches_any_of(WhitespaceToken.NEWLINE, TypedToken.STRING, DelimiterToken.AT):
            # base case is if a newline is not met
            if self.current_token.matches(WhitespaceToken.NEWLINE):
                self.eat(WhitespaceToken.NEWLINE)

            elif self.current_token.matches_any_of(TypedToken.STRING, DelimiterToken.AT):
                command_node = self.command()
                command_nodes.append(command_node)

            else:
                self.error("Expected a newline, command or statement specifier")

        logging.debug(f"End command compound at {self.current_token!r}")

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
        self.eat(DelimiterToken.EXCLAMATION_MARK)

        if self.current_token.matches(TypedToken.STRING, value="mfunc"):
            return self.mfunc_stmt()
        if self.current_token.matches(TypedToken.STRING, value="folder"):
            return self.folder_stmt()
        if self.current_token.matches(TypedToken.STRING, value="prefix"):
            return self.prefix_stmt()
        if self.current_token.matches(TypedToken.STRING, value="constobj"):
            return self.constobj_stmt()

        self.error("Invalid statement")

    def mfunc_stmt(self):
        """
        mfunc_stmt ::= "mfunc" && STR && (NEWLINE)* & INDENT && suite && DEDENT

        Returns:
            McFunctionNode: The mcfunction node to define the mcfunction in the parse tree
        """
        self.eat(TypedToken.STRING, value="mfunc")

        # if self.symbol_table.function is not None:
        #     self.error("Cannot define a mcfunction inside an mcfunction")

        mfunc_name = self.eat(TypedToken.STRING, error_message="Expected a string after a mfunc statement")

        # if self.symbol_table.folders is None:
        #     full_path = os.path.join(self.file_path, name)
        # else:
        #     full_path = os.path.join(self.file_path, self.symbol_table.folders, name)

        # skips any and all newlines right after a mfunc statement
        while self.current_token.matches(WhitespaceToken.NEWLINE):
            self.eat(WhitespaceToken.NEWLINE)

        self.eat(WhitespaceToken.INDENT)
        command_nodes = self.command_suite()
        self.eat(WhitespaceToken.DEDENT)

        return McFunctionNode(mfunc_name, command_nodes)

    def folder_stmt(self):
        """
        folder_stmt ::= "folder" && STR && (NEWLINE)* & INDENT && suite && DEDENT

        Returns:
            FolderNode
        """
        self.eat(TypedToken.STRING, value="folder")

        # requires there to be no current mcfunction since a folder statement
        # always occurs outside a mfunc statement
        # if self.symbol_table.function is not None:
        #     self.error("Cannot parse a folder statement inside an mcfunction")

        # sets the current folder
        # self.symbol_table = ScopedSymbolTable(enclosing_scope=self.symbol_table)
        # self.symbol_table.add_folder(folder_token.value)
        folder_token = self.eat(TypedToken.STRING)

        # skips any and all newlines right after a folder statement
        while self.current_token.matches(WhitespaceToken.NEWLINE):
            self.eat(WhitespaceToken.NEWLINE)

        self.eat(WhitespaceToken.INDENT)
        statement_nodes = self.statement_suite()
        self.eat(WhitespaceToken.DEDENT)

        # resets the current folder
        # self.symbol_table = self.symbol_table.enclosing_scope

        return FolderNode(folder_token, statement_nodes)

    def prefix_stmt(self):
        """
        prefix_stmt ::= "prefix" && STR

        Returns:
            PrefixNode
        """
        self.eat(TypedToken.STRING, value="prefix")
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
        self.eat(TypedToken.STRING, value="constobj")
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
        if self.current_token.matches(DelimiterToken.AT):
            selector_begin_node = self.selector_begin_cmd()
            command_segment_nodes.append(selector_begin_node)
        elif (Parser.config_data.version == "1.13" and 
                (self.current_token.value in Parser.execute_keywords or is_coord_token(self.current_token))):
            execute_node = self.execute_cmd()
            command_segment_nodes.append(execute_node)

        if not self.current_token.matches(WhitespaceToken.NEWLINE):
            # guaranteed to be a scoreboard shortcut command with a selector
            if self.current_token.matches(DelimiterToken.AT):
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
        Intermediary function to determine whether a selector at the beginning, IntRangeNode, NumberRangeNode
        of a command is part of a scoreboard shortcut or execute shortcut

        It is an execute shortcut if the second token is a selector, coordinate, part of execute_keywords or a colon
        It is (assumed to be) a scoreboard shortcut otherwise

        Returns:
            ExecuteCmdNode: if the selector is part of an execute shortcut
            ScoreboardCmdMathNode: if the selector is part of a scoreboard math shortcut
            ScoreboardCmdSpecialNode: if the selector is part of a scoreboard special shortcut
        """
        selector_node = self.selector()
        # assumes scoreboard objectives will not be the same as the execute shortcut simple tokens
        if (self.current_token.value in Parser.execute_keywords or is_coord_token(self.current_token) or 
                self.current_token.matches_any_of(DelimiterToken.AT, DelimiterToken.COLON)):
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
                exec_sub_if_nodes = self.exec_sub_cmds()
            else:
                exec_sub_if_nodes = None

            # this execute node format is specific to 1.12
            execute_node = ExecuteSubLegacyArg(selector=selector_node, coords=coords_node, sub_if=exec_sub_if_nodes)
            execute_nodes.append(execute_node)

            begin_selector = None
            if self.current_token.matches(DelimiterToken.COLON):
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
            if self.current_token.value in Parser.execute_keywords:
                exec_sub_node = self.exec_sub_cmds()
                execute_nodes.append(exec_sub_node)

            elif self.current_token.matches(DelimiterToken.AT):
                selector_node = self.selector()
                execute_nodes.append(selector_node)

            elif is_coord_token(self.current_token):
                coords_node = self.vec3()
                execute_nodes.append(coords_node)
        
            elif self.current_token.matches(DelimiterToken.COLON):
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

        Chooses a method between each token value in execute_keywords
        This assumes that the current token value matches one token value inside the ExecuteSimpleToken

        Returns:
            list of ExecSubArg Nodes
        """
        # assert Parser.config_data.version == "1.13"

        # skips past the first part of the execute sub command
        sub_cmd_token = self.eat(TypedToken.STRING)
        self.eat(DelimiterToken.OPEN_PARENTHESES)

        # gets the attribute of "exec_sub_(sub_command)"
        method_name = f"exec_sub_{sub_cmd_token.value}_arg"
        exec_sub_arg_method = getattr(self, method_name, self.invalid_method) 

        # contains the list of nodes gotten from the arg method
        exec_sub_arg_nodes = []

        while True:
            exec_sub_arg_node = exec_sub_arg_method()
            exec_sub_arg_nodes.append(exec_sub_arg_node)

            if self.current_token.matches(DelimiterToken.COLON):
                self.advance()
            elif self.current_token.matches(DelimiterToken.CLOSE_PARENTHESES):
                break

        self.eat(DelimiterToken.CLOSE_PARENTHESES)

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
            block_node = self.block()

            if is_coord_token(self.current_token):
                coord_node = self.vec3()
            else:
                coord_node = None

            return ExecuteSubIfBlockArg(block_node, coord_node)

        else:
            raise NotImplementedError("1.13")
            

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

    def sb_players_math(self, begin_target, begin_objective=None):
        """
        sb_players_math ::= target && STR && ["=", "<=", ">=", "swap", "+=", "-=", "*=", "/=", "%="] && (signed_int | target && (STR)?)

        Returns:
            ScoreboardCmdMathNode: pass
            ScoreboardCmdMathValueNode: pass
        """

        if begin_objective is None:
            begin_objective = self.eat(TypedToken.STRING)
        operator = self.eat(TypedToken.STRING, values=Parser.sb_math_operators)

        if self.current_token.matches(DelimiterToken.AT):
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
        simple_cmd ::= [bossbar_cmd, effect_cmd, data_cmd, function_cmd, tag_cmd, team_cmd, xp_cmd, (COMMAND_KEYWORD && (STR, selector, nbt, json)*)]

        Note that a simple command can turn into a scoreboard command
        because "tp" can be a fake player name being set to a scoreboard value
        This will only happen if the 3rd token is a scoreboard operator
        """
        command_name = self.current_token.value
        if command_name not in self.config_data.command_names:
            self.error("Expected a command name (specifed under fena/src/config/command_names.json")

        # advances the command name
        command_name_token = self.advance()

        if command_name in ("bossbar", "data", "effect", "function", "tag", "team", "xp"):
            # for each command name, does something like self.bossbar_cmd()
            method_name = f"{command_name}_cmd"
            method = getattr(self, method_name, self.invalid_method)
            return method()

        # should get all values until the next newline
        if self.current_token.matches(WhitespaceToken.NEWLINE):
            return SimpleCmdNode([command_name_token])

        # if the second token exists and it is a string, it might still be a scoreboard shortcut
        if self.current_token.matches(TypedToken.STRING):
            second_token = self.eat(TypedToken.STRING)
            if self.current_token.value in Parser.sb_math_operators:
                return self.sb_players_math(begin_target=command_name_token, begin_objective=second_token)

            nodes = [command_name_token, second_token]
        else:
            nodes = [command_name_token]

        # STR, selector, nbt, json
        while not self.current_token.matches(WhitespaceToken.NEWLINE):
            if self.current_token.matches(DelimiterToken.AT):
                selector_node = self.selector()
                nodes.append(selector_node)

            elif self.current_token.matches(DelimiterToken.OPEN_CURLY_BRACKET):
                tag_node = self.curly_bracket_tag()
                nodes.append(tag_node)
            
            else:
                str_token = self.eat(TypedToken.STRING)
                nodes.append(str_token)

        return SimpleCmdNode(nodes)

    def curly_bracket_tag(self):
        """
        Chooses between parsing json or nbt by seeing if the first token is a literal string or not
        """
        self.eat(DelimiterToken.OPEN_CURLY_BRACKET)
        if self.current_token.matches(TypedToken.LITERAL_STRING):
            return self.json(past_curly_bracket=True)
        return self.nbt(past_curly_bracket=True)

    def bossbar_cmd(self):
        """
        bossbar_cmd ::= "bossbar" && [bossbar_add, bossbar_remove, bossbar_get, bossbar_set]
        """

        sub_cmd = self.current_token.value
        if sub_cmd == "add":
            return self.bossbar_add()
        if sub_cmd == "remove":
            return self.bossbar_remove()

        bossbar_id = self.bossbar_id()

        if self.current_token == "<-":
            return self.bossbar_get(bossbar_id)
        return self.bossbar_set(bossbar_id)

    def bossbar_add(self):
        """
        bossbar_add ::= "add" && bossbar_id && [json, STR]?
        """
        self.eat(TypedToken.STRING, value="add")
        bossbar_id = self.bossbar_id()

        if self.current_token.matches(DelimiterToken.OPEN_CURLY_BRACKET):
            json_node = self.json()
            return BossbarAddNode(bossbar_id, json_node)

        self.error("Expected a json object")

    def bossbar_remove(self):
        """
        bossbar_remove ::= "remove" && bossbar_id
        """
        self.eat(TypedToken.STRING, value="remove")
        bossbar_id = self.bossbar_id()
        return BossbarRemoveNode(bossbar_id)

    def bossbar_get(self, bossbar_id):
        """
        bossbar_get ::= bossbar_id && "<-" && ["max", "value", "players", "visible"]
        """
        self.eat(TypedToken.STRING, value="<-")
        sub_cmd = self.eat(TypedToken.STIRNG, values=Parser.config_data.bossbar_get)

        return BossbarGetNode(bossbar_id, sub_cmd)

    def bossbar_set(self, bossbar_id):
        """
        bossbar_set ::= bossbar_id && bossbar_arg && "=" && bossbar_arg_value
        # bossbar_option_arg, bossbar_option_arg_value are defined in the bossbar_version.json
        """
        arg_token, json_arg_details = self.json_parse_arg(json_type="bossbar_set")
        self.eat(DelimiterToken.EQUALS)
        arg_value_token = self.json_parse_arg_value(json_arg_details)

        return BossbarSetNode(bossbar_id, arg_token, arg_value_token)

    def bossbar_id(self):
        """
        bossbar_id ::= namespace_id
        """
        return self.namespace_id()

    def data_cmd(self):
        """
        data_cmd ::= "data" && [data_get, data_merge, data_remove]
        data_get ::= entity_vec3 && "<-" && (STR && (signed_int)?)?
        data_merge ::= entity_vec3 && "+" && nbt
        data_remove ::= entity_vec3 && "-" && STR
        """
        raise NotImplementedError

    def effect_cmd(self):
        """
        effect_cmd ::= "effect" && [effect_give, effect_clear]
        effect_clear ::= selector && "-" && ["all", effect_id]
        effect_give ::= selector && "+" && effect_id && (pos_int && ((nonneg_int)? && ["true", "false"]? )? )?
        # effect_id are defined under effects_version.txt
        """
        raise NotImplementedError

    def function_cmd(self):
        """
        function_cmd ::= "function" && STR
        """
        raise NotImplementedError

    def tag_cmd(self):
        """
        tag_cmd ::= "tag" && [tag_add, tag_remove]
        tag_add ::= selector && "+" && STR
        tag_remove ::= selector && "-" && STR
        """
        raise NotImplementedError

    def team_cmd(self):
        """
        team_cmd ::= "team" && [team_add, team_join, team_leave, team_empty, team_option, team_remove]
        team_add ::= "add" && STR && (STR)*
        team_join ::= STR && "+" && target
        team_leave ::= "leave" && target
        team_empty ::= "empty" && STR
        # team_option ::= STR && json_parse
        team_option ::= STR && team_option_arg && "=" && team_option_arg_value
        # team_option_arg, team_option_arg_value are defined in the team_options_version.json
        team_remove ::= "remove" && STR
        """
        raise NotImplementedError

    def xp_cmd(self):
        """
        xp_cmd ::= "xp" && [xp_math, xp_get]
        xp_math ::= ["=", "+", "-"] && nonneg_int && ["points", "levels"]?
        xp_get ::= "<-" && ["points", "levels"]
        """
        raise NotImplementedError

    def selector(self):
        """
        selector ::= selector_var & ("[" & selector_args & "]")?

        Returns:
            SelectorNode
        """
        # selector_var = self.eat(DelimiterToken.AT)
        selector_var = self.selector_var()

        if self.current_token.matches(DelimiterToken.OPEN_SQUARE_BRACKET):
            self.eat(DelimiterToken.OPEN_SQUARE_BRACKET)
            selector_args = self.selector_args()
            self.eat(DelimiterToken.CLOSE_SQUARE_BRACKET)
            return SelectorNode(selector_var, selector_args)

        return SelectorNode(selector_var)

    def selector_var(self):
        """
        selector_var ::= "@" & selector_var_specifier

        Returns:
            SelectorVarNode
        """
        self.eat(DelimiterToken.AT)
        specifier = self.selector_var_specifier()
        return SelectorVarNode(specifier)

    def selector_var_specifier(self):
        """
        # selector_var_specifier is defined under selector_version.json as "selector_variable_specifiers"

        Returns:
            Token with TypedToken.SELECTOR_VARIABLE_SPECIFIER
        """
        return self.eat(TypedToken.SELECTOR_VARIABLE_SPECIFIER, values=Parser.config_data.selector_variable_specifiers)

    def selector_args(self):
        """
        selector_args ::= (single_arg)? | (single_arg & ("," & single_arg)*)?

        Returns:
            SelectorArgsNode
        """
        # all individual lists for each different type of argument
        # this requires that dictionaries retain order (python 3.6)
        # otherwise, use an ordered dict
        all_selector_args = {
            SelectorDefaultArgNode: [],
            SelectorScoreArgNode: [],
            SelectorTagArgNode: [],
            SelectorNbtArgNode: [],
            SelectorAdvancementGroupArgNode: None,
        }

        if not self.current_token.matches(DelimiterToken.CLOSE_SQUARE_BRACKET):
            while self.current_token.matches_any_of(TypedToken.STRING, DelimiterToken.EXCLAMATION_MARK, DelimiterToken.OPEN_CURLY_BRACKET):
                selector_arg = self.single_arg()
                arg_type = type(selector_arg)

                # makes sure that the argument type is actually inside the dictionary
                # this is contained in an assert stmt because this should never happen
                assert arg_type in all_selector_args, f"Expected {arg_type} to be in {list(all_selector_args)}"

                # if it isn't a list, it only allows one argument
                if not isinstance(all_selector_args[arg_type], list):
                    if not all_selector_args[arg_type] is None:
                        self.error(f"Found an extra argument {selector_arg}")
                    all_selector_args[arg_type] = selector_arg
                all_selector_args[arg_type].append(selector_arg)

                if self.current_token.matches(DelimiterToken.COMMA):
                    self.advance()
                elif self.current_token.matches(DelimiterToken.CLOSE_SQUARE_BRACKET):
                    break
                else:
                    self.error("Expected a comma or closing square bracket")

            else:
                self.error("Expected a string or exclamation mark as a selector argument")

        default_args = all_selector_args[SelectorDefaultArgNode]
        score_args = SelectorScoreArgsNode(all_selector_args[SelectorScoreArgNode])
        tag_args = SelectorTagArgsNode(all_selector_args[SelectorTagArgNode])
        nbt_args = SelectorNbtArgsNode(all_selector_args[SelectorNbtArgNode])
        adv_args = all_selector_args[SelectorAdvancementGroupArgNode]
        if adv_args is None:
            adv_args = SelectorAdvancementGroupArgNode([])

        return SelectorArgsNode(default_args, score_args, tag_args, nbt_args, adv_args)

        # all_selector_args[SelectorNbtArgNode] = SelectorNbtArgsNode(all_selector_args[SelectorNbtArgNode])
        # return SelectorArgsNode(*all_selector_args.values())

    def single_arg(self):
        """
        single_arg ::= [simple_arg, score_arg, tag_arg, nbt_arg]
        """
        # note that this can be anything and it doesn't have to be specified under selector.json
        # literally can be any string, even if it matches a default arg
        negated = self.current_token.matches(DelimiterToken.EXCLAMATION_MARK)
        if negated:
            self.advance()

        # checks whether it is an nbt argument
        if self.current_token.matches(DelimiterToken.OPEN_CURLY_BRACKET):
            return self.nbt_arg(negated)

        selector_arg_token = self.eat(TypedToken.STRING)
        if not self.current_token.matches(DelimiterToken.EQUALS):
            return self.tag_arg(selector_arg_token, negated)

        # guaranteed to be a default arg
        # gets any replacements
        selector_arg = selector_arg_token.value
        replacement = Parser.config_data.selector_replacements.get(selector_arg, selector_arg)

        if replacement in Parser.config_data.selector_arguments:
            selector_arg_token.replacement = replacement
            return self.simple_arg(selector_arg_token)

        # otherwise, score arg
        return self.score_arg(selector_arg_token)

    def tag_arg(self, tag_arg, negated):
        """
        tag_arg ::= ("!")? & STR

        Args:
            tag_arg (Token)

        Returns:
            SelectorTagArgNode
        """
        return SelectorTagArgNode(tag_arg, negated)

    def score_arg(self, objective_arg):
        """
        score_arg ::= (STR & "=" & score_arg_value)

        Args:
            objective_arg (Token)

        Returns:
            SelectorScoreArgNode
        """
        self.eat(DelimiterToken.EQUALS)
        value = self.score_arg_value()
        return SelectorScoreArgNode(objective_arg, value)
    
    def score_arg_value(self):
        """
        score_arg_value ::= [int_range, "*"] | "(" & score_arg_value & ")"
        """
        if self.current_token.matches(TypedToken.STRING):
            value = self.eat(TypedToken.STRING, value="*", error_message="If the value is a string token, expected '*'")
        elif self.current_token.matches(DelimiterToken.OPEN_PARENTHESES):
            self.eat(DelimiterToken.OPEN_PARENTHESES)
            value = self.score_arg_value()
            self.eat(DelimiterToken.CLOSE_PARENTHESES)
        else:
            value = self.int_range()

        return value

    def nbt_arg(self, negated):
        """
        nbt_arg ::= ("!")? & nbt
        """
        nbt = self.nbt()
        return SelectorNbtArgNode(nbt, negated)

    def simple_arg(self, simple_arg_token):
        """
        simple_arg ::= default_arg & "=" & default_arg_value_group

        Returns:
            SelectorDefaultArgNode
        """
        json_arg_details = self.json_parse_arg(json_type="selector", arg_token=simple_arg_token)
        self.eat(DelimiterToken.EQUALS)
        default_arg_value = self.default_arg_value_group(json_arg_details)

        return SelectorDefaultArgNode(simple_arg_token, default_arg_value)

    def default_arg_value_group(self, json_arg_details):
        """
        default_arg_value_group = ("!")? & (default_arg_value | ("(" && default_arg_values && ")"))
        # default_arg_value is defined under selector_version.json as "selector_argument_details"

        Args:
            json_arg_details (dict): pass

        Returns:
            SelectorDefaultArgValueNode: if the value is a range, number or string
            SelectorDefaultGroupArgValueNode: if the value is actually a group surrounded by "(" and ")"
        """
        # checks for negation
        if (json_arg_details.get("negation", False) and self.current_token.matches(DelimiterToken.EXCLAMATION_MARK)):
            self.advance()
            negated = True
        else:
            negated = False

        # checks for group
        if json_arg_details.get("group", False) and self.current_token.matches(DelimiterToken.OPEN_PARENTHESES):
            if ((json_arg_details["group"] == "negation" and negated) or
                    (json_arg_details["group"] == "default" and not negated) or
                    (json_arg_details["group"] == "any")):
                group = True
            else:
                # open parenthesis shows there is a group defined in the wrong context
                self.error("Unknown base case for group")
        else:
            group = False

        # gets group values
        if group:
            self.eat(DelimiterToken.OPEN_PARENTHESES)
            value_nodes = self.default_arg_values(json_arg_details, negated)
            self.eat(DelimiterToken.CLOSE_PARENTHESES)

            return SelectorDefaultGroupArgValueNode(value_nodes)

        # gets one single argument
        arg_value_token = self.json_parse_arg_value(json_arg_details)
        return SelectorDefaultArgValueNode(arg_value_token, negated)

    def default_arg_values(self, json_arg_details, negated):
        """
        default_arg_values ::= (default_arg_value)? | (single_arg & ("," & single_arg)*)?
        # default_arg_value is defined under selector_version.json as "selector_argument_details"

        Returns:
            list: Contains any combination of Token, IntRangeNode and, NumberRangeNode objects
        """
        default_arg_values = []
        while not self.current_token.matches_any_of(DelimiterToken.CLOSE_PARENTHESES, DelimiterToken.COMMA):
            value = self.json_parse_arg_value(json_arg_details)
            arg_value = SelectorDefaultArgValueNode(value, negated)
            default_arg_values.append(arg_value)

            if self.current_token.matches(DelimiterToken.COMMA):
                self.advance()
            elif self.current_token.matches(DelimiterToken.CLOSE_PARENTHESES):
                break
            else:
                self.error("Expected a comma or closing parentheses")

        else:
            self.error("Expected a value for the group argument")

        return default_arg_values

    def adv_arg_group(self):
        raise NotImplementedError()

    def nbt_object(self, past_curly_bracket=False):
        """
        nbt_object ::= "{" && ((nbt_map)? | (nbt_map && ("," && nbt_map)*)) && "}"

        Returns:
            NbtObjectNode
        """
        mappings = []

        if not past_curly_bracket:
            self.eat(DelimiterToken.OPEN_CURLY_BRACKET)

        if not self.current_token.matches(DelimiterToken.CLOSE_CURLY_BRACKET):
            while self.current_token.matches(TypedToken.STRING):
                nbt_map = self.nbt_map()
                mappings.append(nbt_map)

                if self.current_token.matches(DelimiterToken.COMMA):
                    self.advance()
                elif self.current_token.matches(DelimiterToken.CLOSE_CURLY_BRACKET):
                    break
                else:
                    self.error("Expected a comma or closing curly bracket")

            else:
                self.error("Expected a literal string to begin a nbt map")

        self.eat(DelimiterToken.CLOSE_CURLY_BRACKET)

        return NbtObjectNode(mappings)

    # nbt ::= nbt_object
    nbt = nbt_object

    def nbt_map(self):
        """
        nbt_map ::= STR && ":" && nbt_value
        """
        arg = self.eat(TypedToken.STRING)
        self.eat(DelimiterToken.COLON)
        value = self.nbt_value()

        return NbtMapNode(arg, value)

    def nbt_array(self):
        """
        nbt_array ::= "[" && (nbt_array_begin && ";")? && nbt_value)? | (nbt_value && ("," && nbt_value)*) && "]"
        """
        # getes the type specifier if it exists
        self.eat(DelimiterToken.OPEN_SQUARE_BRACKET)
        nbt_values = []

        if self.current_token.matches(TypedToken.STRING):
            type_specifier = self.nbt_array_begin()
            self.eat(DelimiterToken.SEMICOLON)
        else:
            type_specifier = None

        if not self.current_token.matches(DelimiterToken.CLOSE_SQUARE_BRACKET):
            while self.current_token.matches_any_of(TypedToken.LITERAL_STRING, TypedToken.INT, TypedToken.FLOAT,
                    DelimiterToken.OPEN_CURLY_BRACKET, DelimiterToken.OPEN_SQUARE_BRACKET):
                nbt_value = self.nbt_value()
                nbt_values.append(nbt_value)

                if self.current_token.matches(DelimiterToken.COMMA):
                    self.advance()
                elif self.current_token.matches(DelimiterToken.CLOSE_SQUARE_BRACKET):
                    break
                else:
                    self.error("Expected a comma or closing square bracket")

            else:
                self.error("Expected a nbt value")

        self.eat(DelimiterToken.CLOSE_SQUARE_BRACKET)
        return NbtArrayNode(nbt_values, type_specifier=type_specifier)

    def nbt_array_begin(self):
        """
        nbt_array_begin ::= ["I", "L", "B"]
        """
        return self.eat(TypedToken.STRING, values=("I", "L", "B"))

    def nbt_value(self):
        """
        nbt_value ::= [literal_str, nbt_number, nbt_object, nbt_array]
        """
        if self.current_token.matches_any_of(DelimiterToken.OPEN_SQUARE_BRACKET):
            return self.nbt_array()
        if self.current_token.matches(TypedToken.LITERAL_STRING):
            return self.advance()
        if self.current_token.matches_any_of(TypedToken.INT, TypedToken.FLOAT):
            return self.nbt_number()
        if self.current_token.matches(DelimiterToken.OPEN_CURLY_BRACKET):
            return self.nbt_object()
        self.error("Unexpected default case")

    def nbt_number(self):
        """
        nbt_number = (signed_int & ["b", "s", "L"]?) | json_number & ["d", "f"]?
        """
        if self.current_token.matches(TypedToken.INT):
            int_value = self.advance()
            if self.current_token.matches(TypedToken.STRING):
                int_type = self.eat(TypedToken.STRING, values=("b", "s", "L"))
            else:
                int_type = None
            return NbtIntegerNode(int_value, int_type)

        if self.current_token.matches(TypedToken.FLOAT):
            float_value = self.advance()
            if self.current_token.matches(TypedToken.STRING):
                float_type = self.eat(TypedToken.STRING, values=("f", "d"))
            else:
                float_type = None
            return NbtFloatNode(float_value, float_type)
        
        self.error("Unexpected default case")

    def json_object(self, past_curly_bracket=False):
        """
        json_object ::= "{" && ((json_map)? | (json_map && ("," && json_map)*)) && "}"

        Returns:
            JsonObjectNode
        """
        mappings = []

        if not past_curly_bracket:
            self.eat(DelimiterToken.OPEN_CURLY_BRACKET)

        if not self.current_token.matches(DelimiterToken.CLOSE_CURLY_BRACKET):
            while self.current_token.matches(TypedToken.LITERAL_STRING):
                json_map = self.json_map()
                mappings.append(json_map)

                if self.current_token.matches(DelimiterToken.COMMA):
                    self.advance()
                elif self.current_token.matches(DelimiterToken.CLOSE_CURLY_BRACKET):
                    break
                else:
                    self.error("Expected a comma or closing curly bracket")

            # while else loop
            # this is only ran if the while loop ends with a false condition
            # if it ended with a "break", this is not called
            else:
                self.error("Expected a literal string to begin a json map")

        self.eat(DelimiterToken.CLOSE_CURLY_BRACKET)

        return JsonObjectNode(mappings)

    # json ::= json_object
    json = json_object

    def json_map(self):
        """
        json_map ::= literal_str && ":" && json_value
        """
        arg = self.eat(TypedToken.LITERAL_STRING)
        self.eat(DelimiterToken.COLON)
        value = self.json_value()

        return JsonMapNode(arg, value)

    def json_array(self):
        """
        json_array ::= "[" && ((json_value)? | (json_value && ("," && json_value)*)) && "]"
        """
        self.eat(DelimiterToken.OPEN_SQUARE_BRACKET)
        json_values = []

        if not self.current_token.matches(DelimiterToken.CLOSE_SQUARE_BRACKET):
            # matches any json value
            while self.current_token.matches_any_of(TypedToken.LITERAL_STRING, TypedToken.STRING, TypedToken.INT,
                    TypedToken.FLOAT, DelimiterToken.OPEN_CURLY_BRACKET, DelimiterToken.OPEN_SQUARE_BRACKET):
                json_value = self.json_value()
                json_values.append(json_value)

                if self.current_token.matches(DelimiterToken.COMMA):
                    self.advance()
                elif self.current_token.matches(DelimiterToken.CLOSE_SQUARE_BRACKET):
                    break
                else:
                    self.error("Expected a comma or closing square bracket")

            else:
                self.error("Expected a json value")

        self.eat(DelimiterToken.CLOSE_SQUARE_BRACKET)

        return JsonArrayNode(json_values)

    def json_value(self):
        """
        json_value ::= [literal_str, json_number, "true", "false", "null", json_object, json_array]
        """
        if self.current_token.matches(TypedToken.STRING):
            return self.eat(TypedToken.STRING, values=("true", "false", "null"))
        if self.current_token.matches_any_of(TypedToken.LITERAL_STRING, TypedToken.INT, TypedToken.FLOAT):
            return self.advance()
        if self.current_token.matches(DelimiterToken.OPEN_CURLY_BRACKET):
            return self.json_object()
        if self.current_token.matches(DelimiterToken.OPEN_SQUARE_BRACKET):
            return self.json_array()
        self.error("Unexpected default case")

    def json_number(self):
        """
        json_number ::= ("-")? && INT && ("." && INT)? && (["e", "E"] && ["+", "-"] && INT)?
        """
        raise NotImplementedError

    def nonneg_int(self):
        """
        nonneg_int ::= INT  # Z nonneg
        """
        if not is_nonneg_int(self.current_token.value):
            self.error("Expected a nonnegative integer (all integers greater than or equal to 0)")
        return self._get_int()

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
        token = self.eat(TypedToken.STRING, TypedToken.INT)
        # if token.matches(TypedToken.STRING):
        #     token.cast(TypedToken.INT)
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

    def int_range_bracket(self, args=()):
        if self.current_token.matches_any_of(TypedToken.INT, DelimiterToken.RANGE):
            return self.int_range(args)
        elif self.current_token.matches(DelimiterToken.OPEN_PARENTHESES):
            self.eat(DelimiterToken.OPEN_PARENTHESES)
            result = self.int_range_bracket(args)
            self.eat(DelimiterToken.CLOSE_PARENTHESES)
            return result
        else:
            self.error("Expected an integer, '..' or open parenthesis")

    def int_range(self, args=()):
        """
        int_range ::= [signed_int, (signed_int & ".."), (".." & signed_int), (signed_int & ".." & signed_int)]
        """
        min_int = None
        max_int = None

        if self.current_token.matches(TypedToken.INT):
            min_int = self.eat(TypedToken.INT)

        # if it isn't a singular integer, it requires a range
        if self.current_token.matches(DelimiterToken.RANGE):
            self.advance()
            if self.current_token.matches(TypedToken.INT):
                max_int = self.eat(TypedToken.INT)

        # singular integer
        else:
            max_int = min_int

        # a range cannot just be ".."
        if min_int is None and max_int is None:
            self.error("Expected at least one integer in an integer range")

        return IntRangeNode(min_int, max_int, args)

    def number_range_bracket(self):
        if self.current_token.matches_any_of(TypedToken.INT, TypedToken.FLOAT, DelimiterToken.RANGE):
            return self.number_range()
        elif self.current_token.matches(DelimiterToken.OPEN_PARENTHESES):
            self.eat(DelimiterToken.OPEN_PARENTHESES)
            result = self.number_range_bracket()
            self.eat(DelimiterToken.CLOSE_PARENTHESES)
            return result
        else:
            self.error("Expected an integer, '..' or open parenthesis")

    def number_range(self):
        """
        number_range ::= [signed_float, (signed_float & ".."), (".." & signed_float), (signed_float & ".." & signed_float)]
        """
        min_num = None
        max_num = None

        if self.current_token.matches_any_of(TypedToken.INT, TypedToken.FLOAT):
            min_num = self.advance()

        # if it isn't a singular integer, it requires a range
        if self.current_token.matches(DelimiterToken.RANGE):
            self.advance()
            if self.current_token.matches_any_of(TypedToken.INT, TypedToken.FLOAT):
                max_num = self.advance()

        # singular number
        else:
            max_num = min_num

        # a range cannot just be ".."
        if min_num is None and max_num is None:
            self.error("Expected at least one number in a number range")

        return NumberRangeNode(min_num, max_num)

    def target(self):
        """
        target ::= [selector, STR]

        Returns:
            SelectorNode or Token
        """
        if self.current_token.matches(DelimiterToken.AT):
            return self.selector()

        return self.eat(TypedToken.STRING)

    def entity_vec3(self):
        """
        entity_vec3 ::= [selector, vec3]

        Returns:
            SelectorNode or Vec3Node
        """
        if self.current_token.matches(DelimiterToken.AT):
            return self.selector()

        return self.vec3()
    
    def entity_id(self):
        """
        entity_id ::= ("minecraft" & ":")? & entity_name
        """
        if self.current_token.matches(TypedToken.STRING, value="minecraft"):
            self.advance()
            self.eat(DelimiterToken.COLON)

        arg_value = self.current_token.value
        if arg_value not in Parser.config_data.entities:
            self.error("Expected an entity type")

        entity_token = self.eat(TypedToken.STRING)
        return NamespaceIdNode(entity_token)
        # entity_token = self.eat(TypedToken.STRING)
        # entity_token.replacement = "minecraft:" + entity_token.value
        # return entity_token

    def vec2(self):
        """
        vec2 ::= coord && coord

        Returns:
            Vec2Node
        """
        coords_node = self._coords(3)
        assert_type(coords_node, Vec3Node)
        return coords_node

    def vec3(self):
        """
        vec3 ::= coord && coord && coord

        Returns:
            Vec3Node
        """
        coords_node = self._coords(3)
        assert_type(coords_node, Vec3Node)
        return coords_node

    def _coords(self, coord_num):
        """
        Returns:
            Vec2Node or Vec3Node
        """
        assert coord_num in (2, 3)

        coords = []
        for _ in range(coord_num):
            if is_coord_token(self.current_token):
                coord = self.eat(TypedToken.STRING)
                coords.append(coord)
            else:
                self.error("Expected a coord token")

        if not are_coords(*coords):
            coords_str = " ".join(str(c) for c in coords)
            self.error(f"Expected a proper coord type given all coordinates ({coords_str})")

        # pylint to disable possible error with the length of the coords object
        if coord_num == 2:
            # pylint: disable-msg=E1120
            return Vec2Node(*coords)
        elif coord_num == 3:
            # pylint: disable-msg=E1120
            return Vec3Node(*coords)
        else:
            self.error("Unknown base case")

    def block(self):
        """
        block ::= block_id & ("[" & (block_states)? & "]")? & (nbt)?
        block_id ::= ("minecraft" && ":")? && block_type
        # block_type is defined under blocks.json

        Returns:
            BlockNode
        """
        if self.current_token.value not in Parser.config_data.blocks:
            self.error("Expected a block inside the if argument")

        block_type = self.eat(TypedToken.STRING)

        # checks for block states
        if self.current_token.matches(DelimiterToken.OPEN_SQUARE_BRACKET):
            self.advance()
            block_states = self.block_states()
            self.eat(DelimiterToken.CLOSE_SQUARE_BRACKET)
        else:
            block_states = None

        if self.current_token.matches(DelimiterToken.OPEN_CURLY_BRACKET):
            nbt = self.nbt()
        else:
            nbt = None

        return BlockNode(block_type, block_states, nbt)

    def block_id(self):
        """
        block_id ::= ("minecraft" && ":")? && block_type
        """
        raise NotImplementedError

    def block_type(self):
        """
        # block_type is defined under blocks.json
        """
        raise NotImplementedError

    def block_states(self):
        """
        block_states ::= (block_state)? | (block_state & ("," & block_state)*)?
        """
        raise NotImplementedError

    def block_state(self):
        """
        block_state ::= STR && "=" && STR
        """
        raise NotImplementedError

    def namespace_id(self):
        """
        namespace_id ::= STR && (":" && STR)?
        """
        # possible namespace if ":" exists
        # otherwise, namespace is the id_value
        id_value = self.eat(TypedToken.STRING)

        if self.current_token.matches(DelimiterToken.COLON):
            self.advance()
            namespace = id_value
            id_value = self.eat(TypedToken.STRING)
            return NamespaceIdNode(id_value, namespace)

        return NamespaceIdNode(id_value)

    def __repr__(self):
        return f"Parser[iterator={self.iterator!r}, current_token={self.current_token!r}]"

if __name__ == "__main__":
    from fena.lexer import Lexer

    logging_setup.format_file_name("test_lexer.txt")

    # with open("test_lexer.txt") as file:
    #     text = file.read()
    # lexer = Lexer(text)

    # r"C:\Users\Austin-zs\AppData\Roaming\.minecraft\saves\Snapshot 17w18b\data\functions\ego\event_name"
    # parser = Parser(lexer)

    # try:
    #     parser.parse()
    # except Exception as e:
    #     logging.exception(e)

    # mcfunctions = parser.mcfunctions
    # for mcfunction in mcfunctions:
    #     logging.debug("")
    #     logging.debug(str(mcfunction))
    #     for command in mcfunction.commands:
    #         logging.debug(repr(command))

    # lexer = Lexer("@e[x=-153,y=0,z=299,dx=158,dy=110,dz=168,m=2,c=5, team=bruh,name=lol, a_tag.of.epic_proportions, RRar=3..5, type=cow, dist=2..4, lvl=5, x_rot=..7, y_rot=1..]")
    # parser = Parser(lexer.get_selector())
    # tree = parser.selector()
    # print(tree)

    import traceback

    def test(string, lexer_method, parser_method, expect_error=False):
        print(f"    {string}:")
        try:
            lexer = Lexer(string)
            parser = Parser(lexer, lexer_method)
            ast = parser.parse(method_name=parser_method)
        except Exception:
            if expect_error:
                print(f"success: expected error")
            else:
                print(f"failure: did not expect error")
                raise Exception
        else:
            if expect_error:
                print(f"failure: expected error for {ast!r}")
                raise Exception
            else:
                print(f"success: {ast!r}")

        print()
    
    def test_cmd(cmd, expect_error=False):
        test(cmd, "get_command", "command", expect_error)

    def tests_bossbar():
        test_cmd(r'bossbar add ayylmao {"text":"oh damn it is json","color":"yo mama"}')
        test_cmd(r'bossbar add nou:ayylmao {"text":"oh damn it is json","color":"yo mama"}')
        test_cmd(r'bossbar remove ayylmao')
        test_cmd(r'bossbar remove minecraft:ayylmao')
        test_cmd(r'bossbar minecraft:ayylmao color = nou', expect_error=True)
        test_cmd(r'bossbar minecraft:ayylmao color = green')
        test_cmd(r'bossbar minecraft:ayylmao max = -1', expect_error=True)
        test_cmd(r'bossbar minecraft:ayylmao max = 0', expect_error=True)
        test_cmd(r'bossbar minecraft:ayylmao max = 1')
        test_cmd(r'bossbar minecraft:ayylmao name = 1', expect_error=True)
        test_cmd(r'bossbar minecraft:ayylmao name = {}')
        test_cmd(r'bossbar minecraft:ayylmao name = {"text":"yo mama"}')

    def test_json(json, expect_error=False):
        test(json, "get_curly_bracket_tag", "json", expect_error)

    def tests_json():
        test_json(r'{"asdf":1, "asdf2":2, "asdf3":3}')
        test_json(r'{"asdf":1, "asdf2":2}')
        test_json(r'{"asdf":1}')
        test_json(r'{"asdf": [{"arg": "value"}, 1, 1.2, 1e1, 1.2e1, 1.2e+1, [1, 2, 3], "hello", true, false, null]}')
        test_json(r'{}')
        test_json(r'{"test":1, "test":2, "test":3, }', expect_error=True)
        test_json(r'{"asdf', expect_error=True)
        test_json(r'{"asdf":1}a', expect_error=True)

    def test_selector(selector, expect_error=False):
        test(selector, "get_selector", "selector", expect_error)

    def tests_selector():
        test_selector("@a")
        test_selector("@p")
        test_selector("@3", expect_error=True)
        test_selector("@e[type=armor_stand]")
        test_selector("@e[type=armor_stand,c=1]")

    # tests_bossbar()
    # tests_json()
    # tests_selector()
    # test_json(r'{"nou":[1, 2,]}', expect_error=True)
    test(r'{HurtByTimestamp: 0, Attributes: [{Base: 1.0E7d, Name: "generic.maxHealth"}, {Base: 0.0d, Name: "generic.knockbackResistance"}, {Base: 0.25d, Name: "generic.movementSpeed"}, {Base: 0.0d, Name: "generic.armor"}, {Base: 0.0d, Name: "generic.armorToughness"}, {Base: 16.0d, Modifiers: [{UUIDMost: 5954586636154850795L, UUIDLeast: -5021346310275855673L, Amount: -0.012159221696308982d, Operation: 1, Name: "Random spawn bonus"}], Name: "generic.followRange"}], Invulnerable: 0b, FallFlying: 0b, ForcedAge: 0, PortalCooldown: 0, AbsorptionAmount: 0.0f, Saddle: 0b, FallDistance: 0.0f, InLove: 0, DeathTime: 0s, HandDropChances: [0.085f, 0.085f], PersistenceRequired: 0b, Age: 0, Motion: [0.0d, -0.0784000015258789d, 0.0d], Leashed: 0b, UUIDLeast: -8543204344868739349L, Health: 79.2f, LeftHanded: 0b, Air: 300s, OnGround: 1b, Dimension: 0, Rotation: [214.95569f, 0.0f], HandItems: [{}, {}], ArmorDropChances: [0.085f, 0.085f, 0.085f, 0.085f], UUIDMost: 900863262324051519L, Pos: [724.3034218419358d, 4.0d, 280.78117600802693d], Fire: -1s, ArmorItems: [{}, {}, {}, {}], CanPickUpLoot: 0b, HurtTime: 0s}', "get_curly_bracket_tag", "nbt")

    # import doctest
    # doctest.testmod()
