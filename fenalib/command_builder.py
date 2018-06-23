""" Contains node visitors for the AST of a command to build itself """

import logging
import os

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

    import fenalib.logging_setup as logging_setup

from fenalib.assert_utils import assert_type
from fenalib.lexical_token import Token
from fenalib.config_data import ConfigData
from fenalib.in_file_config import InFileConfig
from fenalib.node_visitors import NodeBuilder
from fenalib.nodes import CmdNode, IntRangeNode, SelectorDefaultGroupArgValueNode, JsonObjectNode, JsonMapNode, SelectorNode
from fenalib.number_utils import is_signed_int
from fenalib.str_utils import encode_str, decode_str
from fenalib.lexer import Lexer
from fenalib.parser import Parser

class CommandBuilder_1_12(NodeBuilder):
    """
    Attributes:
        cmd_root (Node): The parent node of the AST representing a command
        mcfunction_path (str): The full path to the mcfunction file used for smart function shortcuts)
    """

    config_data = ConfigData()
    in_file_config = InFileConfig()

    def __init__(self, cmd_root, mcfunction_path):
        assert_type(cmd_root, CmdNode, Token)
        assert_type(mcfunction_path, str)
        assert self.in_file_config.finalized
        self.cmd_root = cmd_root
        self.mcfunction_path = mcfunction_path

    def interpret(self):
        """
        Creates the full built command

        Returns:
            str: The full command as a string
        """
        return self.build(self.cmd_root)

    def build_FenaCmdNode(self, node):
        return self.iter_build(node.cmd_segment_nodes, " ")

    def build_ExecuteCmdNode(self, node):
        """
        Node Attributes:
            sub_cmd_nodes (list of ExecuteSubArgNode objects)
        """
        return self.iter_build(node.sub_cmd_nodes, ' ')

    def build_ExecuteSubLegacyArg(self, node):
        """
        turns to <selector> <vec3> [detect vec3 block_type data_value]

        Node Attributes:
            selector (SelectorNode)
            coords (Vec3Node or None)
            sub_if (list of ExecuteSubIfBlockArg objects)
        """
        if node.coords is None:
            coords = "~ ~ ~"
        else:
            coords = self.build(node.coords)
        selector = self.build(node.selector)

        # no detect area
        if not node.sub_if:
            return f"execute {selector} {coords}"

        # can have one or more detect areas
        result = []
        for index, sub_if in enumerate(node.sub_if):
            sub_if = self.build(sub_if)
            if index == 0:
                result.append(f"execute {selector} {coords} {sub_if}")
            else:
                result.append(f"execute @s {coords} {sub_if}")
        return " ".join(result)

    def build_ExecuteSubIfBlockArg(self, node):
        """
        Node Attributes:
            block (BlockNode)
            coords (Vec3Node or None)
        """
        if node.coords is None:
            coords = "~ ~ ~"
        else:
            coords = self.build(node.coords)

        block = self.build(node.block)
        return f"detect {coords} {block}"

    def build_DataMergeNode(self, node):
        """
        Node Attributes:
            entity_vec3 (SelectorNode, Vec3Node)
            nbt (NbtObjectNode)
        """
        data_select_type = "entitydata" if isinstance(node.entity_vec3, SelectorNode) else "blockdata"
        entity_vec3 = self.build(node.entity_vec3)
        nbt = self.build(node.nbt)
        return f"{data_select_type} {entity_vec3} {nbt}"

    def build_ScoreboardCmdMathNode(self, node):
        """
        Node Attributes:
            target (SelectorNode or Token)
            objective (Token)
            operator (Token)
            target_get (SelectorNode or Token)
            objective_get (Token or None)
        """
        target = self.build(node.target)
        objective = self.build(node.objective, prefix=True)
        operator = self.build(node.operator)
        target_get = self.build(node.target_get)
        objective_get = objective if node.objective_get is None else self.build(node.objective_get, prefix=True)
        return f"scoreboard players operation {target} {objective} {operator} {target_get} {objective_get}"

    def build_ScoreboardCmdMathValueNode(self, node):
        """
        Node Attributes:
            target (SelectorNode or Token)
            objective (Token)
            operator (Token)
            value (Token)
            nbt (NbtObjectNode)
        """
        target = self.build(node.target)
        objective = self.build(node.objective, prefix=True)
        operator = self.build(node.operator)
        value = self.build(node.value)
        nbt = "" if node.nbt is None else self.build(node.nbt)

        # simply cannot have nbt data in 1.13
        assert node.nbt is None or (node.nbt is not None and self.config_data.version == "1.12")

        # simple command that can contain nbt
        operation_dict = {"=": "set", "+=": "add", "-=": "remove"}
        if operator in operation_dict:
            operation = operation_dict[operator]
            if nbt:
                return f"scoreboard players {operation} {target} {objective} {value} {nbt}"
            return f"scoreboard players {operation} {target} {objective} {value}"

        # otherwise, scoreboard players operation
        if node.nbt is not None:
            raise SyntaxError(f"NBT arguments are not allowed with 'scoreboard players operation' {node.nbt}")

        constobj = self.in_file_config.constobj

        # <= sets the target to the score if and only if the target has a larger score compared to the value
        # therefore making the target score less than or equal to the value
        # >= sets the target to the score if and only if the target has a smaller score compared to the value
        # therefore making the target score greater than or equal to the value

        if operator in ("*=", "/=", "%=", "<", ">"):
            return f"scoreboard players operation {target} {objective} {operator} {value} {constobj}"

        if operator == "><":
            # no reason to swap with a constant value
            raise SyntaxError(f"Cannot swap with a constant value with operator {node.operator}")

        raise SyntaxError("Unknown default case")

    def build_ScoreboardCmdSpecialNode(self, node):
        """
        Args:
            node (ScoreboardCmdSpecialNode)
        """
        # sub_cmd = self.build(node.sub_cmd, replacements={"<-": "get"})
        sub_cmd = self.build(node.sub_cmd)
        target = self.build(node.target)
        objective = self.build(node.objective, prefix=True)
        return f"scoreboard players {sub_cmd} {objective} {target}"

    def build_EffectClearNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            effect_id (NamespaceIdNode or None)
        """
        selector = self.build(node.selector)
        if node.effect_id is None:
            return f"effect {selector} clear"

        effect_id = self.build(node.effect_id)
        return f"effect {selector} {effect_id} 0 0 true"

    def build_EffectGiveNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            effect_id (NamespaceIdNode)
            duration (Token or None)
            level (Token or None)
            hide_particles (bool)
        """
        selector = self.build(node.selector)
        effect_id = self.build(node.effect_id)
        duration = "2" if node.duration is None else self.build(node.duration)
        level = "0" if node.level is None else self.build(node.level)
        hide_particles = "true" if node.hide_particles else "false"
        return f"effect {selector} {effect_id} {duration} {level} {hide_particles}"

    def build_FunctionCmdNode(self, node):
        """
        Node Attributes:
            value (Token)
            namespace (Token or None)
        """
        if node.namespace is None:
            function_shortcut = self.build(node.value)
        else:
            value = self.build(node.value)
            namespace = self.build(node.namespace)
            function_shortcut = f"{namespace}:{value}"

        if function_shortcut in self.in_file_config.function_conflicts:
            # smart assigning
            raise NotImplementedError()

        function_name = self.in_file_config.functions[function_shortcut]
        return f"function {function_name}"

    def build_SimpleCmdNode(self, node):
        """
        Args:
            node (SimpleCmdNode)
        """
        return self.iter_build(node.tokens, " ")

    def build_ItemGiveNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            item (ItemNode)
            count (Token or None)
        """
        selector = self.build(node.selector)
        item_id = self.build(node.item.item_id)
        count = "1" if node.count is None else self.build(node.count)
        damage = "0" if node.item.damage is None else self.build(node.item.damage)

        if node.item.nbt is not None:
            nbt = self.build(node.item.nbt)
            return f"give {selector} minecraft:{item_id} {count} {damage} {nbt}"

        return f"give {selector} minecraft:{item_id} {count} {damage}"

    def build_ItemClearNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            item (ItemNode)
            count (Token or None)
        """
        selector = self.build(node.selector)
        if isinstance(node.item, Token):
            return f"clear {selector}"

        item_id = self.build(node.item.item_id)
        count = "-1" if node.count is None else self.build(node.count)
        damage = "-1" if node.item.damage is None else self.build(node.item.damage)

        if node.item.nbt is not None:
            nbt = self.build(node.item.nbt)
            return f"clear {selector} minecraft:{item_id} {damage} {count} {nbt}"

        return f"clear {selector} minecraft:{item_id} {damage} {count}"

    def build_ItemReplaceEntityNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            slot (Token)
            item (ItemNode)
            count (Token or None)
        """
        selector = self.build(node.selector)
        slot = self.build(node.slot)
        item_id = self.build(node.item.item_id)
        count = "1" if node.count is None else self.build(node.count)
        damage = "0" if node.item.damage is None else self.build(node.item.damage)

        if node.item.nbt is not None:
            nbt = self.build(node.item.nbt)
            return f"replaceitem entity {selector} slot.{slot} minecraft:{item_id} {count} {damage} {nbt}"
        return f"replaceitem entity {selector} slot.{slot} minecraft:{item_id} {count} {damage}"

    def build_ItemReplaceBlockNode(self, node):
        """
        Node Attributes:
            vec3 (Vec3Node)
            slot (Token)
            item (ItemNode)
            count (Token or None)
        """
        vec3 = self.build(node.vec3)
        slot = self.build(node.slot)
        item_id = self.build(node.item.item_id)
        count = "1" if node.count is None else self.build(node.count)
        damage = "0" if node.item.damage is None else self.build(node.item.damage)

        if node.item.nbt is not None:
            nbt = self.build(node.item.nbt)
            return f"replaceitem block {vec3} slot.{slot} minecraft:{item_id} {count} {damage} {nbt}"
        return f"replaceitem block {vec3} slot.{slot} minecraft:{item_id} {count} {damage}"

    def build_TagAddNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            tag (Token)
            nbt (NbtObjectNode or None)
        """
        selector = self.build(node.selector)
        tag = self.build(node.tag, prefix=True)
        if node.nbt is None:
            return f"scoreboard players tag {selector} add {tag}"

        nbt = self.build(node.nbt)
        return f"scoreboard players tag {selector} add {tag} {nbt}"

    def build_TagRemoveNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            tag (Token)
            nbt (NbtObjectNode or None)
        """
        selector = self.build(node.selector)
        tag = self.build(node.tag, prefix=True)
        if node.nbt is None:
            return f"scoreboard players tag {selector} remove {tag}"

        nbt = self.build(node.nbt)
        return f"scoreboard players tag {selector} remove {tag} {nbt}"


    def build_TeamAddNode(self, node):
        """
        Args:
            node (TeamAddNode)
            display_name (list of Token objects)
        """
        team_name = self.build(node.team_name, prefix=True)
        if not node.display_name:
            return f"scoreboard teams add {team_name}"

        display_name = self.iter_build(node.display_name, " ")
        return f"scoreboard teams add {team_name} {display_name}"

    def build_TeamJoinNode(self, node):
        """
        Args:
            node (TeamJoinNode)
        """
        team_name = self.build(node.team_name, prefix=True)
        target = self.build(node.target)
        return f"scoreboard teams join {team_name} {target}"

    def build_TeamLeaveNode(self, node):
        """
        Args:
            node (TeamLeaveNode)
        """
        target = self.build(node.target)
        return f"scoreboard teams leave {target}"

    def build_TeamEmptyNode(self, node):
        """
        Args:
            node (TeamEmptyNode)
        """
        team_name = self.build(node.team_name, prefix=True)
        return f"scoreboard teams empty {team_name}"

    def build_TeamOptionNode(self, node):
        """
        Args:
            node (TeamOptionNode)
        """
        team_name = self.build(node.team_name, prefix=True)
        option = self.build(node.option)
        value = self.build(node.value)
        return f"scoreboard teams option {team_name} {option} {value}"

    def build_TeamRemoveNode(self, node):
        """
        Args:
            node (TeamRemoveNode)
        """
        team_name = self.build(node.team_name, prefix=True)
        return f"scoreboard teams remove {team_name}"

    def build_XpMathNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            operator (Token)
            value (Token)
            sub_cmd (Token or None)
        """
        selector = self.build(node.selector)
        operator = self.build(node.operator)
        value = self.build(node.value)
        sub_cmd = "points" if node.sub_cmd is None else self.build(node.sub_cmd)

        if operator == "=":
            raise SyntaxError(f"Xp cannot be set to a specific amount in 1.12 with {node}")
        if operator == "-" and sub_cmd == "points":
            raise SyntaxError(f"Xp cannot be removed in point increments in 1.12 with {node}")

        value_ending = "" if sub_cmd == "points" else "L"
        negative = "-" if operator == "-" else ""

        return f"xp {selector} {negative}{value}{value_ending}"

    def build_SelectorNode(self, node):
        """
        Node Attributes:
            selector_var (SelectorVarNode)
            selector_args (SelectorArgsNode or None)
        """
        selector_var = self.build(node.selector_var)

        if node.selector_args is None:
            return f"{selector_var}"

        selector_args = self.build(node.selector_args)
        return f"{selector_var}[{selector_args}]"

    def build_SelectorVarNode(self, node):
        """
        Node Attributes:
            selector_var_specifier (Token)
        """
        selector_var_specifier = self.build(node.selector_var_specifier)
        return f"@{selector_var_specifier}"

    def build_SelectorArgsNode(self, node):
        """
        Attributes:
            default_args (list of SelectorDefaultArgNode objects)
            score_args (SelectorScoreArgsNode)
            tag_args (SelectorTagArgsNode)
            nbt_args (SelectorNbtArgsNode)
            advancement_args (SelectorAdvancementGroupArgNode)
        """
        # all_args = (node.default_args, node.score_args, node.tag_args, node.nbt_args, node.advancement_args)

        # note that map returns a generator
        # all_built_args = map(lambda x: ",".join(self.iter_build(x)), all_args)
        default_args = self.iter_build(node.default_args, ",")
        score_args = self.build(node.score_args)
        tag_args = self.build(node.tag_args)
        nbt_args = self.build(node.nbt_args)
        advancement_args = self.build(node.advancement_args)

        all_built_args = (default_args, score_args, tag_args, nbt_args, advancement_args)
        # removes any 0 length strings
        return ",".join(x for x in all_built_args if x)

    def build_SelectorScoreArgsNode(self, node):
        """
        Node Attributes:
            score_args (list of SelectorScoreArgNode objects)
        """
        return self.iter_build(node.score_args, ",")

    def build_SelectorScoreArgNode(self, node):
        """
        Node Attributes:
            objective (Token)
            value (IntRangeNode, Token)
        """
        objective = self.build(node.objective, prefix=True)
        result = []

        # checks if the value is an IntRangeNode or a TypedToken.STIRNG with value="*"
        if isinstance(node.value, Token):
            # gets the smallest value of a 32 bit signed integer and select all above that
            min_int = -1<<31
            result.append(f"score_{objective}_min={min_int}")

        else:
            # actually uses the values of the min_int from the integer range
            if node.value.min_int is not None:
                min_int = self.build(node.value.min_int)
                result.append(f"score_{objective}_min={min_int}")
            if node.value.max_int is not None:
                max_int = self.build(node.value.max_int)
                result.append(f"score_{objective}={max_int}")

        assert result, "why the hell would there not be a result"
        return ",".join(result)

    def build_SelectorDefaultArgNode(self, node):
        """
        Node Attributes:
            arg (Token)
            arg_value (SelectorDefaultArgValueNode, SelectorDefaultGroupArgValueNode)
        """
        # int range node should have the arguments inside node.args
        # therefore, only the int range node should be built
        if isinstance(node.arg_value.arg_value, IntRangeNode):
            return self.build(node.arg_value.arg_value)

        arg = self.build(node.arg)
        arg_value = self.build(node.arg_value)
        return f"{arg}={arg_value}"

    def build_SelectorDefaultArgValueNode(self, node):
        """
        Node Attributes:
            arg_value (Token, NumberRangeNode, IntRangeNode)
            negated (bool)
        """
        negated = "!" if node.negated else ""
        arg_value = self.build(node.arg_value)
        return f"{negated}{arg_value}"

    def build_SelectorDefaultGroupArgValueNode(self, node):
        """
        Node Attributes:
            arg_values (list of Token objects)
        """
        raise SyntaxError("Cannot build a selector group value node in 1.12")

    def build_SelectorTagArgsNode(self, node):
        """
        Node Attributes:
            tag_args (list of SelectorTagArgNode objects)
        """
        # requires the tag args to be less than one for length
        if len(node.tag_args) > 1:
            raise SyntaxError("Cannot have more than one tag inside a selector for 1.12")

        return self.iter_build(node.tag_args, ",")

    def build_SelectorTagArgNode(self, node):
        """
        Node Attributes:
            tag (Token)
            negated (bool)
        """
        negated = "!" if node.negated else ""
        tag = self.build(node.tag, prefix=True)
        return f"tag={negated}{tag}"

    def build_SelectorNbtArgsNode(self, node):
        """
        Node Attributes:
            nbt_args (list of SelectorTagArgNode objects)
        """
        if node.nbt_args:
            raise SyntaxError("Cannot build a selector nbt node in 1.12")
        return ""

    def build_SelectorNbtArgNode(self, node):
        """
        Node Attributes:
            nbt (NbtNode)
            negated (bool)
        """
        raise SyntaxError("Cannot build a selector nbt node in 1.12")

    def build_SelectorAdvancementGroupArgNode(self, node):
        """
        Attributes:
            advancements (?)
        """
        if node.advancements:
            raise SyntaxError("Cannot build a selector advancement node in 1.12")
        return ""

    def build_NbtObjectNode(self, node):
        """
        Node Attributes:
            mappings (list of NbtMapNode objects)
        """
        return "{" + self.iter_build(node.mappings, ",") + "}"

    def build_NbtMapNode(self, node):
        """
        Node Attributes:
            arg (Token)
            value (Token)
        """
        arg = self.build(node.arg)
        value = self.build(node.value)
        return f"{arg}:{value}"

    def build_NbtArrayNode(self, node):
        """
        Node Attributes:
            values (list of NbtNode objects)
            type_specifier (Token or None)
        """
        values = self.iter_build(node.values, ",")
        type_specifier = ("" if node.type_specifier is None else f"{self.build(node.type_specifier)};")
        return f"[{type_specifier}{values}]"

    def build_NbtIntegerNode(self, node):
        """
        Node Attributes:
            int_value (Token)
            int_type (Token or None)
        """
        int_value = self.build(node.int_value)
        if node.int_type is None:
            return int_value

        int_type = self.build(node.int_type)
        return f"{int_value}{int_type}"

    def build_NbtFloatNode(self, node):
        """
        Node Attributes:
            float_value (Token)
            float_type (Token or None)
        """
        float_value = self.build(node.float_value)
        if node.float_type is None:
            return float_value

        float_type = self.build(node.float_type)
        return f"{float_value}{float_type}"

    def build_JsonObjectNode(self, node, previous_arg=None):
        """
        Attributes:
            mappings (list of JsonMapNode objects)
        """
        result = []
        for mapping in node.mappings:
            if isinstance(mapping, JsonMapNode):
                result.append(self.build(mapping, previous_arg=previous_arg))
            else:
                result.append(self.build(mapping))

        return "{" + ",".join(result) + "}"

    def build_JsonMapNode(self, node, previous_arg=None):
        """
        Attributes:
            arg (Token)
            value (Token, JsonArrayNode, JsonObjectNode)
        """
        arg = self.build(node.arg)

        # only passes on the current argument down if the value is also a json map node
        if isinstance(node.value, JsonObjectNode):
            # passes the argument "score" in so the "name" arg under "score" can be converted into a proper selector
            current_arg = '"score"' if arg == '"score"' else None
            value = self.build(node.value, previous_arg=current_arg)
        else:
            value = self.build(node.value)

        # if the argument is a selector, it builds a selector
        if arg == '"selector"':
            selector = decode_str(value)
            lexer = Lexer(selector)
            parser = Parser(lexer, method_name="get_selector")
            ast = parser.parse(method_name="selector")
            result = self.build_SelectorNode(ast)
            value = encode_str(result)

        if previous_arg == '"score"':
            # gets one token, and builds it with a possible prefix
            if arg == '"objective"':
                target = decode_str(value)
                lexer = Lexer(target)
                parser = Parser(lexer, method_name="get_until_space")
                ast = parser.parse(method_name="advance")
                result = self.build_Token(ast, prefix=True)
                value = encode_str(result)

            # gets some target, so the get_command is versatile enough to get either a selector or single token
            elif arg == '"name"':
                target = decode_str(value)
                lexer = Lexer(target)
                parser = Parser(lexer, method_name="get_command")
                ast = parser.parse(method_name="target")
                result = self.build(ast)
                value = encode_str(result)

        return f"{arg}:{value}"

    def build_JsonArrayNode(self, node):
        """
        Attributes:
            values (list of Token, JsonArrayNode, JsonObjectNode)
        """
        return "[" + self.iter_build(node.values, ",") + "]"

    def build_IntRangeNode(self, node):
        """
        Note that a range can be a singular number. If so, left_int is the same as right_int

        Node Attributes:
            min_int (Token or None)
            max_int (Token or None)
            args (tuple of 2 strs or None): Contains the argument for the min int and the max int (eg. (rm, r))
        """
        # means that max_arg is also not none
        if len(node.args) == 0:
            raise SyntaxError(f"Cannot build {node!r} by itself without specifying any `args` value")

        min_arg, max_arg = node.args

        # gets each individual min or max selector arg/value pair
        result = []
        if node.min_int is not None:
            min_int = self.build(node.min_int)
            result.append(f"{min_arg}={min_int}")
        if node.max_int is not None:
            max_int = self.build(node.max_int)
            result.append(f"{max_arg}={max_int}")

        return ",".join(result)

    def build_NumberRangeNode(self, node):
        raise NotImplementedError("1.13+")

    def build_BlockNode(self, node):
        """
        Node Attributes:
            block (Token)
            states (Token or list of BlockStateNode objects or None)
            nbt (NbtObjectNode or None)
        """
        block = self.build(node.block)

        # counts for if node.states is None or an empty list
        if not node.states:
            states = "*"
        elif isinstance(node.states, list):
            states = self.iter_build(node.states, ",")
        elif isinstance(node.states, Token):
            states = self.build(node.states)
        else:
            raise SyntaxError("Unexpected default case")

        if node.nbt is None:
            return f"minecraft:{block} {states}"

        nbt = self.build(node.nbt)
        return f"minecraft:{block} {states} replace {nbt}"

    def build_BlockStateNode(self, node):
        """
        Attributes:
            arg (Token)
            value (Token)
        """
        arg = self.build(node.arg)
        value = self.build(node.value)
        return f"{arg}={value}"

    def build_Vec2Node(self, node):
        coord1 = self.build(node.coord1)
        coord2 = self.build(node.coord2)
        return f"{coord1} {coord2}"

    def build_Vec3Node(self, node):
        coord1 = self.build(node.coord1)
        coord2 = self.build(node.coord2)
        coord3 = self.build(node.coord3)
        return f"{coord1} {coord2} {coord3}"

    def build_NamespaceIdNode(self, node):
        """
        Attributes:
            id_value (Token)
            namespace (Token or None)
        """
        id_value = self.build(node.id_value, prefix=True)
        namespace = ("minecraft" if node.namespace is None else self.build(node.namespace))
        return f"{namespace}:{id_value}"

    def build_Token(self, token, prefix=False, replacements=None):
        """
        Returns its value with a prefix if avaliable

        Args:
            prefix (bool): Whether the value might have a prefix placeholder or not
            replacements (dict): Any possible replacements to the token valuestring

        Returns:
            str: The new string that is guaranteed to have a prefix
        """
        assert_type(prefix, bool)
        assert_type(replacements, dict, optional=True)

        # prioritizes replacement over value
        string = token.replacement if (token.replacement is not None) else str(token.value)

        if prefix:
            if string.startswith("_"):
                # string=__ti -> fena._ti
                # string=_ti -> fena.ti
                prefix_str = self.in_file_config.prefix
                return f"{prefix_str}.{string[1:]}"

            if "." not in string and self.config_data.ego:
                logging.warning(f"No prefix given to {token!r}")

        if replacements is not None:
            return replacements.get(string, string)

        return string

    def build_str(self, node):
        """
        Literally just returns itself lmao
        """
        return node

# TODO finish 1.13
class CommandBuilder_1_13(CommandBuilder_1_12):
    def __init__(self, *args):
        super().__init__(*args)

    def build_FenaCmdNode(self, node):
        # gets rid of a trailing " run" if it exists
        command = self.iter_build(node.cmd_segment_nodes, " ")
        if command.endswith(" run"):
            return command[:-len(" run")]
        return command

    def build_SelectorScoreArgsNode(self, node):
        """
        Node Attributes:
            score_args (list of SelectorScoreArgNode objects)
        """
        return "scores={" + self.iter_build(node.score_args, ",") + "}" if node.score_args else ""

    def build_SelectorScoreArgNode(self, node):
        """
        Node Attributes:
            objective (Token)
            value (IntRangeNode, Token)
        """
        objective = self.build(node.objective, prefix=True)

        # checks if the value is an IntRangeNode or a TypedToken.STIRNG with value="*"
        if isinstance(node.value, Token):
            # gets the smallest value of a 32 bit signed integer and select all above that
            min_int = -1<<31
            return f"{objective}={min_int}.."

        # actually uses the values of the min_int from the integer range
        range_str = self.build(node.value)
        return f"{objective}={range_str}"

    def build_SelectorDefaultArgNode(self, node):
        """
        Node Attributes:
            arg (Token)
            arg_value (SelectorDefaultArgValueNode, SelectorDefaultGroupArgValueNode)
        """
        arg = self.build(node.arg)
        if isinstance(node.arg_value, SelectorDefaultGroupArgValueNode):
            result = []
            for arg_value in self.iter_build(node.arg_value.arg_values):
                result.append(f"{arg}={arg_value}")
            return ",".join(result)

        # otherwise, a regular argument value
        arg_value = self.build(node.arg_value)
        return f"{arg}={arg_value}"

    def build_SelectorTagArgsNode(self, node):
        """
        Node Attributes:
            tag_args (list of SelectorTagArgNode objects)
        """
        return self.iter_build(node.tag_args, ",")

    def build_SelectorNbtArgsNode(self, node):
        """
        Node Attributes:
            nbt_args (list of SelectorTagArgNode objects)
        """
        # concatenates all negated and non-negated nbt tags into their own lists
        negated_nbt = []
        non_negated_nbt = []

        for nbt_arg in node.nbt_args:
            built_nbt_arg = self.build(nbt_arg)
            if nbt_arg.negated:
                negated_nbt.append(built_nbt_arg)
            else:
                non_negated_nbt.append(built_nbt_arg)

        built_negated = "nbt={" + ",".join(negated_nbt) + "}" if negated_nbt else ""
        built_non_negated = "nbt=!{" + ",".join(non_negated_nbt) + "}" if non_negated_nbt else ""
        all_built_nbt = (nbt for nbt in (built_negated, built_non_negated) if nbt)
        return ",".join(all_built_nbt)

    def build_SelectorNbtArgNode(self, node):
        """
        Node Attributes:
            nbt (NbtNode)
            negated (bool)
        """
        nbt = self.build(node.nbt)
        negated = "!" if node.negated else ""
        return f"{negated}{nbt}"

    def build_SelectorAdvancementGroupArgNode(self, node):
        """
        Node Attributes:
            advancements (?)
        """
        return self.iter_build(node.advancements, ",")

    def build_IntRangeNode(self, node):
        """
        Note that a range can be a singular number. If so, left_int is the same as right_int

        Node Attributes:
            min_int (Token or None)
            max_int (Token or None)
            args (tuple of 2 strs or None): Contains the argument for the min int and the max int (eg. (rm, r))
        """
        # means that max_arg is also not none
        assert len(node.args) == 0

        # gets each individual min or max selector arg/value pair
        min_int = ("" if node.min_int is None else self.build(node.min_int))
        max_int = ("" if node.max_int is None else self.build(node.max_int))
        if min_int == max_int:
            return min_int
        return f"{min_int}..{max_int}"

    def build_NumberRangeNode(self, node):
        """
        Note that a range can be a singular number. If so, left_int is the same as right_int

        Node Attributes:
            min_number (Token or None)
            max_number (Token or None)
        """
        # gets each individual min or max selector arg/value pair
        min_number = ("" if node.min_number is None else self.build(node.min_number))
        max_number = ("" if node.max_number is None else self.build(node.max_number))
        if min_number == max_number:
            return min_number
        return f"{min_number}..{max_number}"

    def build_BlockNode(self, node):
        """
        Node Attributes:
            block (Token)
            states (Token or list of BlockStateNode objects or None)
            nbt (NbtObjectNode or None)
        """
        block = self.build(node.block)

        # just making sure, shis should've been checked at parsing
        assert not isinstance(node.states, Token)

        # counts for if node.states is None or an empty list
        if not node.states:
            states = ""
        elif isinstance(node.states, list):
            states = "[" + self.iter_build(node.states, ",") + "]"
        else:
            raise SyntaxError("Unexpected default case")

        nbt = "" if node.nbt is None else self.build(node.nbt)

        return f"minecraft:{block}{states}{nbt}"

    def build_BlockStateNode(self, node):
        """
        Node Attributes:
            arg (Token)
            value (Token)
        """
        arg = self.build(node.arg)
        value = self.build(node.value)
        return f"{arg}={value}"

    def build_ExecuteCmdNode(self, node):
        """
        Node Attributes:
            sub_cmd_nodes (list of ExecuteSubArgNode objects)
        """
        return f"execute {self.iter_build(node.sub_cmd_nodes, ' ')} run"

    def build_ExecuteSubAsArg(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
        """
        selector = self.build(node.selector)
        return f"as {selector}"

    def build_ExecuteSubPosVec3Arg(self, node):
        """
        Node Attributes:
            vec3 (Vec3Node)
        """
        vec3 = self.build(node.vec3)
        return f"positioned {vec3}"

    def build_ExecuteSubPosSelectorArg(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
        """
        selector = self.build(node.selector)
        return f"positioned as {selector}"

    def build_ExecuteSubAtAnchorArg(self, node):
        """
        Node Attributes:
            anchor (Token)
        """
        anchor = self.build(node.anchor)
        return f"anchored {anchor} positioned ^ ^ ^"

    def build_ExecuteSubAtSelectorArg(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
        """
        selector = self.build(node.selector)
        return f"at {selector}"

    def build_ExecuteSubAtCoordsArg(self, node):
        """
        Node Attributes:
            vec3 (Vec3Node)
            vec2 (Vec2Node)
        """
        vec3 = self.build(node.vec3)
        vec2 = self.build(node.vec2)
        return f"positioned {vec3} facing {vec2}"

    def build_ExecuteSubAtAxesArg(self, node):
        """
        Node Attributes:
            axes (Token)
        """
        axes = self.build(node.axes)
        return f"align {axes}"

    def build_ExecuteSubFacingVec3Arg(self, node):
        """
        Node Attributes:
            vec2 (Vec2Node)
        """
        vec3 = self.build(node.vec3)
        return f"facing {vec3}"

    def build_ExecuteSubFacingSelectorArg(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            anchor (Token or None)
        """
        selector = self.build(node.selector)
        if node.anchor is None:
            anchor = "feet"
        else:
            anchor = self.build(node.anchor)
        return f"facing entity {selector} {anchor}"

    def build_ExecuteSubRotSelectorArg(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
        """
        selector = self.build(node.selector)
        return f"rotated as {selector}"

    def build_ExecuteSubRotVec2Arg(self, node):
        """
        Node Attributes:
            vec2 (Vec2Node)
        """
        vec2 = self.build(node.vec2)
        return f"rotated {vec2}"

    def build_ExecuteSubAnchorArg(self, node):
        """
        Node Attributes:
            axes (Token)
        """
        axes = self.build(node.axes)
        return f"anchored {axes}"

    def build_ExecuteSubInArg(self, node):
        """
        Node Attributes:
            dimension (Token)
        """
        dimension = self.build(node.dimension)
        return f"in {dimension}"

    def build_ExecuteSubAstArg(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
        """
        selector = self.build(node.selector)
        return f"as {selector} at @s"

    def build_ExecuteSubIfSelectorArg(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
        """
        selector = self.build(node.selector)
        return f"{node.sub_cmd} entity {selector}"

    def build_ExecuteSubIfBlockArg(self, node):
        """
        Node Attributes:
            block (BlockNode)
            coords (Vec3Node or None)
        """

        if node.coords is None:
            coords = "~ ~ ~"
        else:
            coords = self.build(node.coords)
        block = self.build(node.block)

        return f"{node.sub_cmd} block {coords} {block}"

    def build_ExecuteSubIfBlocksArg(self, node):
        """
        Node Attributes:
            coords1 (Vec3Node)
            coords2 (Vec3Node)
            coords3 (Vec3Node)
            option (Token or None)
        """

        coords1 = self.build(node.coords1)
        coords2 = self.build(node.coords2)
        coords3 = self.build(node.coords3)

        if node.option is None:
            option = "all"
        else:
            option = self.build(node.option)

        return f"{node.sub_cmd} blocks {coords1} {coords2} {coords3} {option}"

    def build_ExecuteSubIfCompareEntityArg(self, node):
        """
        Node Attributes:
            target (SelectorNode or Token)
            objective (Token)
            operator (Token)
            target_get (SelectorNode)
            objective_get (Token)
        """
        target = self.build(node.target)
        objective = self.build(node.objective, prefix=True)
        operator = self.build(node.operator)
        target_get = self.build(node.target_get)
        objective_get = self.build(node.objective_get, prefix=True)

        return f"{node.sub_cmd} score {target} {objective} {operator} {target_get} {objective_get}"

    def build_ExecuteSubIfCompareIntArg(self, node):
        """
        Node Attributes:
            target (SelectorNode or Token)
            objective (Token)
            operator (Token)
            value (Token)
        """
        target = self.build(node.target)
        objective = self.build(node.objective, prefix=True)
        operator = self.build(node.operator)
        int_value = self.build(node.value)
        sub_cmd = node.sub_cmd

        if int_value == "*":
            int_value = f"{-(1<<31)}.."
        else:
            int_value = int(int_value)

        if operator == "=":
            int_range = int_value
        elif operator == "<":
            int_range = "..{}".format(int_value-1)
        elif operator == "<=":
            int_range = "..{}".format(int_value)
        elif operator == ">":
            int_range = "{}..".format(int_value+1)
        elif operator == ">=":
            int_range = "{}..".format(int_value)
        else:
            raise SyntaxError("Unknown default case")

        return f"{sub_cmd} score {target} {objective} matches {int_range}"

    def build_ExecuteSubIfRangeArg(self, node):
        """
        Node Attributes:
            target (SelectorNode or Token)
            objective (Token)
            int_range (IntRangeNode)
        """
        target = self.build(node.target)
        objective = self.build(node.objective, prefix=True)
        int_range = self.build(node.int_range)
        return f"{node.sub_cmd} score {target} {objective} matches {int_range}"

    def build_ExecuteSubStoreSelectorDataArg(self, node):
        """
        Node Attributes:
            selector (SelectorNode, Vec3Node)
            data_path (DataPathNode)
            scale (Token)
            data_type (Token)
        """
        selector = self.build(node.selector)
        data_path = self.build(node.data_path)
        scale = self.build(node.scale)
        if node.data_type is None:
            if is_signed_int(scale):
                data_type = "long"
            else:
                data_type = "double"
        else:
            data_type = self.build(node.data_type)
        return f"store {node.store_type} entity {selector} {data_path} {data_type} {scale}"

    def build_ExecuteSubStoreVec3DataArg(self, node):
        """
        Node Attributes:
            vec3 (SelectorNode, Vec3Node)
            data_path (DataPathNode)
            scale (Token)
            data_type (Token)
        """
        vec3 = self.build(node.vec3)
        data_path = self.build(node.data_path)
        scale = self.build(node.scale)
        if node.data_type is None:
            if is_signed_int(scale):
                data_type = "long"
            else:
                data_type = "double"
        else:
            data_type = self.build(node.data_type)
        return f"store {node.store_type} block {vec3} {data_path} {data_type} {scale}"

    def build_ExecuteSubStoreScoreArg(self, node):
        """
        Node Attributes:
            target (SelectorNode or Token)
            objective (Token)
        """
        target = self.build(node.target)
        objective = self.build(node.objective, prefix=True)
        return f"store {node.store_type} score {target} {objective}"

    def build_ExecuteSubStoreBossbarArg(self, node):
        """
        Node Attributes:
            bossbar_id (NamespaceIdNode)
            sub_cmd (Token)
        """
        bossbar_id = self.build(node.bossbar_id)
        sub_cmd = self.build(node.sub_cmd)
        return f"store {node.store_type} bossbar {bossbar_id} {sub_cmd}"

    def build_BossbarAddNode(self, node):
        """
        Node Attributes:
            bossbar_id (NamespaceIdNode)
            json (JsonObjectNode)
        """
        bossbar_id = self.build(node.bossbar_id)
        json = self.build(node.json)
        return f"bossbar add {bossbar_id} {json}"

    def build_BossbarRemoveNode(self, node):
        """
        Node Attributes:
            bossbar_id (NamespaceIdNode)
        """
        bossbar_id = self.build(node.bossbar_id)
        return f"bossbar remove {bossbar_id}"

    def build_BossbarGetNode(self, node):
        """
        Node Attributes:
            bossbar_id (NamespaceIdNode)
            sub_cmd (Token)
        """
        bossbar_id = self.build(node.bossbar_id)
        sub_cmd = self.build(node.sub_cmd)
        return f"bossbar get {bossbar_id} {sub_cmd}"

    def build_BossbarSetNode(self, node):
        """
        Node Attributes:
            bossbar_id (NamespaceIdNode)
            arg (Token)
            arg_value (Token, JsonObjectNode)
        """
        bossbar_id = self.build(node.bossbar_id)
        arg = self.build(node.arg)
        arg_value = self.build(node.arg_value)
        return f"bossbar set {bossbar_id} {arg} {arg_value}"

    def build_DataGetNode(self, node):
        """
        Node Attributes:
            entity_vec3 (SelectorNode, Vec3Node)
            data_path (DataPathNode or None)
            scale (Token or None)
        """
        data_select_type = "entity" if isinstance(node.entity_vec3, SelectorNode) else "block"
        entity_vec3 = self.build(node.entity_vec3)

        if node.data_path is None:
            return f"data get {data_select_type} {entity_vec3}"
        data_path = self.build(node.data_path)

        if node.scale is None:
            return f"data get {data_select_type} {entity_vec3} {data_path}"

        scale = self.build(node.scale)
        return f"data get {data_select_type} {entity_vec3} {data_path} {scale}"

    def build_DataMergeNode(self, node):
        """
        Node Attributes:
            entity_vec3 (SelectorNode, Vec3Node)
            nbt (NbtObjectNode)
        """
        data_select_type = "entity" if isinstance(node.entity_vec3, SelectorNode) else "block"
        entity_vec3 = self.build(node.entity_vec3)
        nbt = self.build(node.nbt)
        return f"data merge {data_select_type} {entity_vec3} {nbt}"

    def build_DataRemoveNode(self, node):
        """
        Node Attributes:
            entity_vec3 (SelectorNode, Vec3Node)
            data_path (DataPathNode)
        """
        data_select_type = "entity" if isinstance(node.entity_vec3, SelectorNode) else "block"
        entity_vec3 = self.build(node.entity_vec3)
        data_path = self.build(node.data_path)
        return f"data remove {data_select_type} {entity_vec3} {data_path}"

    def build_EffectClearNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            effect_id (NamespaceIdNode or None)
        """
        selector = self.build(node.selector)
        if node.effect_id is None:
            return f"effect clear {selector}"

        effect_id = self.build(node.effect_id)
        return f"effect clear {selector} {effect_id}"

    def build_EffectGiveNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            effect_id (NamespaceIdNode)
            duration (Token or None)
            level (Token or None)
            hide_particles (bool)
        """
        selector = self.build(node.selector)
        effect_id = self.build(node.effect_id)
        duration = "2" if node.duration is None else self.build(node.duration)
        level = "0" if node.level is None else self.build(node.level)
        hide_particles = "true" if node.hide_particles else "false"
        return f"effect give {selector} {effect_id} {duration} {level} {hide_particles}"

    def build_DataPathNode(self, node):
        """
        Node Attributes:
            path_tokens (list of Token objects)
        """
        return self.iter_build(node.path_tokens, "")

    def build_TagAddNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            tag (Token)
            nbt (NbtObjectNode or None)
        """
        selector = self.build(node.selector)
        tag = self.build(node.tag, prefix=True)
        assert node.nbt is None
        return f"tag {selector} add {tag}"

    def build_TagRemoveNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            tag (Token)
            nbt (NbtObjectNode or None)
        """
        selector = self.build(node.selector)
        tag = self.build(node.tag, prefix=True)
        assert node.nbt is None
        return f"tag {selector} remove {tag}"

    def build_TeamAddNode(self, node):
        """
        Args:
            node (TeamAddNode)
            display_name (list of Token objects)
        """
        team_name = self.build(node.team_name, prefix=True)
        if not node.display_name:
            return f"team add {team_name}"

        display_name = self.iter_build(node.display_name, " ")
        return f"team add {team_name} {display_name}"

    def build_TeamJoinNode(self, node):
        """
        Args:
            node (TeamJoinNode)
        """
        team_name = self.build(node.team_name, prefix=True)
        target = self.build(node.target)
        return f"team join {team_name} {target}"

    def build_TeamLeaveNode(self, node):
        """
        Args:
            node (TeamLeaveNode)
        """
        target = self.build(node.target)
        return f"team leave {target}"

    def build_TeamEmptyNode(self, node):
        """
        Args:
            node (TeamEmptyNode)
        """
        team_name = self.build(node.team_name, prefix=True)
        return f"team empty {team_name}"

    def build_TeamOptionNode(self, node):
        """
        Args:
            node (TeamOptionNode)
        """
        team_name = self.build(node.team_name, prefix=True)
        option = self.build(node.option)
        value = self.build(node.value)
        return f"team option {team_name} {option} {value}"

    def build_TeamRemoveNode(self, node):
        """
        Args:
            node (TeamRemoveNode)
        """
        team_name = self.build(node.team_name, prefix=True)
        return f"team remove {team_name}"

    def build_XpMathNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            operator (Token)
            value (Token)
            sub_cmd (Token or None)
        """
        selector = self.build(node.selector)
        operator = self.build(node.operator)
        value = self.build(node.value)
        sub_cmd = "points" if node.sub_cmd is None else self.build(node.sub_cmd)

        if operator == "=":
            return f"xp set {selector} {value} {sub_cmd}"
        if operator == "+":
            return f"xp add {selector} {value} {sub_cmd}"
        if operator == "-":
            return f"xp add {selector} -{value} {sub_cmd}"

        raise SyntaxError("Unknown default case")

    def build_XpGetNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            sub_cmd (Token)
        """
        selector = self.build(node.selector)
        sub_cmd = self.build(node.sub_cmd)

        return f"xp get {selector} {sub_cmd}"

    def build_ItemGiveNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            item (ItemNode)
            count (Token or None)
        """
        selector = self.build(node.selector)
        item = self.build(node.item)
        count = "1" if node.count is None else self.build(node.count)
        return f"give {selector} {item} {count}"

    def build_ItemClearNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            item (ItemNode or Token)
            count (Token or None)
        """
        selector = self.build(node.selector)
        if isinstance(node.item, Token):
            return f"clear {selector}"

        item = self.build(node.item)
        count = "-1" if node.count is None else self.build(node.count)
        return f"clear {selector} {item} {count}"

    def build_ItemReplaceEntityNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            slot (Token)
            item (ItemNode)
            count (Token or None)
        """
        selector = self.build(node.selector)
        slot = self.build(node.slot)
        item = self.build(node.item)
        count = "1" if node.count is None else self.build(node.count)
        return f"replaceitem entity {selector} {slot} {item} {count}"

    def build_ItemReplaceBlockNode(self, node):
        """
        Node Attributes:
            vec3 (Vec3Node)
            slot (Token)
            item (ItemNode)
            count (Token or None)
        """
        vec3 = self.build(node.vec3)
        slot = self.build(node.slot)
        item = self.build(node.item)
        count = "1" if node.count is None else self.build(node.count)
        return f"replaceitem block {vec3} {slot} {item} {count}"

    def build_ItemNode(self, node):
        """
        Node Attributes:
            item_id (Token)
            nbt (NbtObjectNode or None)
        """
        item_id = self.build(node.item_id)
        nbt = "" if node.nbt is None else self.build(node.nbt)
        return f"minecraft:{item_id}{nbt}"


