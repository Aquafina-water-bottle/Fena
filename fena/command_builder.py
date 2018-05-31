"""
Contains node visitors for the AST of a command to build itself
"""

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
        # print(all_args)

        # requires the tag args to be less than one for length
        if len(node.tag_args) > 1:
            raise SyntaxError("Cannot have more than one tag inside a selector for 1.12")

        # note that map returns a generator
        all_built_args = map(lambda x: ",".join(self.iter_build(x)), all_args)

        # result = ",".join(x for x in all_built_args if x)
        # print(result)
        # return result

        # removes any 0 length strings
        return ",".join(x for x in all_built_args if x)

    def build_SelectorScoreArgNode(self, node):
        """
        Node Attributes:
            objective (Token)
            value (IntRangeNode, Token)
        """
        objective = self.build(node.objective)
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

if __name__ == "__main__":
    logging_setup.format_file_name("test_lexer.txt")

    from fena.lexer import Lexer
    from fena.parser import Parser

    def test(string, lexer_method, parser_method, expected=None, expect_error=False, version="1.12", print_ast=False):
        if version == "1.12":
            CommandBuilder = CommandBuilder_1_12
        elif version == "1.13":
            CommandBuilder = CommandBuilder_1_13
        else:
            raise RuntimeError

        try:
            lexer = Lexer(string)
            parser = Parser(lexer, lexer_method)
            ast = parser.parse(method_name=parser_method)
            command_builder = CommandBuilder(ast)
            output = command_builder.interpret()

            if expected is None:
                expected = string

        except Exception as e:
            print(f"input={string!r}, output={e!r}")
            if not expect_error:
                raise RuntimeError
        else:
            print(f"input={string!r}, output={output!r}")
            if print_ast:
                print(ast)

            if expected != output:
                raise RuntimeError(f"""
                Input:    {string!r}
                Expected: {expected!r}
                Output:   {output!r}""")

    def test_selector(selector, expected=None, expect_error=False, print_ast=False):
        test(selector, "get_selector", "selector", expected, expect_error, print_ast=print_ast)

    def test_selectors():
        test_selector("@p")
        test_selector("@a[]")
        test_selector("@e[type=armor_stand]", "@e[type=minecraft:armor_stand]")
        test_selector("@e[type=minecraft:armor_stand]")
        test_selector("@e[type=armor_stand,c=1]", "@e[type=minecraft:armor_stand,c=1]")
        test_selector("@e[type=armor_stand,dist=1..2]", "@e[type=minecraft:armor_stand,rm=1,r=2]")
        test_selector("@a[x]", "@a[tag=x]")

        test_selector("@a[RRpl=3..4]", "@a[score_RRpl_min=3,score_RRpl=4]")
        test_selector("@a[RRpl=3..]", "@a[score_RRpl_min=3]")
        test_selector("@a[RRpl=..3]", "@a[score_RRpl=3]")
        test_selector("@a[RRpl=3]", "@a[score_RRpl_min=3,score_RRpl=3]")
        test_selector("@a[RRpl=*]", "@a[score_RRpl_min=-2147483648]")
        test_selector("@a[RRpl=(3..4)]", "@a[score_RRpl_min=3,score_RRpl=4]")
        test_selector("@a[RRpl=(3..)]", "@a[score_RRpl_min=3]")
        test_selector("@a[RRpl=(..3)]", "@a[score_RRpl=3]")
        test_selector("@a[RRpl=(3)]", "@a[score_RRpl_min=3,score_RRpl=3]")
        test_selector("@a[RRpl=(*)]", "@a[score_RRpl_min=-2147483648]")
        test_selector("@a[RRpl=((((3..))))]", "@a[score_RRpl_min=3]")

        test_selector("@a[distance=2..5]", "@a[rm=2,r=5]")
        test_selector("@a[distance=5]", "@a[rm=5,r=5]")
        test_selector("@a[distance=2..]", "@a[rm=2]")
        test_selector("@a[distance=..5]", "@a[r=5]")
        test_selector("@a[dist=2..5]", "@a[rm=2,r=5]")
        test_selector("@a[dist=5]", "@a[rm=5,r=5]")
        test_selector("@a[dist=2..]", "@a[rm=2]")
        test_selector("@a[dist=..5]", "@a[r=5]")
        test_selector("@a[dist=(2..5)]", "@a[rm=2,r=5]")
        test_selector("@a[dist=(5)]", "@a[rm=5,r=5]")
        test_selector("@a[dist=(2..)]", "@a[rm=2]")
        test_selector("@a[dist=(..5)]", "@a[r=5]")

        test_selector("@a[level=2..5]", "@a[lm=2,l=5]")
        test_selector("@a[level=5]", "@a[lm=5,l=5]")
        test_selector("@a[level=2..]", "@a[lm=2]")
        test_selector("@a[level=..5]", "@a[l=5]")
        test_selector("@a[lvl=2..5]", "@a[lm=2,l=5]")
        test_selector("@a[lvl=5]", "@a[lm=5,l=5]")
        test_selector("@a[lvl=2..]", "@a[lm=2]")
        test_selector("@a[lvl=..5]", "@a[l=5]")
        test_selector("@a[lvl=(2..5)]", "@a[lm=2,l=5]")
        test_selector("@a[lvl=(5)]", "@a[lm=5,l=5]")
        test_selector("@a[lvl=(2..)]", "@a[lm=2]")
        test_selector("@a[lvl=(..5)]", "@a[l=5]")

        test_selector("@a[x_rotation=2..5]", "@a[rxm=2,rx=5]")
        test_selector("@a[x_rotation=5]", "@a[rxm=5,rx=5]")
        test_selector("@a[x_rotation=2..]", "@a[rxm=2]")
        test_selector("@a[x_rotation=..5]", "@a[rx=5]")
        test_selector("@a[xrot=2..5]", "@a[rxm=2,rx=5]")
        test_selector("@a[xrot=5]", "@a[rxm=5,rx=5]")
        test_selector("@a[xrot=2..]", "@a[rxm=2]")
        test_selector("@a[xrot=..5]", "@a[rx=5]")
        test_selector("@a[xrot=(2..5)]", "@a[rxm=2,rx=5]")
        test_selector("@a[xrot=(5)]", "@a[rxm=5,rx=5]")
        test_selector("@a[xrot=(2..)]", "@a[rxm=2]")
        test_selector("@a[xrot=(..5)]", "@a[rx=5]")

        test_selector("@a[y_rotation=2..5]", "@a[rym=2,ry=5]")
        test_selector("@a[y_rotation=5]", "@a[rym=5,ry=5]")
        test_selector("@a[y_rotation=2..]", "@a[rym=2]")
        test_selector("@a[y_rotation=..5]", "@a[ry=5]")
        test_selector("@a[yrot=2..5]", "@a[rym=2,ry=5]")
        test_selector("@a[yrot=5]", "@a[rym=5,ry=5]")
        test_selector("@a[yrot=2..]", "@a[rym=2]")
        test_selector("@a[yrot=..5]", "@a[ry=5]")
        test_selector("@a[yrot=(2..5)]", "@a[rym=2,ry=5]")
        test_selector("@a[yrot=(5)]", "@a[rym=5,ry=5]")
        test_selector("@a[yrot=(2..)]", "@a[rym=2]")
        test_selector("@a[yrot=(..5)]", "@a[ry=5]")

        test_selector("@a[limit=5,gamemode=creative]", "@a[c=5,m=1]")

        test_selector("@a[hello]", "@a[tag=hello]")
        test_selector("@a[hello,objective=2..,x=5]", "@a[x=5,score_objective_min=2,tag=hello]")
        
        test_selector(
            "@a[x=-153,y=0,z=299,dx=158,dy=110,dz=168,m=2,RRar=3..5]",
            "@a[x=-153,y=0,z=299,dx=158,dy=110,dz=168,m=2,score_RRar_min=3,score_RRar=5]")

        test_selector(
            "@a[g.hello=5,x=-153,y=0,z=299,RRar=3..5]",
            "@a[x=-153,y=0,z=299,score_g.hello_min=5,score_g.hello=5,score_RRar_min=3,score_RRar=5]")

        test_selector("@3", expect_error=True)
        test_selector("@a[a,b,c]", expect_error=True)
        test_selector("@a[a,]", expect_error=True)

    test_selectors()

