from abc import ABC

class NodeVisitor:
    """
    Taken pretty much straight from https://ruslanspivak.com/
    """

    def visit(self, node):
        """
        Visits the specific node specified

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

class ProgramNode(Node):
    """
    Holds all statements

    Attributes:
        statement_nodes (list of McFunctionNodes, FolderNodes, PrefixNodes, ConstObjNodes)
    """
    def __init__(self, statement_nodes):
        assert isinstance(statement_nodes, list)
        self.statement_nodes = statement_nodes

class McFunctionNode(Node):
    """
    Holds a single mcfunction with its full path and all defined commands

    Attributes:
        full_path (str)
        command_nodes (list of CommandNode objects)
    """
    def __init__(self, full_path, command_nodes):
        assert isinstance(full_path, str)
        assert isinstance(command_nodes, list)
        self.full_path = full_path
        self.command_nodes = command_nodes

class FolderNode(Node):
    """
    Holds all statements found inside a folder node

    Attributes:
        folder (str)
        statement_nodes (list of McFunctionNodes, FolderNodes, PrefixNodes, ConstObjNodes)
    """
    def __init__(self, folder, statement_nodes):
        assert isinstance(folder, str)
        assert isinstance(statement_nodes, list)
        self.folder = folder
        self.statement_nodes = statement_nodes

class PrefixNode(Node):
    """
    Attributes:
        prefix (str)
    """
    def __init__(self, prefix):
        assert isinstance(prefix, str)
        self.prefix = prefix

class ConstObjNode(Node):
    """
    Attributes:
        constobj (str)
    """
    def __init__(self, constobj):
        assert isinstance(constobj, str)
        self.constobj = constobj

class CommandNode(Node):
    """
    Holds all command segments for a command node

    Args:
        command_segment_nodes (list of specialized CmdNode objects)
    
    Attributes:
        execute_node (ExecuteCmdNode)
        scoreboard_node (ScoreboardCmdNode) 
        function_node (FunctionCmdNode)
        simple_node (SimpleCmdNode)
    """
    def __init__(self, command_segment_nodes):
        pass

