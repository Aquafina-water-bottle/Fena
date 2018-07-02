if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fenalib.assert_utils import assert_type
from fenalib.lexical_token import Token
from fenalib.nodes import CmdNode, StmtNode, ProgramNode

class TreePostfixTraversal:
    """
    Visitor from https://ruslanspivak.com/
    """


    def _visit(self, method_start, node, **kwargs):
        """
        Visits the specified node with the method starter

        Args:
            method_start (str): The starting part of the method name
                eg. method_start="visit", method_name=visit_<node>
            node (class type that inherits from Node)

        Returns:
            Whatever is gotten with the visitor method
        """
        assert_type(method_start, str)
        class_name = type(node).__name__
        method_name = f"{method_start}_{class_name}"
        visitor_method = getattr(self, method_name, "invalid")

        if visitor_method == "invalid":
            raise NotImplementedError(f"Invalid method: {method_name}")

        return visitor_method(node, **kwargs)

class NodeVisitor(TreePostfixTraversal):
    """
    Uses the visit method to visit any statment node
    """

    def visit(self, node, **kwargs):
        """
        Visits the specified node

        Returns:
            Whatever is gotten with the visitor method
        """
        # assert_type(node, StmtNode, Token, ProgramNode)
        return self._visit("visit", node, **kwargs)

class NodeBuilder(TreePostfixTraversal):
    """
    Uses the build method to traverse the tree to build fena commands
    """

    def build(self, node, **kwargs):
        """
        Builds the specified node

        Args:
            node (class type that inherits from Node)

        Returns:
            str: Whatever is gotten with the build method
        """
        # assert_type(node, CmdNode, Token, str)
        return self._visit("build", node, **kwargs)

    def iter_build(self, nodes, join_value=None):
        """
        Args:
            nodes (iterable object)
            join_value (str or None)

        Returns:
            generator (if join_value is None): generator to map all nodes to the build method
            str (if join_value is str): Full string of built objects from its nodes joined by the join_value
        """
        assert_type(join_value, str, optional=True)

        build_generator = map(self.build, nodes)
        if join_value is None:
            return build_generator

        return join_value.join(build_generator)

