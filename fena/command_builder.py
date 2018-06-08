""" Contains node visitors for the AST of a command to build itself """ 
import logging

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

    import fena.logging_setup as logging_setup

from fena.assert_utils import assert_type
from fena.lexical_token import Token
from fena.config_data import ConfigData
from fena.in_file_config import InFileConfig
from fena.node_visitors import NodeBuilder
from fena.nodes import CmdNode, IntRangeNode

class CommandBuilder_1_12(NodeBuilder):
    """
    Attributes:
        cmd_root (Node): The parent node of the AST representing a command
    """

    config_data = ConfigData()
    in_file_config = InFileConfig()

    def __init__(self, cmd_root):
        assert_type(cmd_root, CmdNode)
        assert CommandBuilder_1_12.in_file_config.finalized
        self.cmd_root = cmd_root

    def interpret(self):
        """
        Creates the full built command

        Returns:
            str: The full command as a string
        """
        return self.build(self.cmd_root)

    def build_FenaCmdNode(self, node):
        return " ".join(self.iter_build(self.cmd_root.cmd_segment_nodes))

    def build_ExecuteCmdNode(self, node):
        """
        Args:
            node (ExecuteCmdNode)
        """
        return " ".join(self.iter_build(node.sub_cmd_nodes))

    def build_ExecuteSubLegacyArg(self, node):
        """
        turns to <selector> <vec3> [detect vec3 block_type data_value]

        Args:
            node (ExecuteSubLegacyArg)
        """
        if node.coords is None:
            coords = "~ ~ ~"
        else:
            coords = self.build(node.coords)
        selector = self.build(node.selector)

        if node.sub_if is None:
            return f"execute {selector} {coords}"

        sub_if = self.build(node.sub_if)
        return f"execute {selector} {coords} {sub_if}"

    def build_ExecuteSubIfBlockArg(self, node):
        """
        Args:
            node (ExecuteSubIfBlockArg)
        """
        if node.coords is None:
            coords = "~ ~ ~"
        else:
            coords = self.build(node.coords)

        block = self.build(node.block)
        return f"detect {coords} {block}"

    def build_ScoreboardCmdMathNode(self, node):
        """
        Args:
            node (ScoreboardCmdMathNode)
        """
        begin_target = self.build(node.begin_target)
        begin_objective = self.build(node.begin_objective)
        operator = self.build(node.operator)
        end_target = self.build(node.end_target)
        end_objective = self.build(node.end_objective)
        return f"scoreboard players operation {begin_target} {begin_objective} {operator} {end_target} {end_objective}"

    def build_ScoreboardCmdMathValueNode(self, node):
        """
        Args:
            node (ScoreboardCmdMathValueNode)
        """
        target = self.build(node.target)
        objective = self.build(node.objective)
        operator = self.build(node.operator)
        value = self.build(node.value)
        constobj = self.in_file_config.constobj

        if operator == "=":
            return f"scoreboard players set {target} {objective} {value}"
        if operator == "+=":
            return f"scoreboard players add {target} {objective} {value}"
        if operator == "-=":
            return f"scoreboard players add {target} {objective} {value}"
        if operator in ("*=", "/=", "%="):
            return f"scoreboard players operation {target} {objective} {operator} {value} {constobj}"
        if operator == "<=":
            # sets the target to the score if and only if the target has a larger score compared to the value
            # therefore making the target score less than or equal to the value
            return f"scoreboard players operation {target} {objective} < {value} {constobj}"
        if operator == ">=":
            # sets the target to the score if and only if the target has a smaller score compared to the value
            # therefore making the target score greater than or equal to the value
            return f"scoreboard players operation {target} {objective} > {value} {constobj}"
        if operator in ("swap"):
            # no reason to swap with a constant value
            raise SyntaxError("Cannot swap with a constant value")

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
        return f"scoreboard players {sub_cmd} {target} {objective}"

    def build_FunctionCmdNode(self, node):
        """
        Args:
            node (FunctionCmdNode)
        """
        function = self.in_file_config.functions[node.function_name]
        return f"function {function}"

    def build_SimpleCmdNode(self, node):
        """
        Args:
            node (SimpleCmdNode)
        """
        return " ".join(self.iter_build(node.tokens))

    def build_TeamAddNode(self, node):
        """
        Args:
            node (TeamAddNode)
        """
        team_name = self.build(node.team_name, prefix=True)
        if node.display_name is None:
            return f"scoreboard teams add {team_name}"

        display_name = self.build(node.display_name)
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
        return f"scoreboard teams leave {team_name}"

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
        Node Attributes:
            default_args (list of SelectorDefaultArgNode objects)
            score_args (list of SelectorScoreArgNode objects)
            tag_args (list of SelectorTagArgNode objects)
            nbt_args (list of SelectorNbtArgNode objects)
            advancement_args (list of SelectorAdvancementArgNode objects)
        """
        all_args = (node.default_args, node.score_args, node.tag_args, node.nbt_args, node.advancement_args)

        # requires the tag args to be less than one for length
        if len(node.tag_args) > 1:
            raise SyntaxError("Cannot have more than one tag inside a selector for 1.12")

        # note that map returns a generator
        all_built_args = map(lambda x: ",".join(self.iter_build(x)), all_args)

        # removes any 0 length strings
        return ",".join(x for x in all_built_args if x)

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
            negated (bool)
        """
        raise SyntaxError("Cannot build a selector group value node in 1.12")

    def build_SelectorTagArgNode(self, node):
        """
        Node Attributes:
            tag (Token)
            negated (bool)
        """
        negated = "!" if node.negated else ""
        tag = self.build(node.tag)
        return f"tag={negated}{tag}"

    def build_SelectorNbtArgNode(self, node):
        """
        Node Attributes:
            nbt (NbtNode)
            negated (bool)
        """
        raise SyntaxError("Cannot build a selector nbt node in 1.12")

    def build_SelectorAdvancementArgNode(self, node):
        raise SyntaxError("Cannot build a selector nbt node in 1.12")

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

    def build_NamespaceIdNode(self, node):
        """
        Attributes:
            id_value (Token)
            namespace (Token or None)
        """
        id_value = self.build(node.id_value)
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
                # prefix=rr, string=__ti -> rr._ti
                # prefix=rr, string=_ti -> rr.ti
                return self.in_file_config.prefix + "." + string[1:]

            if "." not in string and self.config_data.ego:
                logging.warning("No prefix given to {!r}".format(token))

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
    def __init__(self, cmd_root):
        super().__init__(self, cmd_root)

    def build_SelectorArgsNode(self, node):
        """
        Node Attributes:
            default_args (list of SelectorDefaultArgNode objects)
            score_args (list of SelectorScoreArgNode objects)
            tag_args (list of SelectorTagArgNode objects)
            nbt_args (list of SelectorNbtArgNode objects)
            advancement_args (list of SelectorAdvancementArgNode objects)
        """
        # note that map returns a generator
        default_built = ",".join(self.iter_build(node.default_args))
        score_built = "scores={" + ",".join(self.iter_build(node.score_args)) + "}" if node.score_args else ""
        tag_built = ",".join(self.iter_build(node.tag_args))
        nbt_built = "nbt={" + "},nbt={".join(self.iter_build(node.nbt_args)) + "}" if node.nbt_args else ""
        advancement_built = "advancements={" + ",".join(self.iter_build(node.advancement_args)) + "}" if node.advancement_args else ""
        all_built_args = (default_built, score_built, tag_built, nbt_built, advancement_built)

        # removes any 0 length strings
        return ",".join(x for x in all_built_args if x)

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

        return f"{min_int}..{max_int}"

