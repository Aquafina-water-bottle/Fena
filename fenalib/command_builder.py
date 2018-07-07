""" Contains node visitors for the AST of a command to build itself """

import logging

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

    import fenalib.logging_setup as logging_setup
    logging_setup.setup_logging()

from fenalib.assert_utils import assert_type, assert_list_types
from fenalib.lexical_token import Token
from fenalib.config_data import ConfigData
from fenalib.in_file_config import InFileConfig, get_mcfunc_directories
from fenalib.node_visitors import NodeBuilder
from fenalib.nodes import IntRangeNode, JsonObjectNode, JsonMapNode, SelectorNode, SelectorScoreArgNode, SelectorDefaultArgNode, NbtMapNode, NbtArrayNode
from fenalib.str_utils import encode_str, decode_str
from fenalib.lexer import Lexer
from fenalib.parser import Parser

# pylint: disable=too-many-public-methods
class CommandBuilder_1_12(NodeBuilder):
    """
    Attributes:
        cmd_root (Node): The parent node of the AST representing a command
        mcfunction_dir (str): The full directory of mcfunction file used for smart function shortcuts
    """

    config_data = ConfigData()
    in_file_config = InFileConfig()

    def __init__(self, cmd_root, mcfunction_path):
        # assert_type(cmd_root, CmdNode, Token)
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
        execute = self.build("execute", cmd_name=True)
        if node.coords is None:
            coords = "~ ~ ~"
        else:
            coords = self.build(node.coords)
        selector = self.build(node.selector)

        # no detect area
        if not node.sub_if:
            return f"{execute} {selector} {coords}"

        # can have one or more detect areas
        result = []
        for index, sub_if in enumerate(node.sub_if):
            sub_if = self.build(sub_if)
            if index == 0:
                result.append(f"{execute} {selector} {coords} {sub_if}")
            else:
                result.append(f"{execute} @s {coords} {sub_if}")
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
        data_cmd_name = self.build(data_select_type, cmd_name=True)
        entity_vec3 = self.build(node.entity_vec3)
        nbt = self.build(node.nbt)
        return f"{data_cmd_name} {entity_vec3} {nbt}"

    def build_ScoreboardCmdMathNode(self, node):
        """
        Node Attributes:
            target (SelectorNode or Token)
            objective (Token)
            operator (Token)
            target_get (SelectorNode or Token)
            objective_get (Token or None)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        target = self.build(node.target)
        objective = self.build(node.objective, prefix=True)
        operator = self.build(node.operator)
        target_get = self.build(node.target_get)
        objective_get = objective if node.objective_get is None else self.build(node.objective_get, prefix=True)
        return f"{scoreboard} players operation {target} {objective} {operator} {target_get} {objective_get}"

    def build_ScoreboardCmdMathValueNode(self, node):
        """
        Node Attributes:
            target (SelectorNode or Token)
            objective (Token)
            operator (Token)
            value (Token)
            nbt (NbtObjectNode)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
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
                return f"{scoreboard} players {operation} {target} {objective} {value} {nbt}"
            return f"{scoreboard} players {operation} {target} {objective} {value}"

        # otherwise, scoreboard players operation
        if node.nbt is not None:
            raise SyntaxError(f"NBT arguments are not allowed with 'scoreboard players operation' {node.nbt}")

        constobj = self.in_file_config.constobj

        # <= sets the target to the score if and only if the target has a larger score compared to the value
        # therefore making the target score less than or equal to the value
        # >= sets the target to the score if and only if the target has a smaller score compared to the value
        # therefore making the target score greater than or equal to the value

        if operator in ("*=", "/=", "%=", "<", ">"):
            return f"{scoreboard} players operation {target} {objective} {operator} {value} {constobj}"

        if operator == "><":
            # no reason to swap with a constant value
            raise SyntaxError(f"Cannot swap with a constant value with operator {node.operator}")

        raise SyntaxError("Unknown default case")

    def build_ScoreboardCmdSpecialNode(self, node):
        """
        Args:
            node (ScoreboardCmdSpecialNode)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        sub_cmd = self.build(node.sub_cmd)
        target = self.build(node.target)
        objective = self.build(node.objective, prefix=True)
        return f"{scoreboard} players {sub_cmd} {target} {objective}"

    def build_EffectClearNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            effect_id (Token or None)
        """
        effect = self.build("effect", cmd_name=True)
        selector = self.build(node.selector)
        if node.effect_id is None:
            return f"{effect} {selector} clear"

        effect_id = self.build(node.effect_id)
        return f"{effect} {selector} minecraft:{effect_id} 0 0 true"

    def build_EffectGiveNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            effect_id (Token)
            duration (Token or None)
            level (Token or None)
            hide_particles (bool)
        """
        effect = self.build("effect", cmd_name=True)
        selector = self.build(node.selector)
        effect_id = self.build(node.effect_id)
        duration = "2" if node.duration is None else self.build(node.duration)
        level = "0" if node.level is None else self.build(node.level)
        hide_particles = "true" if node.hide_particles else "false"
        return f"{effect} {selector} minecraft:{effect_id} {duration} {level} {hide_particles}"

    def build_FunctionCmdNode(self, node):
        """
        Node Attributes:
            function_id (NamespaceIdNode)
            sub_arg (Token or None)
            selector (SelectorNode or None)
        """
        function = self.build("function", cmd_name=True)
        if node.function_id.namespace is not None:
            # if there is a namespace, it is assumed that the path is correct
            function_name = self.build(node.function_id)

        else:
            function_shortcut = self.build(node.function_id.id_value)
            if function_shortcut in self.in_file_config.function_conflicts:
                # smart assigning using self.mcfunction_dir
                # assumes 'functions' is a folder that exists

                # makes the following function shortcuts based off of the mcfunction directories
                # pops the last one because that's the mcfunction name
                mcfunc_dirs = get_mcfunc_directories(self.mcfunction_path)
                mcfunc_dirs.pop()

                while mcfunc_dirs:
                    insert_dir = mcfunc_dirs.pop()
                    # if there are no more directories, this is the last one and must be added with ":" instead of "/"
                    if mcfunc_dirs:
                        function_shortcut = f"{insert_dir}/{function_shortcut}"
                    else:
                        function_shortcut = f"{insert_dir}:{function_shortcut}"

                    if function_shortcut in self.in_file_config.function_conflicts or function_shortcut not in self.in_file_config.functions:
                        continue

                    # otherwise, returns the function shortcut
                    break

                else:
                    # completely invalid, apparently there are two of the exact same shortcut names
                    raise SyntaxError(f"Invalid function shortcut for node {node} (duplicate)")

            function_name = self.in_file_config.functions[function_shortcut]

        if node.sub_arg is None:
            return f"{function} {function_name}"
        assert node.sub_arg is not None and node.selector is not None
        sub_arg = self.build(node.sub_arg, replacements={"ifnot": "unless"})
        selector = self.build(node.selector)
        return f"{function} {function_name} {sub_arg} {selector}"

    def build_SimpleCmdNode(self, node):
        """
        Args:
            node (SimpleCmdNode)
        """
        cmd_name = self.build(node.tokens[0], cmd_name=True)
        cmd_args = self.iter_build(node.tokens[1:], ' ')
        if cmd_args:
            return f"{cmd_name} {cmd_args}"
        return cmd_name

    def build_ItemGiveNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            item (ItemNode)
            count (Token or None)
        """
        give = self.build("give", cmd_name=True)
        selector = self.build(node.selector)
        item_id = self.build(node.item.item_id)
        count = "1" if node.count is None else self.build(node.count)
        damage = "0" if node.item.damage is None else self.build(node.item.damage)

        if node.item.nbt is not None:
            nbt = self.build(node.item.nbt)
            return f"{give} {selector} minecraft:{item_id} {count} {damage} {nbt}"

        return f"{give} {selector} minecraft:{item_id} {count} {damage}"

    def build_ItemClearNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            item (ItemNode)
            count (Token or None)
        """
        clear = self.build("clear", cmd_name=True)
        selector = self.build(node.selector)
        if isinstance(node.item, Token):
            return f"{clear} {selector}"

        item_id = self.build(node.item.item_id)
        count = "-1" if node.count is None else self.build(node.count)
        damage = "-1" if node.item.damage is None else self.build(node.item.damage)

        if node.item.nbt is not None:
            nbt = self.build(node.item.nbt)
            return f"{clear} {selector} minecraft:{item_id} {damage} {count} {nbt}"

        return f"{clear} {selector} minecraft:{item_id} {damage} {count}"

    def build_ItemReplaceEntityNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            slot (Token)
            item (ItemNode)
            count (Token or None)
        """
        replaceitem = self.build("replaceitem", cmd_name=True)
        selector = self.build(node.selector)
        slot = self.build(node.slot)
        item_id = self.build(node.item.item_id)
        count = "1" if node.count is None else self.build(node.count)
        damage = "0" if node.item.damage is None else self.build(node.item.damage)

        if node.item.nbt is not None:
            nbt = self.build(node.item.nbt)
            return f"{replaceitem} entity {selector} slot.{slot} minecraft:{item_id} {count} {damage} {nbt}"
        return f"{replaceitem} entity {selector} slot.{slot} minecraft:{item_id} {count} {damage}"

    def build_ItemReplaceBlockNode(self, node):
        """
        Node Attributes:
            vec3 (Vec3Node)
            slot (Token)
            item (ItemNode)
            count (Token or None)
        """
        replaceitem = self.build("replaceitem", cmd_name=True)
        vec3 = self.build(node.vec3)
        slot = self.build(node.slot)
        item_id = self.build(node.item.item_id)
        count = "1" if node.count is None else self.build(node.count)
        damage = "0" if node.item.damage is None else self.build(node.item.damage)

        if node.item.nbt is not None:
            nbt = self.build(node.item.nbt)
            return f"{replaceitem} block {vec3} slot.{slot} minecraft:{item_id} {count} {damage} {nbt}"
        return f"{replaceitem} block {vec3} slot.{slot} minecraft:{item_id} {count} {damage}"

    def build_ObjectiveAddNode(self, node):
        """
        Node Attributes:
            objective (Token)
            criteria (Token)
            display_name (List[Token])
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        objective = self.build(node.objective, prefix=True)
        criteria = self.build(node.criteria)
        display_name = self.iter_build(node.display_name, " ")
        # strips in case the display name is nothing
        return f"{scoreboard} objectives add {objective} {criteria} {display_name}".strip()

    def build_ObjectiveRemoveNode(self, node):
        """
        Node Attributes:
            objective (Token)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        objective = self.build(node.objective, prefix=True)
        return f"{scoreboard} objectives remove {objective}"

    def build_ObjectiveSetdisplayNode(self, node):
        """
        Node Attributes:
            objective (Token)
            slot (Token)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        slot = self.build(node.slot)
        if node.objective is None:
            return f"{scoreboard} objectives setdisplay {slot}"
        objective = self.build(node.objective, prefix=True)
        return f"{scoreboard} objectives setdisplay {slot} {objective}"

    def build_TagAddNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            tag (Token)
            nbt (NbtObjectNode or None)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        selector = self.build(node.selector)
        tag = self.build(node.tag, prefix=True)
        if node.nbt is None:
            return f"{scoreboard} players tag {selector} add {tag}"

        nbt = self.build(node.nbt)
        return f"{scoreboard} players tag {selector} add {tag} {nbt}"

    def build_TagRemoveNode(self, node):
        """
        Node Attributes:
            selector (SelectorNode)
            tag (Token)
            nbt (NbtObjectNode or None)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        selector = self.build(node.selector)
        tag = self.build(node.tag, prefix=True)
        if node.nbt is None:
            return f"{scoreboard} players tag {selector} remove {tag}"

        nbt = self.build(node.nbt)
        return f"{scoreboard} players tag {selector} remove {tag} {nbt}"


    def build_TeamAddNode(self, node):
        """
        Args:
            node (TeamAddNode)
            display_name (list of Token objects)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        team_name = self.build(node.team_name, prefix=True)
        if not node.display_name:
            return f"{scoreboard} teams add {team_name}"

        display_name = self.iter_build(node.display_name, " ")
        return f"{scoreboard} teams add {team_name} {display_name}"

    def build_TeamJoinNode(self, node):
        """
        Args:
            node (TeamJoinNode)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        team_name = self.build(node.team_name, prefix=True)
        target = self.build(node.target)
        return f"{scoreboard} teams join {team_name} {target}"

    def build_TeamLeaveNode(self, node):
        """
        Args:
            node (TeamLeaveNode)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        target = self.build(node.target)
        return f"{scoreboard} teams leave {target}"

    def build_TeamEmptyNode(self, node):
        """
        Args:
            node (TeamEmptyNode)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        team_name = self.build(node.team_name, prefix=True)
        return f"{scoreboard} teams empty {team_name}"

    def build_TeamOptionNode(self, node):
        """
        Args:
            node (TeamOptionNode)
        """
        scoreboard = self.build("scoreboard", cmd_name=True)
        team_name = self.build(node.team_name, prefix=True)
        option = self.build(node.option)
        value = self.build(node.value)
        return f"{scoreboard} teams option {team_name} {option} {value}"

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
        xp = self.build("xp", cmd_name=True)
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

        return f"{xp} {negative}{value}{value_ending} {selector}"

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
            nbt_args (SelectorNbtArgsNode)
            advancement_args (SelectorAdvancementGroupArgNode)
        """
        # all_args = (node.default_args, node.score_args, node.tag_args, node.nbt_args, node.advancement_args)

        # note that map returns a generator
        # all_built_args = map(lambda x: ",".join(self.iter_build(x)), all_args)
        assert_list_types(node.default_args, SelectorDefaultArgNode, duplicate_key=lambda x: x.arg.value)
        default_args = self.iter_build(node.default_args, ",")
        score_args = self.build(node.score_args)
        tag_arg = "" if node.tag_arg is None else self.build(node.tag_arg)

        all_built_args = (default_args, score_args, tag_arg)
        # removes any 0 length strings
        return ",".join(x for x in all_built_args if x)

    def build_SelectorScoreArgsNode(self, node):
        """
        Node Attributes:
            score_args (list of SelectorScoreArgNode objects)
        """
        assert_list_types(node.score_args, SelectorScoreArgNode, duplicate_key=lambda x: x.objective.value)
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

        if arg == "team":
            arg_value = self.build(node.arg_value, prefix=True)
        else:
            arg_value = self.build(node.arg_value)
        return f"{arg}={arg_value}"

    def build_SelectorDefaultArgValueNode(self, node, prefix=False):
        """
        Node Attributes:
            arg_value (Token, NumberRangeNode, IntRangeNode)
            negated (bool)
        """
        negated = "!" if node.negated else ""
        arg_value = self.build(node.arg_value, prefix=prefix)
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
        assert_list_types(node.mappings, NbtMapNode, duplicate_key=lambda x: x.arg.value)
        return "{" + self.iter_build(node.mappings, ",") + "}"

    def build_NbtMapNode(self, node):
        """
        Node Attributes:
            arg (Token)
            value (Token)
        """
        arg = self.build(node.arg)

        if arg == "pages" and isinstance(node.value, NbtArrayNode):
            value = self.build(node.value, build_type="json_list")
        elif arg == "Tags" and isinstance(node.value, NbtArrayNode):
            value = self.build(node.value, build_type="tag_list")
        else:
            value = self.build(node.value)

        return f"{arg}:{value}"

    def build_NbtArrayNode(self, node, build_type=None):
        """
        Node Attributes:
            values (list of NbtNode objects)
            type_specifier (Token or None)
        """
        values = []
        for value in node.values:
            built_value = self.build(value)
            if build_type == "json_list":
                json = decode_str(built_value)
                lexer = Lexer(json)
                parser = Parser(lexer, method_name="get_curly_bracket_tag")
                ast = parser.parse(method_name="json")
                result = self.build_JsonObjectNode(ast)
                built_value = encode_str(result)

            elif build_type == "tag_list":
                tag = decode_str(self.build(value))
                lexer = Lexer(tag)
                parser = Parser(lexer, method_name="get_until_space")
                ast = parser.parse(method_name="advance")
                result = self.build_Token(ast, prefix=True)
                built_value = encode_str(result)

            values.append(built_value)

        values_str = ",".join(values)
        type_specifier = ("" if node.type_specifier is None else f"{self.build(node.type_specifier)};")
        return f"[{type_specifier}{values_str}]"

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
        assert_list_types(node.mappings, JsonMapNode, duplicate_key=lambda x: x.arg.value)

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
            # checks for action "run_command"
            if arg == '"clickEvent"':
                for mapping in node.value.mappings:
                    if mapping.arg.value == '"action"' and mapping.value.value == '"run_command"':
                        # can parse as a regular command
                        value = self.build(node.value, previous_arg='"run_command"')
                        break
                else:
                    # only runs if the for loop isn't broken
                    value = self.build(node.value)
            else:
                # passes the argument "score" in so the "name" arg under "score" can be converted into a proper selector
                current_arg = (arg if arg in ('"score"', '"clickEvent"') else None)
                value = self.build(node.value, previous_arg=current_arg)
        else:
            value = self.build(node.value)

        # if the argument is a selector, it builds a selector
        if previous_arg == '"run_command"' and arg == '"value"':
            # removes the /
            cmd = decode_str(value)[1:]
            lexer = Lexer(cmd)
            parser = Parser(lexer, method_name="get_command")
            ast = parser.parse(method_name="command")
            result = self.build_FenaCmdNode(ast)
            value = encode_str("/" + result)

        elif arg == '"selector"':
            selector = decode_str(value)
            lexer = Lexer(selector)
            parser = Parser(lexer, method_name="get_selector")
            ast = parser.parse(method_name="selector")
            result = self.build_SelectorNode(ast)
            value = encode_str(result)

        elif previous_arg == '"score"':
            # gets one token, and builds it with a possible prefix
            if arg == '"objective"':
                objective = decode_str(value)
                lexer = Lexer(objective)
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

    def build_NamespaceIdNode(self, node, prefix=False):
        """
        Attributes:
            id_value (Token)
            namespace (Token or None)
        """
        id_value = self.build(node.id_value, prefix=prefix)
        namespace = ("minecraft" if node.namespace is None else self.build(node.namespace))
        return f"{namespace}:{id_value}"

    def build_Token(self, token, prefix=False, replacements=None, cmd_name=False):
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
        assert_type(cmd_name, bool)
        assert not (cmd_name and prefix), "Both cmd_name and prefix cannot be True"

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

        if cmd_name and string in self.config_data.plugin_conflict_commands:
            return f"minecraft:{string}"

        if replacements is not None:
            return replacements.get(string, string)

        return string

    def build_str(self, node, cmd_name=False):
        """
        Literally just returns itself lmao
        """
        if cmd_name and node in self.config_data.plugin_conflict_commands:
            return f"minecraft:{node}"
        return node


