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
from exec_nodes import ExecuteCmdNode_1_12, ExecuteCmdNode_1_13, ExecuteSubCmdNode_1_12, ExecuteSubIfArgBlock
from node_visitors import NodeBuilder, NodeVisitor
from coord_utils import is_coord_token
from config_data import ConfigData
from number_utils import is_signed_int

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
simple_cmd ::= [team_cmd, tag_cmd, data_cmd, bossbar_cmd, effect_cmd, function_cmd, (COMMAND_KEYWORD && (STR)*)]

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
exec_sub_rot_arg ::= [vec3, selector]
exec_sub_anchor_arg ::= ["feet", "eyes"]
exec_sub_in_arg ::= ["overworld", "nether", "end"]
exec_sub_ast_arg ::= selector

exec_sub_if_arg ::= [exec_sub_if_arg_selector, exec_sub_if_arg_block, exec_sub_if_arg_blocks, exec_sub_if_arg_compare, exec_sub_if_arg_range]
exec_sub_if_arg_selector ::= selector
exec_sub_if_arg_block ::= block && (vec3)?
exec_sub_if_arg_blocks ::= vec3 && vec3 && "==" && vec3 && ["all", "masked"]?
exec_sub_if_arg_compare ::= (target)? && STR && ["==", "<", "<=", ">", ">="] && (target && STR) | (INT)
exec_sub_if_arg_range ::= (target)? && STR && in && range
exec_sub_ifnot_arg ::= exec_sub_if_arg
exec_sub_unless_arg ::= exec_sub_if_arg

exec_sub_result_arg ::= [exec_sub_result_arg_data, exec_sub_result_arg_score, exec_sub_result_arg_bossbar]
exec_sub_result_arg_data ::= [vec3, selector] && STR && (data_type)? && signed_int
exec_sub_result_arg_score ::= selector && STR
exec_sub_result_arg_bossbar ::= STR && ["max", "value"]
exec_sub_success_arg ::= exec_sub_result_arg 

sb_cmd ::= [sb_players_math, sb_players_special]
sb_players_math ::= target && STR && ["=", "<=", ">=", "swap", "+=", "-=", "*=", "/=", "%="] && (signed_int | target && (STR)?)
sb_players_special ::= target && ["enable", "reset", "<-"] && STR

team_cmd ::= "team" && [team_add, team_join, team_leave, team_empty, team_option, team_remove]
team_add ::= "add" && STR && (STR)*
team_join ::= STR && "+=" && target
team_leave ::= "leave" && target
team_empty ::= "empty" && STR
team_option ::= STR && team_option_arg && "=" && team_option_arg_value
# team_option_arg, team_option_arg_value are defined in the team_options_version.json
team_remove ::= "remove" && STR

tag_cmd ::= "tag" && [tag_add, tag_remove]
tag_add ::= selector && "+=" && STR
tag_remove ::= selector && "-=" && STR

data_cmd ::= "data" && [data_get, data_merge, data_remove]
data_get ::= [selector, vec3] && "<-" && (STR && (signed_int)?)?
data_merge ::= [selector, vec3] && "+=" && nbt_tag
data_remove ::= [selector, vec3] && "-=" && STR

bossbar_cmd ::= "bossbar" && [bossbar_add, bossbar_remove, bossbar_get, bossbar_set_]
bossbar_add ::= STR && json
bossbar_remove ::= STR
bossbar_get ::= STR && "<-" && ["max", "value", "players", "visible"]
bossbar_set_max ::= STR && "max" && "=" && pos_int
bossbar_set_value ::= STR && "value" && "=" && nonneg_int
bossbar_set_players ::= STR && "players" && "=" && selector
bossbar_set_visible ::= STR && "=" && ["visible", "invisible"]
bossbar_set_color ::= STR && "color" && "=" && ["white", "pink", "red", "yellow", "green", "blue", "purple"]
bossbar_set_style ::= STR && "color" && "=" && ["0", "6", "10", "12", "20"]

effect_cmd ::= "effect" && [effect_give, effect_clear]
effect_clear ::= selector && "-" && ["all", effect_id]
effect_give ::= selector && "+" && effect_id && (pos_int && ((nonneg_int)? && ["true", "false"]? )? )?
# effect_id are defined under effects_version.txt

function_cmd ::= "function" && STR

selector ::= selector_var & ("[" & selector_args & "]")?
# selector_var is defined under selector_version.json as "selector_variables"
selector_args ::= (single_arg)? | (single_arg & ("," & single_arg)*)?
single_arg ::= [simple_arg, range_arg, tag_arg]

simple_arg ::= default_arg & "=" & ("!")? & [STR, signed_int]
# default_arg is defined under selector_version.json as "selector_arguments"
tag_arg ::= STR
range_arg ::= STR & ("=" & range)?
range ::= [nonneg_int, (nonneg_int & ".."), (".." & nonneg_int), (nonneg_int & ".." & nonneg_int)]

nonneg_int ::= INT  # Z nonneg
signed_int ::= ("-")? && INT  # Z
pos_int ::= INT, ::/= 0  # Z+

float ::= (INT)? && "." && INT  # R, R <= 0
signed_float ::= ("-")? && float  # R

target ::= [selector, STR]
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

    def eat(self, *token_types, values=None, error_message=None):
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

        if (self.current_token.matches_any_of(*token_types) and
                (values is None or (self.current_token.value in values and self.current_token.type in ALL_TYPED_TOKEN_TYPES))):
            return self.advance()

        if error_message is None:
            if len(token_types) == 1:
                error_message = "Expected {}".format(token_types[0])
            else:
                error_message = "Expected one of {}".format(token_types)

        if values is not None:
            error_message += " with any value from {}".format(values)

        self.error(error_message)

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
        while self.current_token.matches_any_of(WhitespaceSimpleToken.NEWLINE, TypedToken.STRING, SelectorTypedToken.SELECTOR_VARIABLE):
            # base case is if a newline is not met
            if self.current_token.matches(WhitespaceSimpleToken.NEWLINE):
                self.eat(WhitespaceSimpleToken.NEWLINE)

            elif self.current_token.matches_any_of(TypedToken.STRING, SelectorTypedToken.SELECTOR_VARIABLE):
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

        mfunc_token = self.eat(TypedToken.STRING, error_message="Expected a string after a mfunc statement")

        name = mfunc_token.value + ".mcfunction"
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

        return McFunctionNode(name, command_nodes)

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

        return FolderNode(folder_token.value, statement_nodes)

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
        return PrefixNode(prefix_token.value)

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
        return ConstObjNode(constobj_token.value)

    def command(self):
        """
        command ::= (execute_cmd && ":")? && [sb_cmd, function_cmd, simple_cmd]

        Returns:
            FenaCmdNode
        """
        command_segment_nodes = []

        # gets either the execute command or a scoreboard shortcut command
        if self.current_token.matches(SelectorTypedToken.SELECTOR_VARIABLE):
            selector_begin_node = self.selector_begin_cmd()
            command_segment_nodes.append(selector_begin_node)
        elif (Parser.config_data.version == "1.13" and 
                self.current_token.value in TokenValues.get(ExecuteSimpleToken) or is_coord_token(self.current_token)):
            execute_node = self.execute_cmd()
            command_segment_nodes.append(execute_node)

        if not self.current_token.matches(WhitespaceSimpleToken.NEWLINE):
            # guaranteed to be a scoreboard shortcut command with a selector
            if self.current_token.matches(SelectorTypedToken.SELECTOR_VARIABLE):
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
                self.current_token.matches_any_of(SelectorTypedToken.SELECTOR_VARIABLE, SimpleToken.COLON)):
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
            execute_node = ExecuteSubCmdNode_1_12(selector=selector_node, coords=coords_node, sub_if=exec_sub_if_nodes)
            execute_nodes.append(execute_node)

            begin_selector = None
            if self.current_token.matches(SimpleToken.COLON):
                self.advance()
                break

            return ExecuteCmdNode_1_12(execute_nodes)

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

        execute_node = ExecuteCmdNode_1_13(execute_nodes)
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

            return ExecuteSubIfArgBlock(block_token, coord_node, version="1.12")

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

        if self.current_token.value in ("enable", "reset", "<-"):
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
        valid_operators = frozenset({"=", "<=", ">=", "swap", "+=", "-=", "*=", "/=", "%="})

        begin_objective = self.eat(TypedToken.STRING)
        operator = self.eat(TypedToken.STRING, values=valid_operators)

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
        sub_cmd = self.eat(TypedToken.STRING)
        objective = self.eat(TypedToken.STRING)

        return ScoreboardCmdSpecialNode(target, sub_cmd, objective)


    def simple_cmd(self):
        """
        Note that a simple command can turn into a scoreboard command
        because "tp" can be a fake player name being set to a scoreboard value
        """
        pass

    def selector(self):
        """
        """
        pass

    def vec3(self):
        """
        """
        pass

    def target(self):
        pass
    
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
