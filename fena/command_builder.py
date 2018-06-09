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
from fena.nodes import CmdNode, IntRangeNode, SelectorDefaultGroupArgValueNode, JsonObjectNode, JsonMapNode
from fena.str_utils import encode_str, decode_str
from fena.lexer import Lexer
from fena.parser import Parser

class CommandBuilder_1_12(NodeBuilder):
    """
    Attributes:
        cmd_root (Node): The parent node of the AST representing a command
    """

    config_data = ConfigData()
    in_file_config = InFileConfig()

    def __init__(self, cmd_root):
        assert_type(cmd_root, CmdNode)
        assert self.in_file_config.finalized
        self.cmd_root = cmd_root

    def interpret(self):
        """
        Creates the full built command

        Returns:
            str: The full command as a string
        """
        return self.build(self.cmd_root)

    def build_FenaCmdNode(self, node):
        return self.iter_build(self.cmd_root.cmd_segment_nodes, " ")

    def build_ExecuteCmdNode(self, node):
        """
        Args:
            node (ExecuteCmdNode)
        """
        return self.iter_build(node.sub_cmd_nodes, " ")

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
        objective_get = self.build(node.objective_get, prefix=True)
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
        if node.nbt is not None and self.config_data.version == "1.13":
            raise SyntaxError(f"NBT arguments are not allowed in 1.13: {node.nbt}")

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
            raise SyntaxError(f"Cannot swap with a constant value in {node.operator}")

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
        return self.iter_build(node.tokens, " ")

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
    def __init__(self, cmd_root):
        super().__init__(cmd_root)

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
        Attributes:
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

