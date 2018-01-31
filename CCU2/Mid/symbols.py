import logging

class Symbol():
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class VarSymbol(Symbol):
    """Represents a variable, with the name and type"""
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type,
        )

    __repr__ = __str__


class BuiltinTypeSymbol(Symbol):
    """Represents a built in type"""
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


class ProcedureSymbol(Symbol):
    """Represents a procedure, with a name and parameters"""
    def __init__(self, name, params=None):
        super(ProcedureSymbol, self).__init__(name)
        # a list of formal parameters
        self.params = params if params is not None else []

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params,
        )

    __repr__ = __str__


class ScopedSymbolTable(object):
    """
    stores all symbols within one scope
    
    symbol can be:
        -procedure
        -variable
        -type
    """
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope

    def _init_builtins(self):
        self.insert(BuiltinTypeSymbol('INTEGER'))
        self.insert(BuiltinTypeSymbol('REAL'))

    def __str__(self):
        # stores all outputted lines in a list
        lines = []
        
        # creates the header and a line of "=" underneath said title
        header1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines.append("")
        lines.append(header1)
        
        # outputs scope name, level, and enclosing scope
        infoPlaceholder = "\t%-15s: %s"
        lines.append(infoPlaceholder % ("Scope name", self.scope_name))
        lines.append(infoPlaceholder % ("Scope level", self.scope_level))
        
        # either prints out "None" if there is no enclosing scope
        # or prints the actual enclosing scope
        if self.enclosing_scope is None:
            lines.append(infoPlaceholder % ("Enclosing scope", None))
        else:
            lines.append(infoPlaceholder % ("Enclosing scope", self.enclosing_scope.scope_name))
            
        # outputs the header for the contents
        header2 = '\tScope (Scoped symbol table) CONTENTS'
        lines.append(header2)
        
        # outputs contents of the scoped table
        contentPlaceholder = "\t\t%-10s: %s"
        for key, value in self._symbols.items():
            lines.append(contentPlaceholder % (key, value))
        
        lines.append("")

        return '\n'.join(lines)

    __repr__ = __str__

    def insert(self, symbol):
        logging.debug('Insert: %s' % symbol.name)
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        """
        ???
        """
        print(name, type(name))
        logging.debug('Lookup: %s. (Scope name: %s)' % (name, self.scope_name))

        # 'symbol' is either an instance of the Symbol class or None
        symbol = self._symbols.get(name)

        if symbol is not None:
            return symbol
        
        if current_scope_only:
            return None

        # recursively go up the chain and lookup the name
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)

