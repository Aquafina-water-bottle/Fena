if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fena.assert_utils import assert_type
from fena.parser import Parser
from fena.node_visitors import NodeVisitor

class Interpreter(NodeVisitor):
    """
    Args:
        parser (Parser)
        output_path (str)
    """
    def __init__(self, parser, output_path):
        assert_type(parser, Parser)
        assert_type(output_path, str)
        self.parser = parser
        self.output_path = output_path 

    def interpret(self):
        """
        Returns:
            list of McFunction objects
        """
        ast = self.parser.parse()
        return self.visit(ast)