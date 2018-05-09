from nodes import CmdNode, StmtNode

class TreePostfixTraversal:
    """
    Visitor from https://ruslanspivak.com/
    """

    def _visit(self, method_start, node):
        """
        Visits the specified node with the method starter

        Args:
            method_start (str): The starting part of the method name
                eg. method_start="visit", method_name=visit_<node>
            node (class type that inherits from Node)

        Returns:
            Whatever is gotten with the visitor method
        """
        assert isinstance(method_start, str)
        method_name = '{}_{}'.format(method_start, type(node).__name__)
        visitor_method = getattr(self, method_name)
        return visitor_method(node)

class NodeVisitor(TreePostfixTraversal):
    """
    Uses the visit method to visit any statment node
    """

    def visit(self, node):
        """
        Visits the specified node

        Returns:
            Whatever is gotten with the visitor method
        """
        assert isinstance(node, StmtNode)
        return self._visit("visit", node)

class NodeBuilder(TreePostfixTraversal):
    """
    Uses the build method to traverse the tree to build fena commands
    """

    def build(self, node):
        """
        Builds the specified node

        Args:
            node (class type that inherits from Node)

        Returns:
            Whatever is gotten with the build method
        """
        assert isinstance(node, CmdNode)
        return self._visit("build", node)
