from abc import ABC
from config_data import ConfigData
from in_file_config import InFileConfig
from lexical_token import Token

in_file_config = InFileConfig()
config_data = ConfigData()

class Node(ABC):
    pass

class CmdNode(Node, ABC):
    pass

class StmtNode(Node, ABC):
    pass

class JsonParseNode(Node, ABC):
    """
    Specifically holds an arg and an arg value
    """
    def __init__(self, arg, arg_value):
        self.arg = arg
        self.arg_value = arg_value

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
    def __init__(self, name, command_nodes):
        assert isinstance(name, Token)
        assert isinstance(command_nodes, list)
        self.name = name
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
        cmd_segment_nodes (list of specialized CmdNode objects)
    
    Attributes:
        execute_node (ExecuteCmdNode)
        scoreboard_node (ScoreboardCmdNode) 
        function_node (FunctionCmdNode)
        simple_node (SimpleCmdNode)
    """
    def __init__(self, cmd_segment_nodes):
        self.cmd_segment_nodes = cmd_segment_nodes

class ExecuteCmdNode(CmdNode):
    """
    Attributes:
        sub_cmd_nodes (list of ExecuteSub{type}Arg objects)
    """
    def __init__(self, sub_cmd_nodes):
        self.sub_cmd_nodes = sub_cmd_nodes

    def __repr__(self):
        return f"ExecuteCmdNode[sub_cmd_nodes={self.sub_cmd_nodes}]"

class ExecuteSubLegacyArg(CmdNode):
    """
    Execute node for all versions under 1.12 inclusive

    Attributes:
        selector (SelectorNode)
        coords (Vec3Node or None)
        sub_if (ExecuteSubIfBlockArg or None)
    """
    def __init__(self, selector, coords=None, sub_if=None):
        assert isinstance(selector, SelectorNode)
        assert coords is None or isinstance(coords, Vec3Node)
        assert sub_if is None or isinstance(sub_if, ExecuteSubIfBlockArg)

        self.selector = selector
        self.coords = coords
        self.sub_if = sub_if

    def __repr__(self):
        return f"SelectorNode[selector={self.selector}, coords={self.coords}, sub_if={self.sub_if}]"

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

class ExecuteSubIfSelectorArg(ExecuteSubIfArg):
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

    # def build(self):
    #     selector = self.selector.build()
    #     return f"{self.sub_cmd} entity {selector}"

class ExecuteSubIfBlockArg(ExecuteSubIfArg):
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

    # def build(self):
    #     if self.coords is None:
    #         coords = "~ ~ ~"
    #     else:
    #         coords = self.coords.build()

    #     block = self.block.build()
    #     if self.version == "1.12":
    #         return f"detect {coords} {block}"
    #     return f"{self.sub_cmd} block {coords} {block}"
    
class ExecuteSubIfBlocksArg(ExecuteSubIfArg):
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

    # def build(self):
    #     if self.masked:
    #         cmd_param = "masked"
    #     else:
    #         cmd_param = "all"
    #         
    #     coords1 = self.coords1.build()
    #     coords2 = self.coords2.build()
    #     coords3 = self.coords3.build()
    #     return f"{self.sub_cmd} blocks {coords1} {coords2} {coords3} {cmd_param}"

class ExecuteSubIfCompareEntityArg(ExecuteSubIfArg):
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
    # valid_operators = frozenset({"==", "<", "<=", ">", ">="})

    def __init__(self, selector1, objective1, operator, selector2, objective2, negated=False):
        super().__init__(negated)
        self.selector1 = selector1
        self.objective1 = objective1
        self.operator = operator
        self.selector2 = selector2
        self.objective2 = objective2

    # def build(self):
    #     return "{} score {} {} {} {} {}".format(
    #         self.sub_cmd, self.selector1.build(), self.objective1.build(prefix=True),
    #         self.operator.build(replacements={"==": "="}), self.selector2.build(), self.objective2.build(prefix=True))

class ExecuteSubIfCompareIntArg(ExecuteSubIfArg):
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
    # valid_operators = frozenset({"==", "<", "<=", ">", ">="})

    def __init__(self, selector, objective, operator, value, negated=False):
        super().__init__(negated)
        self.selector = selector
        self.objective = objective
        self.operator = operator
        self.value = value

    # def build(self):
    #     int_value = self.value.value
    #     if self.operator.value == "==":
    #         int_range = int_value
    #     elif self.operator.value == "<":
    #         int_range = "..{}".format(int_value-1)
    #     elif self.operator.value == "<=":
    #         int_range = "..{}".format(int_value)
    #     elif self.operator.value == ">":
    #         int_range = "{}..".format(int_value+1)
    #     elif self.operator.value == ">=":
    #         int_range = "{}..".format(int_value)
    #     else:
    #         raise SyntaxError("Unknown default case")

    #     return "{} score {} {} matches {}".format(self.sub_cmd, self.selector.build(), self.objective.build(prefix=True), int_range)

class ExecuteSubIfRangeArg(ExecuteSubIfArg):
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

    # def build(self):
    #     return "{} score {} {} matches {}".format(self.sub_cmd, self.selector.build(), self.objective.build(prefix=True), self.int_range.build())


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

class SimpleCmdNode(CmdNode):
    """
    Attributes:
        nodes (list of Token, SelectorNode, JsonNode and NbtNode objects)
    """
    def __init__(self, tokens):
        assert isinstance(tokens, list)
        self.tokens = tokens


class BossbarCmdNode(CmdNode):
    pass

class BossbarAddNode(BossbarCmdNode):
    """
    Attributes:
        bossbar_id (Token)
        display_name (Token)
        json (JsonNode)
    """
    def __init__(self, bossbar_id, display_name=None, json=None):
        assert isinstance(bossbar_id, Token)

        # makes sure that at least one is none since the only possible
        # options are for both to be none, or one to be not none
        assert display_name is None or json is None
        if display_name is not None:
            assert isinstance(display_name, Token)
        if json is not None:
            assert isinstance(json, JsonNode)

        self.bossbar_id = bossbar_id
        self.display_name = display_name
        self.json = json

class BossbarRemoveNode(BossbarCmdNode):
    """
    Attributes:
        bossbar_id (Token)
    """
    def __init__(self, bossbar_id):
        assert isinstance(bossbar_id, Token)
        self.bossbar_id = bossbar_id

class BossbarGetNode(BossbarCmdNode):
    """
    Attributes:
        bossbar_id (Token)
        sub_cmd (Token)
    """
    def __init__(self, bossbar_id, sub_cmd):
        assert isinstance(bossbar_id, Token)
        assert isinstance(sub_cmd, Token)
        self.bossbar_id = bossbar_id
        self.sub_cmd = sub_cmd

class BossbarSetNode(BossbarCmdNode):
    """
    Attributes:
        bossbar_id (Token)
        arg (Token)
        value (Token)
    """
    def __init__(self, bossbar_id, arg, arg_value):
        assert isinstance(bossbar_id, Token)
        assert isinstance(arg, Token)
        assert isinstance(arg_value, Token)
        self.bossbar_id = bossbar_id
        self.arg = arg
        self.arg_value = arg_value


class DataCmdNode(CmdNode):
    pass

class DataGetNode(DataCmdNode):
    """
    Attributes:
        entity_vec3 (SelectorNode, Vec3Node)
        path (Vec3Node)
    """
    def __init__(self, entity_vec3, path, scale=None):
        self.entity_vec3 = entity_vec3
        self.path = path
        self.scale = scale

class DataMergeNode(DataCmdNode):
    """
    Attributes:
        nbt (NbtNode)
    """
    def __init__(self, nbt):
        self.nbt = nbt

class DataRemoveNode(DataCmdNode):
    """
    Attributes:
        path (Vec3Node)
    """
    def __init__(self, path):
        self.path = path


class EffectCmdNode(CmdNode):
    pass

class EffectClearNode(EffectCmdNode):
    def __init__(self, effect=None):
        self.effect = effect

class EffectGiveNode(EffectCmdNode):
    def __init__(self, effect, duration=None, level=None, show_particles=False):
        self.effect = effect
        self.duration = duration
        self.level = level
        self.show_particles = show_particles


class FunctionCmdNode(CmdNode):
    """
    Attributes:
        function_name (str): The mcfunction shortcut for the mcfunction name
    """
    def __init__(self, function_name):
        assert isinstance(function_name, str)
        self.function_name = function_name

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

class TeamLeaveNode(TeamCmdNode):
    """
    team_leave ::= "leave" && target

    Attributes:
        target (SelectorNode or Token)
    """
    def __init__(self, target):
        super().__init__()
        self.target = target

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

class TeamOptionNode(TeamCmdNode):
    """
    Attributes:
        team_name (Token)
        option (Token)
        value (Token)
    """
    def __init__(self, team_name, option, value):
        super().__init__()
        self.team_name = team_name
        self.option = option
        self.value = value

class TeamRemoveNode(TeamCmdNode):
    """
    Attributes:
        team_name (Token)
    """
    def __init__(self, team_name):
        super().__init__()
        self.team_name = team_name


class TagCmdNode(CmdNode):
    pass

class TagAddNode(TagCmdNode):
    """
    Attributes:
        tag (Token)
    """
    def __init__(self, tag):
        self.tag = tag

class TagRemoveNode(TagCmdNode):
    """
    Attributes:
        tag (Token)
    """
    def __init__(self, tag):
        self.tag = tag
    

class SelectorNode(CmdNode):
    """
    Attributes:
        selector_var (SelectorVarNode)
        selector_args (list of SelectorArgNode objects or None)
    """
    def __init__(self, selector_var, selector_args=None):
        assert isinstance(selector_var, SelectorVarNode)
        assert selector_args is None or isinstance(selector_args, list)

        self.selector_var = selector_var
        self.selector_args = selector_args

    def __repr__(self):
        return f"SelectorNode[selector_var={self.selector_var}, selector_args={self.selector_args}]"

class SelectorVarNode(CmdNode):
    """
    Attributes:
        selector_var_specifier (Token)
    """
    def __init__(self, selector_var_specifier):
        self.selector_var_specifier = selector_var_specifier

    def __repr__(self):
        return f"SelectorVarNode[selector_var_specifier={self.selector_var_specifier}]"

class SelectorScoreArgNode(CmdNode):
    """
    Attributes:
        objective (Token)
        int_range (IntRangeNode)
    """
    def __init__(self, objective, int_range):
        assert isinstance(objective, Token), repr(objective)
        assert isinstance(int_range, IntRangeNode)
        self.objective = objective
        self.int_range = int_range

    def __repr__(self):
        return f"SelectorScoreArgNode[objective={self.objective}, int_range={self.int_range}]"

class SelectorDefaultArgNode(CmdNode):
    """
    Attributes:
        arg (Token)
        arg_value (SelectorDefaultArgValueNode, SelectorDefaultGroupArgValueNode)
    """
    def __init__(self, arg, arg_value):
        assert isinstance(arg, Token), repr(arg)
        assert isinstance(arg_value, (SelectorDefaultArgValueNode, SelectorDefaultGroupArgValueNode)), repr(arg_value)
        self.arg = arg
        self.arg_value = arg_value

    def __repr__(self):
        return f"SelectorDefaultArgNode[arg={self.arg}, arg_value={self.arg_value}]"

class SelectorDefaultArgValueNode(CmdNode):
    """
    Attributes:
        arg_value (Token, NumberRangeNode, IntRangeNode)
        negated (bool)
    """
    def __init__(self, arg_value, negated=False):
        self.arg_value = arg_value
        self.negated = negated

    def __repr__(self):
        return f"SelectorDefaultArgValueNode[arg_value={self.arg_value}, negated={self.negated}]"

class SelectorDefaultGroupArgValueNode(CmdNode):
    """
    Attributes:
        arg_values (list of Token objects)
        negated (bool)
    """
    def __init__(self, arg_values, negated=False):
        assert isinstance(arg_values, list)
        assert isinstance(negated, bool)
        self.arg_values = arg_values
        self.negated = negated

class SelectorTagArgNode(CmdNode):
    """
    Attributes:
        tag (Token)
    """
    def __init__(self, tag):
        assert isinstance(tag, Token)
        self.tag = tag

    def __repr__(self):
        return f"SelectorTagArgNode[tag={self.tag}]"

class SelectorNbtArgNode(CmdNode):
    """
    Attributes:
        nbt (NbtNode)
    """
    def __init__(self, nbt):
        # assert isinstance(nbt, NbtNode)
        self.nbt = nbt

class SelectorAdvancementArgNode(CmdNode):
    """
    Attributes:
        advancements (?)
    """
    def __init__(self, advancements):
        self.advancements = advancements 



class NbtNode(CmdNode):
    pass

class JsonNode(CmdNode):
    pass

class IntRangeNode(CmdNode):
    """
    Note that a range can be a singular number. If so, left_int is the same as right_int

    Attributes:
        min_int (Token)
        max_int (Token)
    """
    def __init__(self, min_int, max_int):
        assert min_int is None or isinstance(min_int, Token)
        assert max_int is None or isinstance(max_int, Token)
        self.min_int = min_int
        self.max_int = max_int

    def __repr__(self):
        return f"IntRangeNode[min={self.min_int}, max={self.max_int}]"

class NumberRangeNode(CmdNode):
    """
    Note that a range can be a singular number. If so, min_number is the same as max_number

    Attributes:
        min_number (Token or None)
        max_number (Token or None)
    """
    def __init__(self, min_number, max_number):
        assert min_number is None or isinstance(min_number, Token)
        assert max_number is None or isinstance(max_number, Token)
        self.min_number = min_number
        self.max_number = max_number

class BlockNode(CmdNode):
    """
    Attributes:
        block (Token)
        states (list of BlockStateNode objects)
        nbt (NbtNode or None)
    """
    def __init__(self, block, states, nbt=None):
        assert isinstance(block, Token)
        assert isinstance(states, list)
        # assert nbt is None or isinstance(nbt, NbtNode)
        self.block = block
        self.states = states
        self.nbt = nbt


class CoordsNode(CmdNode):
    """
    Factory for getting a vec2 or vec3 node
    This is literally here because linting is stupid
    """
    def __new__(self, coords):
        if len(coords) == 3:
            return Vec3Node(*coords)
        elif len(coords) == 2:
            return Vec2Node(*coords)
        else:
            raise SyntaxError("Invalid number of coordinates to make a Vec3Node or Vec2Node")

class Vec2Node(CmdNode):
    """
    Attributes:
        coord1 (Token)
        coord2 (Token)
    """
    def __init__(self, coord1, coord2):
        self.coord1 = coord1
        self.coord2 = coord2

class Vec3Node(CmdNode):
    """
    Attributes:
        coord1 (Token)
        coord2 (Token)
        coord3 (Token)
    """
    def __init__(self, coord1, coord2, coord3):
        self.coord1 = coord1
        self.coord2 = coord2
        self.coord3 = coord3

    def __repr__(self):
        return f"Vec3Node[coord1={self.coord1}, coord2={self.coord2}, coord3={self.coord3}]"
    
