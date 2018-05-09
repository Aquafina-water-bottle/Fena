from abc import ABC
from config_data import ConfigData
from in_file_config import InFileConfig
from builder import Builder
from lexical_token import Token

in_file_config = InFileConfig()
config_data = ConfigData()

class Node(ABC):
    pass

class CmdNode(Node, ABC):
    pass

class StmtNode(Node, ABC):
    pass

class ProgramNode(Node):
    """
    Holds all statements found inside the global scope of the program

    Attributes:
        statement_nodes (list of McFunctionNodes, FolderNodes, PrefixNodes, ConstObjNodes)
    """
    def __init__(self, statement_nodes):
        assert isinstance(statement_nodes, list)
        self.statement_nodes = statement_nodes

class McFunctionNode(StmtNode):
    """
    Holds a single mcfunction with its full path and all fena command nodes

    Attributes:
        name (Token): The mcfunction name
        command_nodes (list of CommandNode objects)
    """
    def __init__(self, full_path, command_nodes):
        assert isinstance(full_path, Token)
        assert isinstance(command_nodes, list)
        self.full_path = full_path
        self.command_nodes = command_nodes

class FolderNode(StmtNode):
    """
    Holds all statements found inside a folder node

    Attributes:
        folder (Token)
        statement_nodes (list of McFunctionNodes, FolderNodes, PrefixNodes, ConstObjNodes)
    """
    def __init__(self, folder, statement_nodes):
        assert isinstance(folder, Token)
        assert isinstance(statement_nodes, list)
        self.folder = folder
        self.statement_nodes = statement_nodes

class PrefixNode(StmtNode):
    """
    Attributes:
        prefix (Token)
    """
    def __init__(self, prefix):
        assert isinstance(prefix, Token)
        self.prefix = prefix

class ConstObjNode(StmtNode):
    """
    Attributes:
        constobj (Token)
    """
    def __init__(self, constobj):
        assert isinstance(constobj, Token)
        self.constobj = constobj

class FenaCmdNode(CmdNode):
    """
    Holds all command segments for a command node

    Args:
        command_segment_nodes (list of specialized CmdNode objects)
    
    Attributes:
        execute_node (ExecuteCmdNode)
        scoreboard_node (ScoreboardCmdNode) 
        function_node (FunctionCmdNode)
        simple_node (SimpleCmdNode)
    """
    def __init__(self, command_segment_nodes):
        self.command_segment_nodes = command_segment_nodes

    def build(self):
        return " ".join(x.build() for x in self.command_segment_nodes)


class ExecuteCmdNode_1_12(CmdNode):
    def __init__(self, sub_cmd_nodes):
        self.sub_cmd_nodes = sub_cmd_nodes

    def build(self):
        return " ".join(x.build() for x in self.sub_cmd_nodes)

class ExecuteSubCmdNode_1_12(CmdNode):
    """
    Attributes:
        selector (SelectorNode)
        coords (Vec3Node)
        sub_if (ExecuteSubIfArgBlock)
    """
    def __init__(self, selector, coords, sub_if):
        assert isinstance(selector, SelectorNode)
        assert isinstance(coords, Vec3Node)
        assert isinstance(sub_if, ExecuteSubIfArgBlock)

        self.selector = selector
        self.coords = coords
        self.sub_if = sub_if

    def build(self):
        if self.coords is None:
            coords = "~ ~ ~"
        else:
            coords = self.coords.build()
        selector = self.selector.build()

        if self.sub_if is None:
            return f"execute {selector} {coords}"
        else:
            sub_if = self.sub_if.build()
            return f"execute {selector} {coords} {sub_if}"

class ExecuteCmdNode_1_13(CmdNode):
    """
    Attributes:
        exec_sub_cmd_nodes (list of children types of ExecuteSubIfArg)
    """
    def __init__(self, exec_sub_cmd_nodes):
        assert isinstance(exec_sub_cmd_nodes, list)
        self.exec_sub_cmd_nodes = exec_sub_cmd_nodes 

    def build(self):
        return " ".join(x.build() for x in self.exec_sub_cmd_nodes)

class ExecuteSubAsArg(CmdNode):
    pass

class ExecuteSubPosArg(CmdNode):
    pass

class ExecuteSubAtArg(CmdNode):
    pass

class ExecuteSubFacingArg(CmdNode):
    pass

class ExecuteSubRotArg(CmdNode):
    pass

class ExecuteSubAnchorArg(CmdNode):
    pass

class ExecuteSubAstArg(CmdNode):
    pass

class ExecuteSubInArg(CmdNode):
    pass


class ExecuteSubIfArg(CmdNode):
    """
    Args:
        negated (bool): Whether the statement argument should be negated or not when built

    Attributes:
        sub_cmd (str): Either "if" if negated is false, or "unless" if negated is true
    """
    def __init__(self, negated):
        assert isinstance(negated, bool)
        self.sub_cmd = ("unless" if negated else "if")

class ExecuteSubIfArgSelector(ExecuteSubIfArg):
    """
    Args:
        selector (SelectorNode)

    Usage:
        if(selector) -> if entity selector
    """
    def __init__(self, selector, negated=False):
        assert isinstance(selector, SelectorNode)

        super().__init__(negated)
        self.selector = selector

    def build(self):
        selector = self.selector.build()
        return f"{self.sub_cmd} entity {selector}"

class ExecuteSubIfArgBlock(ExecuteSubIfArg):
    """
    Args:
        block (BlockNode)
        coords (CoordNode or None)
        version (str): Minecraft version

    Usage:
        if(block_type) -> if(block_type ~ ~ ~)
        if(block_type vec3) -> if block vec3 block_type
    """
    def __init__(self, block, coords, negated=False, version="1.13"):
        super().__init__(negated)
        self.block = block
        self.coords = coords
        self.version = version

    def build(self):
        if self.coords is None:
            coords = "~ ~ ~"
        else:
            coords = self.coords.build()

        block = self.block.build()
        if self.version == "1.12":
            return f"detect {coords} {block}"
        return f"{self.sub_cmd} block {coords} {block}"
    
class ExecuteSubIfArgBlocks(ExecuteSubIfArg):
    """
    Args:
        coords1 (CoordNode)
        coords2 (CoordNode)
        coords3 (CoordNode)
        masked (bool)
    
    Usage:
        if(vec3 vec3 == vec3) -> if(vec3 vec3 == vec3 all) -> if blocks vec3 vec3 vec3 all
        if(vec3 vec3 == vec3 masked) -> if blocks vec3 vec3 vec3 masked
    """
    def __init__(self, coords1, coords2, coords3, masked=False, negated=False):
        super().__init__(negated)
        self.coords1 = coords1
        self.coords2 = coords2
        self.coords3 = coords3
        self.masked = masked

    def build(self):
        if self.masked:
            cmd_param = "masked"
        else:
            cmd_param = "all"
            
        coords1 = self.coords1.build()
        coords2 = self.coords2.build()
        coords3 = self.coords3.build()
        return f"{self.sub_cmd} blocks {coords1} {coords2} {coords3} {cmd_param}"

class ExecuteSubIfArgCompareEntity(ExecuteSubIfArg):
    """
    Args:
        selector1 (SelectorNode)
        objective1 (Token)
        operator (Token)
        selector2 (SelectorNode)
        objective2 (Token)

    Usage:
        if(target objective operator target2 objective2) -> if score target objective operator target2 objective
    """
    valid_operators = frozenset({"==", "<", "<=", ">", ">="})

    def __init__(self, selector1, objective1, operator, selector2, objective2, negated=False):
        super().__init__(negated)
        self.selector1 = selector1
        self.objective1 = objective1
        self.operator = operator
        self.selector2 = selector2
        self.objective2 = objective2

        if self.operator.value not in ExecuteSubIfArgCompareEntity.valid_operators:
            raise SyntaxError("{}: Invalid operator type, operators must be within {}".format(self.operator, ExecuteSubIfArgCompareEntity.valid_operators))

    def build(self):
        return "{} score {} {} {} {} {}".format(
            self.sub_cmd, self.selector1.build(), self.objective1.build(prefix=True),
            self.operator.build(replacements={"==": "="}), self.selector2.build(), self.objective2.build(prefix=True))

class ExecuteSubIfArgCompareInt(ExecuteSubIfArg):
    """
    Args:
        selector (SelectorNode)
        objective (Token)
        operator (Token)
        value (Token)

    Usage:
        if(target objective == int) -> if score target objective matches int
        if(target objective < int) -> if score target objective matches ..(int-1)
        if(target objective <= int) -> if score target objective matches ..(int)
        if(target objective > int) -> if score target objective matches (int+1)..
        if(target objective >= int) -> if score target objective matches (int)..
    """
    valid_operators = frozenset({"==", "<", "<=", ">", ">="})

    def __init__(self, selector, objective, operator, value, negated=False):
        super().__init__(negated)
        self.selector = selector
        self.objective = objective
        self.operator = operator
        self.value = value

        if self.operator.value not in ExecuteSubIfArgCompareInt.valid_operators:
            raise SyntaxError("{}: Invalid operator type, operators must be within {}".format(self.operator, ExecuteSubIfArgCompareInt.valid_operators))

    def build(self):
        int_value = self.value.value
        if self.operator.value == "==":
            int_range = int_value
        elif self.operator.value == "<":
            int_range = "..{}".format(int_value-1)
        elif self.operator.value == "<=":
            int_range = "..{}".format(int_value)
        elif self.operator.value == ">":
            int_range = "{}..".format(int_value+1)
        elif self.operator.value == ">=":
            int_range = "{}..".format(int_value)
        else:
            raise SyntaxError("Unknown default case")

        return "{} score {} {} matches {}".format(self.sub_cmd, self.selector.build(), self.objective.build(prefix=True), int_range)

class ExecuteSubIfArgRange(ExecuteSubIfArg):
    """
    Args:
        selector1 (SelectorNode)
        objective1 (Token)
        int_range (RangeNode)

    Usage:
        if(target objective in int..int) -> if score target objective matches int..int
    """
    def __init__(self, selector, objective, int_range, negated=False):
        super().__init__(negated)
        self.selector = selector
        self.objective = objective
        self.int_range = int_range

    def build(self):
        return "{} score {} {} matches {}".format(self.sub_cmd, self.selector.build(), self.objective.build(prefix=True), self.int_range.build())


class ExecuteSubResultArg(CmdNode):
    pass

# class ExecuteSubSuccessArg(CmdNode):
#     pass


class ScoreboardCmdMathNode(CmdNode):
    """
    Args:
        begin_target (SelectorNode or Token)
        begin_objective (Token)
        operator (Token)
        end_target (SelectorNode or Token)
        end_objective (Token or None)
    """

    def __init__(self, begin_target, begin_objective, operator, end_target, end_objective=None):
        self.begin_target = begin_target
        self.begin_objective = begin_objective
        self.operator = operator
        self.end_target = end_target
        self.end_objective = end_objective

    def build(self):
        begin_target = self.begin_target.build()
        begin_objective = self.begin_objective.build()
        operator = self.operator.build()
        end_target = self.end_target.build()
        end_objective = self.end_objective.build()
        return f"scoreboard players operation {begin_target} {begin_objective} {operator} {end_target} {end_objective}"

class ScoreboardCmdMathValueNode(CmdNode):
    """
    Args:
        target (SelectorNode or Token)
        objective (Token)
        operator (Token)
        value (Token)
    """
    def __init__(self, target, objective, operator, value):
        self.target = target
        self.objective = objective
        self.operator = operator
        self.value = value

    def build(self):
        target = self.target.build()
        objective = self.objective.build()
        operator = self.operator.build()
        value = self.value.build()
        constobj = in_file_config.constobj

        if operator == "=":
            return f"scoreboard players set {target} {objective} {value}"
        elif operator == "+=":
            return f"scoreboard players add {target} {objective} {value}"
        elif operator == "-=":
            return f"scoreboard players add {target} {objective} {value}"
        elif operator in ("*=", "/=", "%="):
            return f"scoreboard players operation {target} {objective} {operator} {value} {constobj}"
        elif operator == "<=":
            # sets the target to the score if and only if the target has a larger score compared to the value
            # therefore making the target score less than or equal to the value
            return f"scoreboard players operation {target} {objective} < {value} {constobj}"
        elif operator == ">=":
            # sets the target to the score if and only if the target has a smaller score compared to the value
            # therefore making the target score greater than or equal to the value
            return f"scoreboard players operation {target} {objective} > {value} {constobj}"
        elif operator in ("swap"):
            # no reason to swap with a constant value
            raise SyntaxError("Cannot swap with a constant value")
        else:
            raise SyntaxError("Unknown default case")

class ScoreboardCmdSpecialNode(CmdNode):
    """
    Args:
        target (SelectorNode or Token)
        sub_cmd (Token)
        objective (Token)
    """
    def __init__(self, target, sub_cmd, objective):
        self.target = target
        self.sub_cmd = sub_cmd
        self.objective = objective

        assert self.sub_cmd in ("enable", "reset", "<-")

    def build(self):
        sub_cmd = self.sub_cmd.build(replacements={"<-": "get"})
        target = self.target.build()
        objective = self.objective.build(prefix=True)
        return f"scoreboard players {sub_cmd} {target} {objective}"

class FunctionCmdNode(CmdNode):
    """
    Attributes:
        function_name (str): The mcfunction shortcut for the mcfunction name
    """
    def __init__(self, function_name):
        assert isinstance(function_name, str)
        self.function_name = function_name

    def build(self):
        function = in_file_config.functions[self.function_name]
        return f"function {function}"

class SimpleCmdNode(CmdNode):
    """
    Attributes:
        tokens (list of Token objects)
    """
    def __init__(self, tokens):
        assert isinstance(tokens, list)
        self.tokens = tokens
    
    def build(self):
        return " ".join(x.build() for x in self.tokens)

class TeamCmdNode(CmdNode):
    """
    team_cmd ::= "team" && [team_add, team_join, team_leave, team_empty, team_option, team_remove]
    team_empty ::= "empty" && target
    team_option ::= STR && team_option_arg && "=" && team_option_arg_value
    # team_option_arg, team_option_arg_value are defined in the team_options_version.json
    team_remove ::= "remove" && STR
    """
    def __init__(self):
        if config_data.version == "1.12":
            self.begin_cmd = "scoreboard teams"
        elif config_data.version == "1.13":
            self.begin_cmd = "team"

class TeamAddNode(TeamCmdNode):
    """
    team_add ::= "add" && STR && (STR)*

    Attributes:
        team_name (Token)
        display_name (Token or None)
    """
    def __init__(self, team_name, display_name=None):
        super().__init__()
        self.team_name = team_name
        self.display_name = display_name

    def build(self):
        team_name = self.team_name.build()
        if self.display_name is None:
            return f"{self.begin_cmd} add {team_name}"

        display_name = self.display_name.build()
        return f"{self.begin_cmd} add {team_name} {display_name}"

class TeamJoinNode(TeamCmdNode):
    """
    team_join ::= STR && "+=" && target

    Attributes:
        team_name (Token)
        target (SelectorNode or Token)
    """
    def __init__(self, team_name, target):
        super().__init__()
        self.team_name = team_name
        self.target = target

    def build(self):
        team_name = self.team_name.build()
        target = self.target.build()
        return f"{self.begin_cmd} join {team_name} {target}"

class TeamLeaveNode(TeamCmdNode):
    """
    team_leave ::= "leave" && target

    Attributes:
        target (SelectorNode or Token)
    """
    def __init__(self, target):
        super().__init__()
        self.target = target

    def build(self):
        target = self.target.build()
        return f"{self.begin_cmd} leave {target}"

class TeamEmptyNode(TeamCmdNode):
    """
    team_empty ::= "empty" && STR

    Attributes:
        team_name (Token)
    """
    def __init__(self, team_name, target):
        super().__init__()
        self.team_name = team_name
        self.target = target

    def build(self):
        team_name = self.team_name.build()
        target = self.target.build()
        return f"{self.begin_cmd} join {team_name} {target}"

class TeamOptionNode(TeamCmdNode):
    pass

class TeamRemoveNode(TeamCmdNode):
    pass

class BossbarCmdNode(CmdNode):
    pass

class TagCmdNode(CmdNode):
    pass
    
class DataCmdNode(CmdNode):
    pass


class SelectorNode(CmdNode):
    """
    selector ::= selector_var & ("[" & selector_args & "]")?
    # selector_var is defined under selector_version.json as "selector_variables"
    selector_args ::= (single_arg)? | (single_arg & ("," & single_arg)*)?
    single_arg ::= [simple_arg, range_arg, tag_arg]

    simple_arg ::= default_arg & "=" & ("!")? & [STR, signed_int]
    # default_arg is defined under selector_version.json as "selector_arguments"
    tag_arg ::= STR
    range_arg ::= STR & ("=" & range)?
    range ::= [nonneg_int, (nonneg_int & ".."), (".." & nonneg_int), (nonneg_int & ".." & nonneg_int)]

    Attributes:
        selector_var (Token)
        selector_args (list of SelectorArgNode objects)
    """
    def __init__(self, selector_var, selector_args):
        assert isinstance(selector_var, Token)
        assert isinstance(selector_args, list)

        self.selector_var = selector_var
        self.selector_args = selector_args

    def build(self):
        selector_var = self.selector_var.build()
        selector_args = ",".join(x.build() for x in self.selector_args)
        return f"{selector_var}[{selector_args}]"

class BlockNode(CmdNode):
    pass

class Vec2Node(CmdNode):
    pass

class Vec3Node(CmdNode):
    pass