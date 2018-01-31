class Node(object):
    pass

# all below are representing nodes within an abstract syntax tree
class BinOp(Node):
    """
    binary operator node
    
    stores left expr node, right expr node, and operator token
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
        
    def __str__(self):
        return str(self.left) + " " + str(self.op.value) + " " + str(self.right)
    
    __repr__ = __str__


class Num(Node):
    """
    number node
    
    stores integer or float value
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.token.value)
    
    __repr__ = __str__


class UnaryOp(Node):
    """
    unary operator node
    
    stores operator token (- or +) and expr node
    """
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __str__(self):
        return str(self.op) + str(self.expr)
    
    __repr__ = __str__


class Compound(Node):
    """
    represents a list of statements
    
    contains a list of statement nodes
    """
    def __init__(self):
        self.children = []

    def __str__(self):
        returnStr = ""
        for child in self.children:
            returnStr += str(child) + "; "
        return returnStr
    
    __repr__ = __str__


class Assign(Node):
    """
    assignment statement
    
    stores a left ? node, right ? node and assignment operator token
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return str(self.left.value) + " " + str(self.op.value) + " " + str(self.right)
    
    __repr__ = __str__


class Var(Node):
    """
    variable node
    
    stores token as identifier? node, and value as ? node
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.token.value)
    
    __repr__ = __str__


class NoOp(Node):
    """
    represents an empty expr (eg. newline)
    """
    
    def __str__(self):
        return "NoOp"


class Program(Node):
    """
    the main container of all nodes, as it represents the PROGRAM block
    """
    def __init__(self, name, block):
        self.name = name
        self.block = block

    def __str__(self):
        return str(self.name) + " " + str(self.block)
    
    __repr__ = __str__


class Block(Node):
    def __init__(self, declarations, compound_stmt):
        self.declarations = declarations
        self.compound_stmt = compound_stmt

    def __str__(self):
        returnStr = "{"
        for declaration in self.declarations:
            returnStr += str(declaration) + "; "
        return returnStr + str(self.compound_stmt) + "}"
    
    __repr__ = __str__


class VarDecl(Node):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

    def __str__(self):
        return str(self.var_node) + "=(" + str(self.type_node.value) + ")"
    
    __repr__ = __str__


class Type(Node):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.token)
    
    __repr__ = __str__


class Param(Node):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

    def __str__(self):
        return str(self.var_node) + " " + str(self.type_node)
    
    __repr__ = __str__


class ProcedureDecl(Node):
    def __init__(self, proc_name, params, block_node):
        self.proc_name = proc_name
        self.params = params  # a list of Param nodes
        self.block_node = block_node

    def __str__(self):
        paramStr = ""
        separator = ""
        for param in self.params:
            paramStr += separator + str(param.type_node.value) + " " + str(param.var_node)
            separator = ", "
        return str(self.proc_name) + "(" + paramStr + "): " + str(self.block_node)
    
    __repr__ = __str__


