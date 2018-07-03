import os
import logging

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

    import fenalib.logging_setup as logging_setup

from fenalib.assert_utils import assert_type
from fenalib.parser import Parser
from fenalib.token_classes import TypedToken
from fenalib.str_utils import encode_str, decode_str
from fenalib.node_visitors import NodeVisitor
from fenalib.config_data import ConfigData
from fenalib.in_file_config import InFileConfig
# from fenalib.command_builder import CommandBuilder_1_12, CommandBuilder_1_13
from fenalib.command_builder import CommandBuilder_1_12
from fenalib.mcfunction import McFunction


class Interpreter(NodeVisitor):
    """
    - Visits all statement nodes first to get information for the InFileConfig object
    - Builds all function nodes after

    Attributes:
        parser (Parser)
        output_path (str)
        mcfunctions (dict mapping a McFunction to a McFunctionNode): Relates each McFunctionNode to some McFunction to be built
        current_folders (list): List the current path as specified by the folders
        in_file_config (InFileConfig)
    """
    def __init__(self, parser, output_path):
        assert_type(parser, Parser)
        assert_type(output_path, str)
        self.parser = parser
        self.output_path = output_path
        self.mcfunctions = {}
        self.current_folders = []
        self.in_file_config = InFileConfig()

        # checks whether the output path has "functions" in it
        path_list = os.path.normpath(output_path).split(os.sep)
        if "functions" not in path_list:
            raise SyntaxError(f"Expected 'functions' directory to be in {self.output_path}")

    def interpret(self):
        """
        Returns:
            list of McFunction objects
        """
        ast = self.parser.parse()
        self.visit(ast)
        self.in_file_config.finalize()

        # if config_data.version == "1.12":
        #     CommandBuilder = CommandBuilder_1_12
        # elif config_data.version == "1.13":
        #     CommandBuilder = CommandBuilder_1_13
        # else:
        #     raise RuntimeError("wtf man")
        CommandBuilder = CommandBuilder_1_12

        for mcfunction, mcfunction_node in self.mcfunctions.items():
            for command_node in mcfunction_node.command_nodes:
                command_builder = CommandBuilder(command_node, mcfunction.full_path)
                built_command = command_builder.interpret()
                mcfunction.add_command(built_command)
            mcfunction.finalize()

        return list(self.mcfunctions.keys())

    def visit_ProgramNode(self, node):
        """
        Node Attributes:
            statement_nodes (list of nodes inherited from StmtNode)

        Returns:
            list of McFunction objects
        """
        for statement_node in node.statement_nodes:
            node = self.visit(statement_node)

    def visit_McFunctionNode(self, node):
        """
        Node Attributes:
            name (Token): The mcfunction name
            command_nodes (list of FenaCmdNode objects)
        """
        mfunc_name = self.visit(node.name)

        # direct path from the functions folder
        if ":" in mfunc_name:
            raise NotImplementedError(f"Cannot have ':' in an mcfunction name {node.name} since that specifies a full path")
        full_path = os.path.join(self.output_path, *self.current_folders, mfunc_name + ".mcfunction")
        mcfunction = McFunction(mfunc_name, full_path, node.debug)

        self.mcfunctions[mcfunction] = node
        self.in_file_config.add_function(mcfunction)

    def visit_FolderNode(self, node):
        """
        Node Attributes:
            folder (Token)
            statement_nodes (list of nodes inherited from StmtNode)
        """
        folder_value = self.visit(node.folder)

        # appends the folder string only for the visited nodes under the folder compound
        self.current_folders.append(folder_value)

        for statement_node in node.statement_nodes:
            node = self.visit(statement_node)

        self.current_folders.pop()

    def visit_VarSetNode(self, node):
        """
        Node Attributes:
            variable (Token)
            value (Token)
        """
        if node.variable.value == "prefix":
            self.in_file_config.prefix = self.visit(node.value)
        elif node.variable.value == "constobj":
            self.in_file_config.constobj = self.visit(node.value)
        else:
            raise SyntaxError(f"Expected one of 'prefix' or 'constobj' for node {node.variable}")

    def visit_FenaCmdNode(self, node):
        """
        Node Attributes:
            cmd_segment_nodes (list of MainCmdNode objects)
        """
        pass

    def visit_Token(self, token):
        """
        Simply gets the value, and decodes if it's a quoted string
        """
        if token.matches(TypedToken.LITERAL_STRING):
            return decode_str(token.value)
        return token.value

if __name__ == "__main__":
    """
    TODO:
        - make the function token only be either one literal string or one string
            - if it has a namespace, literal string
        - have the lexer/parser require ":" at the end of a folder and mfunc statement
    """

    from fenalib.lexer import Lexer
    from fenalib.parser import Parser
    from fenalib.writer import Writer

    # logging_setup.format_file_name("test_lexer.txt")
    # with open("test_lexer.txt") as file:
    #     text = file.read()

    logging_setup.format_file_name("test_lexer_1_13.txt")
    with open("test_lexer_1_13.txt") as file:
        text = file.read()

    ConfigData().ego = False
    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        # full_dir_path = os.path.realpath("functions/fena")
        full_dir_path = os.path.realpath("functions/fena/1_13")
        interpreter = Interpreter(parser, full_dir_path)
        mcfunctions = interpreter.interpret()
        writer = Writer(mcfunctions)
        writer.write()

    except Exception as e:
        logging.exception(e) # type: ignore
