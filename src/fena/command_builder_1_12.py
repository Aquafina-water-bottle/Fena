"""
The command builder for specifically building 1.12 commands
"""

import logging
from config_data import ConfigData
from in_file_config import InFileConfig
from node_visitors import NodeBuilder
from nodes import FenaCmdNode

class CommandBuilder_1_12(NodeBuilder):
    """
    Attributes:
        cmd_root (FenaCmdNode): The parent node of the AST representing a command
    """

    config_data = ConfigData()
    in_file_config = InFileConfig()

    def __init__(self, cmd_root):
        assert isinstance(cmd_root, FenaCmdNode)
        self.cmd_root = cmd_root

    def interpret(self):
        """
        Creates the full built command

        Returns:
            str: The full command as a string
        """
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
        sub_cmd = self.build(node.sub_cmd, replacements={"<-": "get"})
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
        Args:
            node (SelectorNode)
        """
        selector_var = self.build(node.selector_var)
        selector_args = ",".join(self.iter_build(node.selector_args))
        return f"{selector_var}[{selector_args}]"

    def build_SelectorArgNode(self, node):
        pass

    def build_Token(self, token, prefix=False, replacements=None):
        """
        Returns its value with a prefix if avaliable

        Args:
            prefix (bool): Whether the value might have a prefix placeholder or not
            replacements (dict): Any possible replacements to the token valuestring

        Returns:
            str: The new string that is guaranteed to have a prefix
        """
        assert isinstance(prefix, bool)
        assert replacements is None or isinstance(replacements, dict)

        string = str(token.value)
        
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

if __name__ == "__main__":
    class A:
        def __init__(self, test):
            self.test = test

        def func1(self, arg):
            return int(arg) + 5
        
        def func2(self):
            return list(map(self.func1, self.test))

    a = A([1, 2, "3", 4, "5"])
    print(a.func2())