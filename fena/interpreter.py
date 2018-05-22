from parse_tree import Parser
from node_visitors import NodeVisitor

class Interpreter(NodeVisitor):
    """
    Args:
        parser (Parser)
        output_path (str)
    """
    def __init__(self, parser, output_path):
        assert isinstance(parser, Parser)
        assert isinstance(output_path, str)
        self.parser = parser
        self.output_path = output_path 

    def interpret(self):
        """
        Returns:
            list of McFunction objects
        """
        ast = self.parser.parse()
        return self.visit(ast)