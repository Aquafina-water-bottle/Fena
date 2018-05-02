from abc import ABC

class NodeVisitor:
    """
    Taken pretty much straight from https://ruslanspivak.com/
    """

    def visit(self, node):
        """
        Visits the specific node type

        Args:
            node (class type that inherits from Node)

        Returns:
            pass
        """
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name)
        return visitor(node)

class Node(ABC):
    pass

class Program(Node):
    pass