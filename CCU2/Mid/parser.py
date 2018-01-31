r"""
// keywords
INT_TYPE ::= "int"
FLOAT_TYPE ::= "float"
STR_TYPE ::= "str"
BOOL_TYPE ::= "bool"
NULL_TYPE ::= "null"
VOID_TYPE ::= "void"

PASS ::= "pass'

// delimiters
DOT ::= "."
COMMA ::= ","
COLON ::= ":"
SEMICOLON ::= ";"
LPAREN ::= "("
RPAREN ::= ")"
NEWLINE ::= "\n"

// operators
PLUS ::= "+"
MINUS ::= "-"
MULTIPLY ::= "*"
DIVIDE ::= "/"
ASSIGN ::= "="

// other
COMMENT_START ::= "/*"
COMMENT_END ::= "*/"
LINE_COMMENT ::= "//"

// tl;dr RIO grammar doesn't really specify how to do indents like this, so rip
INDENT ::= "nah"
DEDENT ::= "fam"

INT_CONST ::= (\D)+
FLOAT_CONST ::= (\D)+ & "." & (\D)+
STR_CONST ::= "\"" && [\E, \N]* && "\""
IDENTIFIER ::= (\A | "_") & (\W | "_")* // identifier



program ::= stmtList
stmtList ::= statement+
statement ::= [functionDecl] | [assignmentStmt, varDeclStmt, PASS] && NEWLINE
functionDecl ::= returnType && LPAREN && parameters && RPAREN && COLON && suite
returnType ::= [INT_TYPE, FLOAT_TYPE, STR_TYPE, BOOL_TYPE, VOID_TYPE]
suite ::= NEWLINE && INDENT && stmtList && DEDENT
parameters ::= (j: (e: \S*)(","))(parameter)*
parameter ::= varDeclType && variable

assignmentStmt ::= variable && ASSIGN && expr
varDeclStmt ::= varDeclType && variable && ASSIGN && expr
varDeclType ::= [INT_TYPE, FLOAT_TYPE, STR_TYPE, BOOL_TYPE]
expr ::= (j: (e: \S*)[PLUS, MINUS])(term+)
term ::= (j: (e: \S*)[MULTIPLY, DIVIDE])(factor+)
factor ::= [([PLUS, MINUS]? factor), INT_CONST, FLOAT_CONST, LPAREN && expr && RPAREN, variable]
variable ::= ID
"""

import logging

from .constants import *
from .nodes import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.currentToken = self.lexer.getNextToken()

    def error(self):
        logging.error(self.lexer.getPosRepr() + "SYNTAX ERROR MOTHERFUCKERS")
        raise SyntaxError

    def eat(self, tokenType):
        """
        gets the next token assuming both type and representation is the same as the current token
        raises an error when the type and repr isn't equal to the current token

        compare the current token type with the passed token
        type and if they match then "eat" the current token
        and assign the next token to the self.currentToken,
        otherwise raise an exception.

        :param tokenType: type of the token (general)
        """
        if isinstance(tokenType, tuple) and (self.currentToken.type == tokenType[VALUE]):
            self.currentToken = self.lexer.getNextToken()
        elif self.currentToken.type == tokenType:
            self.currentToken = self.lexer.getNextToken()
        else:
            self.error()

    def program(self):
        """ program ::= stmtList """
        programName = self.lexer.fileName
        stmtList = self.stmtList()
        programNode = Program(programName, stmtList)
        return programNode

    def stmtList(self):
        """ stmtList ::= statement+ """

        # creates list of nodes
        results = [self.statement()]
        while self.currentToken.type == NEWLINE[VALUE]:
            self.eat(NEWLINE)
            results.append(self.statement())

    def statement(self):
        """ statement ::= [functionDecl] | [assignmentStmt, varDeclStmt, PASS] && NEWLINE """
        if self.currentToken.type == IDENTIFIER:
            node = self.assignmentStmt()
        elif self.currentToken.type == PASS[VALUE]:
            pass

    def functionDecl(self):
        """ functionDecl ::= returnType && LPAREN && parameters && RPAREN && COLON && suite """
        pass

    def returnType(self):
        """ returnType ::= [INT_TYPE, FLOAT_TYPE, STR_TYPE, BOOL_TYPE, VOID_TYPE] """
        pass

    def suite(self):
        """ suite ::= NEWLINE && INDENT && stmtList && DEDENT """
        pass

    def parameters(self):
        """ parameters ::= (j: (e: \S*)(","))(parameter)* """
        pass

    def parameter(self):
        """ parameter ::= varDeclType && variable """
        pass

    def assignmentStmt(self):
        """ assignmentStmt ::= variable && ASSIGN && expr """
        pass

    def varDeclStmt(self):
        """ varDeclStmt ::= varDeclType && variable && ASSIGN && expr """
        pass

    def varDeclType(self):
        """ varDeclType ::= [INT_TYPE, FLOAT_TYPE, STR_TYPE, BOOL_TYPE] """
        pass

    def expr(self):
        """ expr ::= (j: (e: \S*)[PLUS, MINUS])(term+) """
        pass

    def term(self):
        """ term ::= (j: (e: \S*)[MULTIPLY, DIVIDE])(factor+) """
        pass

    def factor(self):
        """ factor ::= [([PLUS, MINUS]? factor), INT_CONST, FLOAT_CONST, LPAREN && expr && RPAREN, variable] """
        pass

    def variable(self):
        """ variable ::= ID """
        pass

    def parse(self):
        pass

    # def block(self):
    #     """block : declarations compound_statement"""
    #     declaration_nodes = self.declarations()
    #     compound_statement_node = self.compound_statement()
    #     node = Block(declaration_nodes, compound_statement_node)
    #     return node
    #
    # def declarations(self):
    #     """declarations : (VAR (variable_declaration SEMI)+)*
    #                     | (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)*
    #                     | empty
    #     """
    #     declarations = []
    #
    #     while True:
    #         if self.currentToken.type == VAR:
    #             self.eat(VAR)
    #             while self.currentToken.type == ID:
    #                 var_decl = self.variable_declaration()
    #                 declarations.extend(var_decl)
    #                 self.eat(SEMI)
    #
    #         elif self.currentToken.type == PROCEDURE:
    #             self.eat(PROCEDURE)
    #             proc_name = self.currentToken.value
    #             self.eat(ID)
    #             params = []
    #
    #             if self.currentToken.type == LPAREN:
    #                 self.eat(LPAREN)
    #
    #                 params = self.formal_parameter_list()
    #
    #                 self.eat(RPAREN)
    #
    #             self.eat(SEMI)
    #             block_node = self.block()
    #             proc_decl = ProcedureDecl(proc_name, params, block_node)
    #             declarations.append(proc_decl)
    #             self.eat(SEMI)
    #         else:
    #             break
    #
    #     return declarations
    #
    # def formal_parameters(self):
    #     """ formal_parameters : ID (COMMA ID)* COLON type_spec """
    #     param_nodes = []
    #
    #     param_tokens = [self.currentToken]
    #     self.eat(ID)
    #     while self.currentToken.type == COMMA:
    #         self.eat(COMMA)
    #         param_tokens.append(self.currentToken)
    #         self.eat(ID)
    #
    #     self.eat(COLON)
    #     type_node = self.type_spec()
    #
    #     for param_token in param_tokens:
    #         param_node = Param(Var(param_token), type_node)
    #         param_nodes.append(param_node)
    #
    #     return param_nodes
    #
    #
    # def formal_parameter_list(self):
    #     """ formal_parameter_list : formal_parameters
    #                               | formal_parameters SEMI formal_parameter_list
    #     """
    #     # procedure Foo();
    #     if not self.currentToken.type == ID:
    #         return []
    #
    #     param_nodes = self.formal_parameters()
    #
    #     while self.currentToken.type == SEMI:
    #         self.eat(SEMI)
    #         param_nodes.extend(self.formal_parameters())
    #
    #     return param_nodes
    #
    #
    # def variable_declaration(self):
    #     """variable_declaration : ID (COMMA ID)* COLON type_spec"""
    #     var_nodes = [Var(self.currentToken)]  # first ID
    #     self.eat(ID)
    #
    #     while self.currentToken.type == COMMA:
    #         self.eat(COMMA)
    #         var_nodes.append(Var(self.currentToken))
    #         self.eat(ID)
    #
    #     self.eat(COLON)
    #
    #     type_node = self.type_spec()
    #     var_declarations = [
    #         VarDecl(var_node, type_node)
    #         for var_node in var_nodes
    #     ]
    #     return var_declarations
    #
    # def type_spec(self):
    #     """type_spec : INTEGER
    #                  | REAL
    #     """
    #     token = self.currentToken
    #     if self.currentToken.type == INT_TYPE:
    #         self.eat(INT_TYPE)
    #     else:
    #         self.eat(REAL)
    #     node = Type(token)
    #     return node
    #
    # def compound_statement(self):
    #     """
    #     compound_statement: BEGIN statement_list END
    #     """
    #     self.eat(BEGIN)
    #     nodes = self.statement_list()
    #     self.eat(END)
    #
    #     root = Compound()
    #     for node in nodes:
    #         root.children.append(node)
    #
    #     return root
    #
    # def statement_list(self):
    #     """
    #     statement_list : statement
    #                    | statement SEMI statement_list
    #     """
    #     node = self.statement()
    #
    #     results = [node]
    #
    #     while self.currentToken.type == SEMI:
    #         self.eat(SEMI)
    #         results.append(self.statement())
    #
    #     return results
    #
    # def statement(self):
    #     """
    #     statement : compound_statement
    #               | assignment_statement
    #               | empty
    #     """
    #     if self.currentToken.type == BEGIN:
    #         node = self.compound_statement()
    #     elif self.currentToken.type == ID:
    #         node = self.assignment_statement()
    #     else:
    #         node = self.empty()
    #     return node
    #
    # def assignment_statement(self):
    #     """
    #     assignment_statement : variable ASSIGN expr
    #     """
    #     left = self.variable()
    #     token = self.currentToken
    #     self.eat(ASSIGN)
    #     right = self.expr()
    #     node = Assign(left, token, right)
    #     return node
    #
    # def variable(self):
    #     """
    #     variable : ID
    #     """
    #     node = Var(self.currentToken)
    #     self.eat(ID)
    #     return node
    #
    # def empty(self):
    #     """An empty production"""
    #     return NoOp()
    #
    # def expr(self):
    #     """
    #     expr : term ((PLUS | MINUS) term)*
    #     """
    #     node = self.term()
    #
    #     while self.currentToken.type in (PLUS, MINUS):
    #         token = self.currentToken
    #         if token.type == PLUS:
    #             self.eat(PLUS)
    #         elif token.type == MINUS:
    #             self.eat(MINUS)
    #
    #         node = BinOp(left=node, op=token, right=self.term())
    #
    #     return node
    #
    # def term(self):
    #     """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
    #     node = self.factor()
    #
    #     while self.currentToken.type in (MUL, INTEGER_DIV, FLOAT_DIV):
    #         token = self.currentToken
    #         if token.type == MUL:
    #             self.eat(MUL)
    #         elif token.type == INTEGER_DIV:
    #             self.eat(INTEGER_DIV)
    #         elif token.type == FLOAT_DIV:
    #             self.eat(FLOAT_DIV)
    #
    #         node = BinOp(left=node, op=token, right=self.factor())
    #
    #     return node
    #
    # def factor(self):
    #     """factor : PLUS factor
    #               | MINUS factor
    #               | INTEGER_CONST
    #               | REAL_CONST
    #               | LPAREN expr RPAREN
    #               | variable
    #     """
    #     token = self.currentToken
    #     if token.type == PLUS:
    #         self.eat(PLUS)
    #         node = UnaryOp(token, self.factor())
    #         return node
    #     elif token.type == MINUS:
    #         self.eat(MINUS)
    #         node = UnaryOp(token, self.factor())
    #         return node
    #     elif token.type == INTEGER_CONST:
    #         self.eat(INTEGER_CONST)
    #         return Num(token)
    #     elif token.type == REAL_CONST:
    #         self.eat(REAL_CONST)
    #         return Num(token)
    #     elif token.type == LPAREN:
    #         self.eat(LPAREN)
    #         node = self.expr()
    #         self.eat(RPAREN)
    #         return node
    #     else:
    #         node = self.variable()
    #         return node
    #
    # def parse(self):
    #     """
    #     program : PROGRAM variable SEMI block DOT
    #     block : declarations compound_statement
    #     declarations : (VAR (variable_declaration SEMI)+)*
    #        | (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)*
    #        | empty
    #     variable_declaration : ID (COMMA ID)* COLON type_spec
    #     formal_params_list : formal_parameters
    #                        | formal_parameters SEMI formal_parameter_list
    #     formal_parameters : ID (COMMA ID)* COLON type_spec
    #     type_spec : INTEGER
    #     compound_statement : BEGIN statement_list END
    #     statement_list : statement
    #                    | statement SEMI statement_list
    #     statement : compound_statement
    #               | assignment_statement
    #               | empty
    #     assignment_statement : variable ASSIGN expr
    #     empty :
    #     expr : term ((PLUS | MINUS) term)*
    #     term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
    #     factor : PLUS factor
    #            | MINUS factor
    #            | INTEGER_CONST
    #            | REAL_CONST
    #            | LPAREN expr RPAREN
    #            | variable
    #     variable: ID
    #     """
    #     node = self.program()
    #     if self.currentToken.type != EOF:
    #         self.error()
    #
    #     return node
    #

