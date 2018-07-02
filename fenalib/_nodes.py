from abc import ABC

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fenalib.config_data import ConfigData
from fenalib.repr_utils import addrepr
from fenalib.assert_utils import assert_type, assert_list_types, assert_tuple_types
from fenalib.lexical_token import Token

config_data = ConfigData()

"""
Backup module when changing to using NamedTuple
"""

@addrepr
class Node(ABC):
    """
    All nodes specified below will inherit from this parent class

    Adds a simple __repr__ method to all of its classes to display its own variables
    """
    pass

class ProgramNode(Node):
    """
    Holds all statements found inside the global scope of the program

    Attributes:
        statement_nodes (list of nodes inherited from StmtNode)
    """
    def __init__(self, statement_nodes):
        assert_type(statement_nodes, list)
        assert_list_types(statement_nodes, StmtNode)
        self.statement_nodes = statement_nodes


class StmtNode(Node, ABC):
    """
    General node to be inherited from all specialized statement nodes
    """
    pass

class McFunctionNode(StmtNode):
    """
    Holds a single mcfunction with its full path and all fena command nodes

    Attributes:
        name (Token): The mcfunction name
        command_nodes (list of FenaCmdNode objects)
    """
    def __init__(self, name, command_nodes):
        assert_type(name, Token)
        assert_list_types(command_nodes, CmdNode)
        self.name = name
        self.command_nodes = command_nodes

class FolderNode(StmtNode):
    """
    Holds all statements found inside a folder node

    Attributes:
        folder (Token)
        statement_nodes (list of nodes inherited from StmtNode)
    """
    def __init__(self, folder, statement_nodes):
        assert_type(folder, Token)
        assert_list_types(statement_nodes, StmtNode)
        self.folder = folder
        self.statement_nodes = statement_nodes

class VarSetNode(StmtNode):
    """
    Holds all variables defined for the file

    Attributes:
        variable (Token)
        value (Token)
    """
    def __init__(self, variable, value):
        assert_type(variable, Token)
        assert_type(value, Token)
        self.variable = variable
        self.value = value


class CmdNode(Node, ABC):
    """
    General node to be inherited from all nodes relating to commands
    """
    pass

class FenaCmdNode(CmdNode):
    """
    Holds all command segments for a command node

    Args:
        cmd_segment_nodes (list of MainCmdNode objects)
            - should contain one of {ExecuteCmdNode, ScoreboardCmdNode, FunctionCmdNode, SimpleCmdNode}
    """
    def __init__(self, cmd_segment_nodes):
        assert_list_types(cmd_segment_nodes, MainCmdNode)
        self.cmd_segment_nodes = cmd_segment_nodes

class MainCmdNode(CmdNode, ABC):
    """
    General node to be inherited from all children nodes to the FenaCmdNode
        - Nodes that a command is made up of in the most general context
        - eg. ExecuteCmdNode, SimpleCmdNode
    """
    pass

class ExecuteCmdNode(MainCmdNode):
    """
    Attributes:
        sub_cmd_nodes (list of ExecuteSubArgNode, SelectorNode and Vec3Node objects or list of ExecuteSubLegacyArg in 1.12)
    """
    def __init__(self, sub_cmd_nodes):
        if config_data.version == "1.12":
            assert_list_types(sub_cmd_nodes, ExecuteSubLegacyArg)
        else:
            assert_list_types(sub_cmd_nodes, ExecuteSubArgNode, SelectorNode, Vec3Node)
        self.sub_cmd_nodes = sub_cmd_nodes

class ExecuteSubLegacyArg(MainCmdNode):
    """
    Execute node for all versions under 1.12 inclusive

    Attributes:
        selector (SelectorNode)
        coords (Vec3Node or None)
        sub_if (list of ExecuteSubIfBlockArg objects)
    """
    def __init__(self, selector, coords=None, sub_if=None):
        assert_type(selector, SelectorNode)
        assert_type(coords, Vec3Node, optional=True)
        assert_list_types(sub_if, ExecuteSubIfBlockArg)
        self.selector = selector
        self.coords = coords
        self.sub_if = sub_if

class ExecuteSubArgNode(CmdNode, ABC):
    pass

class ExecuteSubArgSelectorNode(ExecuteSubArgNode, ABC):
    """
    Attributes:
        selector (SelectorNode)
    """
    def __init__(self, selector):
        assert_type(selector, SelectorNode)
        self.selector = selector

class ExecuteSubArgVec2Node(ExecuteSubArgNode, ABC):
    """
    Attributes:
        vec2 (Vec2Node)
    """
    def __init__(self, vec2):
        assert_type(vec2, Vec2Node)
        self.vec2 = vec2

class ExecuteSubArgVec3Node(ExecuteSubArgNode, ABC):
    """
    Attributes:
        vec3 (Vec3Node)
    """
    def __init__(self, vec3):
        assert_type(vec3, Vec3Node)
        self.vec3 = vec3

class ExecuteSubAsArg(ExecuteSubArgSelectorNode):
    pass

class ExecuteSubPosVec3Arg(ExecuteSubArgVec3Node):
    pass

class ExecuteSubPosSelectorArg(ExecuteSubArgSelectorNode):
    pass

class ExecuteSubAtAnchorArg(ExecuteSubArgNode):
    """
    Attributes:
        anchor (Token)
    """
    def __init__(self, anchor):
        assert_type(anchor, Token)
        self.anchor = anchor

class ExecuteSubAtSelectorArg(ExecuteSubArgSelectorNode):
    pass

class ExecuteSubAtCoordsArg(ExecuteSubArgNode):
    """
    Attributes:
        vec3 (Vec3Node)
        vec2 (Vec2Node)
    """
    def __init__(self, vec3, vec2):
        assert_type(vec3, Vec3Node)
        assert_type(vec2, Vec2Node)
        self.vec3 = vec3
        self.vec2 = vec2

class ExecuteSubAtAxesArg(ExecuteSubArgNode):
    """
    Attributes:
        axes (Token)
    """
    def __init__(self, axes):
        assert_type(axes, Token)
        self.axes = axes

class ExecuteSubFacingVec3Arg(ExecuteSubArgVec3Node):
    """
    Attributes:
        vec3 (Vec3Node)
    """
    pass

class ExecuteSubFacingSelectorArg(ExecuteSubArgNode):
    """
    Attributes:
        selector (SelectorNode)
        anchor (Token or None)
    """
    def __init__(self, selector, anchor=None):
        assert_type(selector, SelectorNode)
        assert_type(anchor, Token, optional=True)
        self.selector = selector
        self.anchor = anchor

class ExecuteSubRotSelectorArg(ExecuteSubArgSelectorNode):
    pass

class ExecuteSubRotVec2Arg(ExecuteSubArgVec2Node):
    """
    Attributes:
        vec2 (Vec2Node)
    """
    pass

class ExecuteSubAnchorArg(ExecuteSubArgNode):
    """
    Attributes:
        axes (Token)
    """
    def __init__(self, axes):
        assert_type(axes, Token)
        self.axes = axes

class ExecuteSubInArg(ExecuteSubArgNode):
    """
    Attributes:
        dimension (Token)
    """
    def __init__(self, dimension):
        assert_type(dimension, Token)
        self.dimension = dimension

class ExecuteSubAstArg(ExecuteSubArgSelectorNode):
    pass

class ExecuteSubIfArg(ExecuteSubArgNode):
    """
    Args:
        negated (bool): Whether the statement argument should be negated or not when built

    Attributes:
        sub_cmd (str): Either "if" if negated is false, or "unless" if negated is true
    """
    def __init__(self, negated):
        assert_type(negated, bool)
        self.sub_cmd = ("unless" if negated else "if")

class ExecuteSubIfSelectorArg(ExecuteSubIfArg):
    """
    Attributes:
        selector (SelectorNode)
    """
    def __init__(self, selector, negated=False):
        assert_type(selector, SelectorNode)
        super().__init__(negated)
        self.selector = selector

class ExecuteSubIfBlockArg(ExecuteSubIfArg):
    """
    Attributes:
        block (BlockNode)
        coords (Vec3Node or None)
    """
    def __init__(self, block, coords=None, negated=False):
        assert_type(block, BlockNode)
        assert_type(coords, Vec3Node, optional=True)

        super().__init__(negated)
        self.block = block
        self.coords = coords

class ExecuteSubIfBlocksArg(ExecuteSubIfArg):
    """
    Attributes:
        coords1 (Vec3Node)
        coords2 (Vec3Node)
        coords3 (Vec3Node)
        option (Token or None)
    """
    def __init__(self, coords1, coords2, coords3, option=None, negated=False):
        assert_type(coords1, Vec3Node)
        assert_type(coords2, Vec3Node)
        assert_type(coords3, Vec3Node)
        assert_type(option, Token, optional=True)

        super().__init__(negated)
        self.coords1 = coords1
        self.coords2 = coords2
        self.coords3 = coords3
        self.option = option

class ExecuteSubIfCompareEntityArg(ExecuteSubIfArg):
    """
    Attributes:
        target (SelectorNode or Token)
        objective (Token)
        operator (Token)
        target_get (SelectorNode)
        objective_get (Token)
    """
    def __init__(self, target, objective, operator, target_get, objective_get, negated=False):
        assert_type(target, SelectorNode, Token)
        assert_type(objective, Token)
        assert_type(operator, Token)
        assert_type(target_get, SelectorNode)
        assert_type(objective_get, Token)

        super().__init__(negated)
        self.target = target
        self.objective = objective
        self.operator = operator
        self.target_get = target_get
        self.objective_get = objective_get

class ExecuteSubIfCompareIntArg(ExecuteSubIfArg):
    """
    Attributes:
        target (SelectorNode or Token)
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
    def __init__(self, target, objective, operator, value, negated=False):
        assert_type(target, SelectorNode, Token)
        assert_type(objective, Token)
        assert_type(operator, Token)
        assert_type(value, Token)

        super().__init__(negated)
        self.target = target
        self.objective = objective
        self.operator = operator
        self.value = value

class ExecuteSubIfRangeArg(ExecuteSubIfArg):
    """
    Attributes:
        target (SelectorNode or Token)
        objective (Token)
        int_range (Token)

    Usage:
        if(target objective in int..int) -> if score target objective matches int..int
    """
    def __init__(self, target, objective, int_range, negated=False):
        assert_type(target, SelectorNode, Token)
        assert_type(objective, Token)
        assert_type(int_range, Token)

        super().__init__(negated)
        self.target = target
        self.objective = objective
        self.int_range = int_range

class ExecuteSubStoreArg(ExecuteSubArgNode):
    def __init__(self, store_type):
        assert_type(store_type, str)
        self.store_type = store_type

class ExecuteSubStoreSelectorDataArg(ExecuteSubStoreArg):
    """
    Attributes:
        selector (SelectorNode)
        data_path (DataPathNode)
        scale (Token)
        data_type (Token)
    """
    def __init__(self, store_type, selector, data_path, scale, data_type=None):
        super().__init__(store_type)
        assert_type(selector, SelectorNode)
        assert_type(data_path, DataPathNode)
        assert_type(scale, Token)
        assert_type(data_type, Token, optional=True)

        self.selector = selector
        self.data_path = data_path
        self.scale = scale
        self.data_type = data_type

class ExecuteSubStoreVec3DataArg(ExecuteSubStoreArg):
    """
    Attributes:
        vec3 (Vec3Node)
        data_path (DataPathNode)
        scale (Token)
        data_type (Token)
    """
    def __init__(self, store_type, vec3, data_path, scale, data_type=None):
        super().__init__(store_type)
        assert_type(vec3, SelectorNode, Vec3Node)
        assert_type(data_path, DataPathNode)
        assert_type(scale, Token)
        assert_type(data_type, Token, optional=True)

        self.vec3 = vec3
        self.data_path = data_path
        self.scale = scale
        self.data_type = data_type

class ExecuteSubStoreScoreArg(ExecuteSubStoreArg):
    """
    Attributes:
        target (SelectorNode or Token)
        objective (Token)
    """
    def __init__(self, store_type, target, objective):
        super().__init__(store_type)
        assert_type(target, SelectorNode, Token)
        assert_type(objective, Token)
        self.target = target
        self.objective = objective

class ExecuteSubStoreBossbarArg(ExecuteSubStoreArg):
    """
    Attributes:
        bossbar_id (NamespaceIdNode)
        sub_cmd (Token)
    """
    def __init__(self, store_type, bossbar_id, sub_cmd):
        super().__init__(store_type)
        assert_type(bossbar_id, NamespaceIdNode)
        assert_type(sub_cmd, Token)
        self.bossbar_id = bossbar_id
        self.sub_cmd = sub_cmd

class ExecuteSubDataArg(ExecuteSubStoreArg):
    pass

class ExecuteSubScoreArg(ExecuteSubStoreArg):
    pass

class ExecuteSubBossbarArg(ExecuteSubStoreArg):
    pass


class ScoreboardCmdMathNode(MainCmdNode):
    """
    Args:
        target (SelectorNode or Token)
        objective (Token)
        operator (Token)
        target_get (SelectorNode or Token)
        objective_get (Token or None)
    """

    def __init__(self, target, objective, operator, target_get, objective_get=None):
        assert_type(target, SelectorNode, Token)
        assert_type(objective, Token)
        assert_type(operator, Token)
        assert_type(target_get, SelectorNode, Token)
        assert_type(objective_get, Token, optional=True)

        self.target = target
        self.objective = objective
        self.operator = operator
        self.target_get = target_get
        self.objective_get = objective_get

class ScoreboardCmdMathValueNode(MainCmdNode):
    """
    Args:
        target (SelectorNode or Token)
        objective (Token)
        operator (Token)
        value (Token)
        nbt (NbtObjectNode or None)
    """
    def __init__(self, target, objective, operator, value, nbt=None):
        assert_type(target, SelectorNode, Token)
        assert_type(objective, Token)
        assert_type(operator, Token)
        assert_type(value, Token)
        assert_type(nbt, NbtObjectNode, optional=True)

        self.target = target
        self.objective = objective
        self.operator = operator
        self.value = value
        self.nbt = nbt

class ScoreboardCmdSpecialNode(MainCmdNode):
    """
    Args:
        target (SelectorNode or Token)
        sub_cmd (Token)
        objective (Token)
    """
    def __init__(self, target, sub_cmd, objective):
        assert_type(target, SelectorNode, Token)
        assert_type(sub_cmd, Token)
        assert_type(objective, Token)

        self.target = target
        self.sub_cmd = sub_cmd
        self.objective = objective

class SimpleCmdNode(MainCmdNode):
    """
    Attributes:
        nodes (list of Token, SelectorNode, JsonObjectNode and NbtObjectNode objects)
    """
    def __init__(self, tokens):
        assert_type(tokens, list)
        assert_list_types(tokens, Token, SelectorNode, JsonObjectNode, NbtObjectNode, NamespaceIdNode)
        self.tokens = tokens

class BossbarCmdNode(MainCmdNode, ABC):
    pass

class BossbarAddNode(BossbarCmdNode):
    """
    Attributes:
        bossbar_id (NamespaceIdNode)
        json (JsonObjectNode)
    """
    def __init__(self, bossbar_id, json):
        assert_type(bossbar_id, NamespaceIdNode)
        assert_type(json, JsonObjectNode)
        self.bossbar_id = bossbar_id
        self.json = json

class BossbarRemoveNode(BossbarCmdNode):
    """
    Attributes:
        bossbar_id (NamespaceIdNode)
    """
    def __init__(self, bossbar_id):
        assert_type(bossbar_id, NamespaceIdNode)
        self.bossbar_id = bossbar_id

class BossbarGetNode(BossbarCmdNode):
    """
    Attributes:
        bossbar_id (NamespaceIdNode)
        sub_cmd (Token)
    """
    def __init__(self, bossbar_id, sub_cmd):
        assert_type(bossbar_id, NamespaceIdNode)
        assert_type(sub_cmd, Token)
        self.bossbar_id = bossbar_id
        self.sub_cmd = sub_cmd

class BossbarSetNode(BossbarCmdNode):
    """
    Attributes:
        bossbar_id (NamespaceIdNode)
        arg (Token)
        arg_value (Token, JsonObjectNode, SelectorNode)
    """
    def __init__(self, bossbar_id, arg, arg_value):
        assert_type(bossbar_id, NamespaceIdNode)
        assert_type(arg, Token)
        assert_type(arg_value, Token, JsonObjectNode, SelectorNode)
        self.bossbar_id = bossbar_id
        self.arg = arg
        self.arg_value = arg_value

class DataCmdNode(MainCmdNode):
    pass

class DataGetNode(DataCmdNode):
    """
    Attributes:
        entity_vec3 (SelectorNode, Vec3Node)
        data_path (DataPathNode or None)
        scale (Token or None)
    """
    def __init__(self, entity_vec3, data_path=None, scale=None):
        assert_type(entity_vec3, SelectorNode, Vec3Node)
        assert_type(data_path, DataPathNode, optional=True)
        assert_type(scale, Token, optional=True)
        self.entity_vec3 = entity_vec3
        self.data_path = data_path
        self.scale = scale

class DataMergeNode(DataCmdNode):
    """
    Attributes:
        entity_vec3 (SelectorNode, Vec3Node)
        nbt (NbtObjectNode)
    """
    def __init__(self, entity_vec3, nbt):
        assert_type(entity_vec3, SelectorNode, Vec3Node)
        assert_type(nbt, NbtObjectNode)
        self.entity_vec3 = entity_vec3
        self.nbt = nbt

class DataRemoveNode(DataCmdNode):
    """
    Attributes:
        entity_vec3 (SelectorNode, Vec3Node)
        data_path (DataPathNode)
    """
    def __init__(self, entity_vec3, data_path):
        assert_type(entity_vec3, SelectorNode, Vec3Node)
        assert_type(data_path, DataPathNode)
        self.entity_vec3 = entity_vec3
        self.data_path = data_path


class EffectCmdNode(MainCmdNode):
    pass

class EffectClearNode(EffectCmdNode):
    """
    Attributes:
        selector (SelectorNode)
        effect_id (Token or None)
    """
    def __init__(self, selector, effect_id=None):
        assert_type(selector, SelectorNode)
        assert_type(effect_id, Token, optional=True)
        self.selector = selector
        self.effect_id = effect_id

class EffectGiveNode(EffectCmdNode):
    """
    Attributes:
        selector (SelectorNode)
        effect_id (Token)
        duration (Token or None)
        level (Token or None)
        hide_particles (bool)
    """
    def __init__(self, selector, effect_id, duration=None, level=None, hide_particles=True):
        assert_type(selector, SelectorNode)
        assert_type(effect_id, Token)
        assert_type(duration, Token, optional=True)
        assert_type(level, Token, optional=True)
        assert_type(hide_particles, bool)
        self.selector = selector
        self.effect_id = effect_id
        self.duration = duration
        self.level = level
        self.hide_particles = hide_particles


class FunctionCmdNode(MainCmdNode):
    """
    Attributes:
        function_id (NamespaceIdNode)
        sub_arg (Token or None)
        selector (SelectorNode or None)
    """
    def __init__(self, function_id, sub_arg=None, selector=None):
        assert_type(function_id, NamespaceIdNode)
        assert_type(sub_arg, Token, optional=True)
        assert_type(selector, SelectorNode, optional=True)
        self.function_id = function_id
        self.sub_arg = sub_arg
        self.selector = selector

class ItemCmdNode(MainCmdNode):
    pass

class ItemGiveNode(ItemCmdNode):
    """
    Attributes:
        selector (SelectorNode)
        item (ItemNode)
        count (Token or None)
    """
    def __init__(self, selector, item, count=None):
        assert_type(selector, SelectorNode)
        assert_type(item, ItemNode)
        assert_type(count, Token, optional=True)
        self.selector = selector
        self.item = item
        self.count = count

class ItemClearNode(ItemCmdNode):
    """
    Attributes:
        selector (SelectorNode)
        item (ItemNode or Token)
        count (Token or None)
    """
    def __init__(self, selector, item, count=None):
        assert_type(selector, SelectorNode)
        assert_type(item, ItemNode, Token)
        assert_type(count, Token, optional=True)
        self.selector = selector
        self.item = item
        self.count = count

class ItemReplaceEntityNode(ItemCmdNode):
    """
    Attributes:
        selector (SelectorNode)
        slot (Token)
        item (ItemNode)
        count (Token or None)
    """
    def __init__(self, selector, slot, item, count=None):
        assert_type(selector, SelectorNode)
        assert_type(slot, Token)
        assert_type(item, ItemNode)
        assert_type(count, Token, optional=True)
        self.selector = selector
        self.slot = slot
        self.item = item
        self.count = count

class ItemReplaceBlockNode(ItemCmdNode):
    """
    Attributes:
        vec3 (Vec3Node)
        slot (Token)
        item (ItemNode)
        count (Token or None)
    """
    def __init__(self, vec3, slot, item, count=None):
        assert_type(vec3, Vec3Node)
        assert_type(slot, Token)
        assert_type(item, ItemNode)
        assert_type(count, Token, optional=True)
        self.vec3 = vec3
        self.slot = slot
        self.item = item
        self.count = count

class ItemNode(CmdNode):
    """
    Attributes:
        item_id (Token)
        damage (Token or None)
        nbt (NbtObjectNode or None)
    """
    def __init__(self, item_id, damage=None, nbt=None):
        assert_type(item_id, Token)
        assert_type(damage, Token, optional=True)
        assert_type(nbt, NbtObjectNode, optional=True)
        self.item_id = item_id
        self.damage = damage
        self.nbt = nbt


class ObjectiveCmdNode(MainCmdNode):
    pass

class ObjectiveAddNode(ObjectiveCmdNode):
    """
    Attributes:
        objective (Token)
        criteria (Token)
        display_name (List[Token])
    """
    def __init__(self, objective, criteria, display_name):
        assert_type(objective, Token)
        assert_type(criteria, Token)
        assert_list_types(display_name, Token)
        self.objective = objective
        self.criteria = criteria
        self.display_name = display_name

class ObjectiveRemoveNode(ObjectiveCmdNode):
    """
    Attributes:
        objective (Token)
    """
    def __init__(self, objective):
        assert_type(objective, Token)
        self.objective = objective

class ObjectiveSetdisplayNode(ObjectiveCmdNode):
    """
    Attributes:
        slot (Token)
        objective (Token or None)
    """
    def __init__(self, slot, objective=None):
        assert_type(slot, Token)
        assert_type(objective, Token, optional=True)
        self.slot = slot
        self.objective = objective


class TagCmdNode(MainCmdNode):
    pass

class TagAddNode(TagCmdNode):
    """
    Attributes:
        selector (SelectorNode)
        tag (Token)
        nbt (NbtObjectNode or None)
    """
    def __init__(self, selector, tag, nbt=None):
        assert_type(selector, SelectorNode)
        assert_type(tag, Token)
        assert_type(nbt, NbtObjectNode, optional=True)
        self.selector = selector
        self.tag = tag
        self.nbt = nbt

class TagRemoveNode(TagCmdNode):
    """
    Attributes:
        selector (SelectorNode)
        tag (Token)
        nbt (NbtObjectNode or None)
    """
    def __init__(self, selector, tag, nbt=None):
        assert_type(selector, SelectorNode)
        assert_type(tag, Token)
        assert_type(nbt, NbtObjectNode, optional=True)
        self.selector = selector
        self.tag = tag
        self.nbt = nbt


class TeamCmdNode(MainCmdNode, ABC):
    pass

class TeamAddNode(TeamCmdNode):
    """
    team_add ::= "add" && STR && (STR)*

    Attributes:
        team_name (Token)
        display_name (list of Token objects)
    """
    def __init__(self, team_name, display_name):
        assert_type(team_name, Token)
        assert_list_types(display_name, Token)
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
        assert_type(team_name, Token)
        assert_type(target, Token, SelectorNode)
        self.team_name = team_name
        self.target = target

class TeamLeaveNode(TeamCmdNode):
    """
    team_leave ::= "leave" && target

    Attributes:
        target (SelectorNode or Token)
    """
    def __init__(self, target):
        assert_type(target, SelectorNode, Token)
        self.target = target

class TeamEmptyNode(TeamCmdNode):
    """
    team_empty ::= "empty" && STR

    Attributes:
        team_name (Token)
    """
    def __init__(self, team_name):
        assert_type(team_name, Token)
        self.team_name = team_name

class TeamOptionNode(TeamCmdNode):
    """
    Attributes:
        team_name (Token)
        option (Token)
        value (Token, JsonObjectNode)
    """
    def __init__(self, team_name, option, value):
        assert_type(team_name, Token)
        assert_type(option, Token)
        assert_type(value, Token, JsonObjectNode)
        self.team_name = team_name
        self.option = option
        self.value = value

class TeamRemoveNode(TeamCmdNode):
    """
    Attributes:
        team_name (Token)
    """
    def __init__(self, team_name):
        assert_type(team_name, Token)
        self.team_name = team_name

class XpCmdNode(MainCmdNode, ABC):
    pass

class XpMathNode(XpCmdNode):
    """
    Attributes:
        selector (SelectorNode)
        operator (Token)
        value (Token)
        sub_cmd (Token or None)
    """
    def __init__(self, selector, operator, value, sub_cmd=None):
        assert_type(selector, SelectorNode)
        assert_type(operator, Token)
        assert_type(value, Token)
        assert_type(sub_cmd, Token, optional=True)
        self.selector = selector
        self.operator = operator
        self.value = value
        self.sub_cmd = sub_cmd

class XpGetNode(XpCmdNode):
    """
    Attributes:
        selector (SelectorNode)
        sub_cmd (Token)
    """
    def __init__(self, selector, sub_cmd):
        assert_type(selector, SelectorNode)
        assert_type(sub_cmd, Token)
        self.selector = selector
        self.sub_cmd = sub_cmd

class SelectorNode(CmdNode):
    """
    Attributes:
        selector_var (SelectorVarNode)
        selector_args (SelectorArgsNode or None)
    """
    def __init__(self, selector_var, selector_args=None):
        assert_type(selector_var, SelectorVarNode)
        assert_type(selector_args, SelectorArgsNode, optional=True)

        self.selector_var = selector_var
        self.selector_args = selector_args

class SelectorVarNode(CmdNode):
    """
    Attributes:
        selector_var_specifier (Token)
    """
    def __init__(self, selector_var_specifier):
        assert_type(selector_var_specifier, Token)
        self.selector_var_specifier = selector_var_specifier

class SelectorArgsNode(CmdNode):
    """
    Attributes:
        default_args (list of SelectorDefaultArgNode objects)
        score_args (SelectorScoreArgsNode)
        tag_args (SelectorTagArgsNode)
        nbt_args (SelectorNbtArgsNode)
        advancement_args (SelectorAdvancementGroupArgNode)
    """
    def __init__(self, default_args, score_args, tag_args, nbt_args, advancement_args):
        assert_list_types(default_args, SelectorDefaultArgNode, duplicate_key=lambda x: x.arg.value)
        assert_type(score_args, SelectorScoreArgsNode)
        assert_type(tag_args, SelectorTagArgsNode)
        assert_type(nbt_args, SelectorNbtArgsNode)
        assert_type(advancement_args, SelectorAdvancementGroupArgNode)

        self.default_args = default_args
        self.score_args = score_args
        self.tag_args = tag_args
        self.nbt_args = nbt_args
        self.advancement_args = advancement_args

class SelectorScoreArgsNode(CmdNode):
    """
    Attributes:
        score_args (list of SelectorScoreArgNode objects)
    """
    def __init__(self, score_args):
        assert_list_types(score_args, SelectorScoreArgNode, duplicate_key=lambda x: x.objective.value)
        self.score_args = score_args

class SelectorScoreArgNode(CmdNode):
    """
    Attributes:
        objective (Token)
        value (IntRangeNode, Token)
    """
    def __init__(self, objective, value):
        assert_type(objective, Token)
        assert_type(value, IntRangeNode, Token)
        self.objective = objective
        self.value = value

class SelectorDefaultArgNode(CmdNode):
    """
    Attributes:
        arg (Token)
        arg_value (SelectorDefaultArgValueNode, SelectorDefaultGroupArgValueNode)
    """
    def __init__(self, arg, arg_value):
        assert_type(arg, Token)
        assert_type(arg_value, (SelectorDefaultArgValueNode, SelectorDefaultGroupArgValueNode))
        self.arg = arg
        self.arg_value = arg_value

class SelectorDefaultArgValueNode(CmdNode):
    """
    Attributes:
        arg_value (Token, NumberRangeNode, IntRangeNode)
        negated (bool)
    """
    def __init__(self, arg_value, negated=False):
        self.arg_value = arg_value
        self.negated = negated

class SelectorDefaultGroupArgValueNode(CmdNode):
    """
    Attributes:
        arg_values (list of SelectorDefaultArgValueNode objects)
    """
    def __init__(self, arg_values):
        assert_list_types(arg_values, SelectorDefaultArgValueNode)
        self.arg_values = arg_values

class SelectorTagArgsNode(CmdNode):
    """
    Attributes:
        tag_args (list of SelectorTagArgNode objects)
    """
    def __init__(self, tag_args):
        assert_list_types(tag_args, SelectorTagArgNode, duplicate_key=lambda x: x.tag.value)
        self.tag_args = tag_args

class SelectorTagArgNode(CmdNode):
    """
    Attributes:
        tag (Token)
        negated (bool)
    """
    def __init__(self, tag, negated=False):
        assert_type(tag, Token)
        assert_type(negated, bool)
        self.tag = tag
        self.negated = negated

class SelectorNbtArgsNode(CmdNode):
    """
    Attributes:
        nbt_args (list of SelectorTagArgNode objects)
    """
    def __init__(self, nbt_args):
        assert_list_types(nbt_args, SelectorTagArgNode)
        self.nbt_args = nbt_args

class SelectorNbtArgNode(CmdNode):
    """
    Attributes:
        nbt (NbtObjectNode)
        negated (bool)
    """
    def __init__(self, nbt, negated=False):
        assert_type(nbt, NbtObjectNode)
        assert_type(negated, bool)
        self.nbt = nbt
        self.negated = negated

class SelectorAdvancementGroupArgNode(CmdNode):
    """
    Attributes:
        advancements (?)
    """
    def __init__(self, advancements):
        self.advancements = advancements


class NbtNode(CmdNode, ABC):
    pass

class NbtObjectNode(NbtNode):
    """
    Attributes:
        mappings (list of NbtMapNode objects)
    """
    def __init__(self, mappings):
        assert_list_types(mappings, NbtMapNode, duplicate_key=lambda x: x.arg.value)
        self.mappings = mappings

class NbtMapNode(NbtNode):
    """
    Attributes:
        arg (Token)
        value (Token, NbtObjectNode, NbtArrayNode, NbtIntegerNode, NbtFloatNode)
    """
    def __init__(self, arg, value):
        assert_type(arg, Token)
        assert_type(value, Token, NbtObjectNode, NbtArrayNode, NbtIntegerNode, NbtFloatNode)
        self.arg = arg
        self.value = value

class NbtArrayNode(NbtNode):
    """
    Attributes:
        values (list of NbtNode objects)
        type_specifier (Token or None)
    """
    def __init__(self, values, type_specifier=None):
        assert_list_types(values, Token, NbtObjectNode, NbtArrayNode, NbtIntegerNode, NbtFloatNode)
        assert_type(type_specifier, Token, optional=True)
        self.values = values
        self.type_specifier = type_specifier

class NbtIntegerNode(NbtNode):
    """
    Attributes:
        int_value (Token)
        int_type (Token or None)
    """
    def __init__(self, int_value, int_type=None):
        assert_type(int_value, Token)
        assert_type(int_type, Token, optional=True)
        self.int_value = int_value
        self.int_type = int_type

class NbtFloatNode(NbtNode):
    """
    Attributes:
        float_value (Token)
        float_type (Token or None)
    """
    def __init__(self, float_value, float_type=None):
        assert_type(float_value, Token)
        assert_type(float_type, Token, optional=True)
        self.float_value = float_value
        self.float_type = float_type


class JsonNode(CmdNode, ABC):
    pass

class JsonObjectNode(JsonNode):
    """
    Attributes:
        mappings (list of JsonMapNode objects)
    """
    def __init__(self, mappings):
        assert_list_types(mappings, JsonMapNode, duplicate_key=lambda x: x.arg.value)
        self.mappings = mappings

class JsonMapNode(JsonNode):
    """
    Attributes:
        arg (Token)
        value (Token, JsonArrayNode, JsonObjectNode)
    """
    def __init__(self, arg, value):
        assert_type(arg, Token)
        assert_type(value, Token, JsonArrayNode, JsonObjectNode)
        self.arg = arg
        self.value = value

class JsonArrayNode(JsonNode):
    """
    Attributes:
        values (list of Token, JsonArrayNode, JsonObjectNode)
    """
    def __init__(self, values):
        assert_list_types(values, Token, JsonArrayNode, JsonObjectNode)
        self.values = values


class IntRangeNode(CmdNode):
    """
    Note that a range can be a singular number. If so, left_int is the same as right_int

    Attributes:
        min_int (Token or None)
        max_int (Token or None)
        args (tuple of 2 strs or None): Contains the argument for the min int and the max int (eg. (rm, r))
    """
    def __init__(self, min_int, max_int, args=()):
        assert_type(min_int, Token, optional=True)
        assert_type(max_int, Token, optional=True)
        assert not (min_int is None and max_int is None)
        assert_tuple_types(args, str)
        assert len(args) in (0, 2)

        # checks whether the number actually works as a 32 bit signed int
        if min_int is not None:
            assert (-1<<31) <= int(min_int.value) <= ((1<<31)-1)
        if max_int is not None:
            assert (-1<<31) <= int(max_int.value) <= ((1<<31)-1)

        # checks whether the max int is actually greater than or equal to the min int if they both exist
        if min_int is not None and max_int is not None:
            assert int(max_int.value) >= int(min_int.value)

        self.min_int = min_int
        self.max_int = max_int
        self.args = args

class NumberRangeNode(CmdNode):
    """
    Note that a range can be a singular number. If so, min_number is the same as max_number

    Attributes:
        min_number (Token or None)
        max_number (Token or None)
    """
    def __init__(self, min_number, max_number):
        assert_type(min_number, Token, optional=True)
        assert_type(max_number, Token, optional=True)
        assert not (min_number is None and max_number is None)
        self.min_number = min_number
        self.max_number = max_number

class BlockNode(CmdNode):
    """
    Attributes:
        block (Token)
        states (Token or list of BlockStateNode objects or None)
        nbt (NbtObjectNode or None)
    """
    def __init__(self, block, states, nbt=None):
        assert_type(block, Token)
        assert_list_types(states, BlockStateNode) if isinstance(states, list) else assert_type(states, Token, optional=True)
        assert_type(nbt, NbtObjectNode, optional=True)
        self.block = block
        self.states = states
        self.nbt = nbt

class BlockStateNode(CmdNode):
    """
    Attributes:
        arg (Token)
        value (Token)
    """
    def __init__(self, arg, value):
        assert_type(arg, Token)
        assert_type(value, Token)
        self.arg = arg
        self.value = value

class Vec2Node(CmdNode):
    """
    Attributes:
        coord1 (Token)
        coord2 (Token)
    """
    def __init__(self, coord1, coord2):
        assert_type(coord1, Token)
        assert_type(coord2, Token)
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
        assert_type(coord1, Token)
        assert_type(coord2, Token)
        assert_type(coord3, Token)
        self.coord1 = coord1
        self.coord2 = coord2
        self.coord3 = coord3

class NamespaceIdNode(CmdNode):
    """
    Attributes:
        namespace (Token or None)
        id_value (Token)
    """
    def __init__(self, id_value, namespace=None):
        assert_type(id_value, Token)
        assert_type(namespace, Token, optional=True)
        self.id_value = id_value
        self.namespace = namespace

class DataPathNode(CmdNode):
    """
    Attributes:
        path_tokens (list of Token objects)
    """
    def __init__(self, path_tokens):
        assert_list_types(path_tokens, Token)
        self.path_tokens = path_tokens


if __name__ == "__main__":
    # testing random hashes
    class A:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    a = A(1, [2, 3, 4])
    some_dict = {a: 1}
    print(some_dict)

