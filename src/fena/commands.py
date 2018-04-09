from config_data import ConfigData
config_data = ConfigData()

class Command:
    """
    Holds branching simple commands using a builder model
    Args:
        tokens (list of Tokens)
    """
    def __init__(self, tokens):
        self.tokens = tokens

    def build(self, prefix=None):
        """
        Builds itself so the string representation can be used
        """
        pass

    def _add_execute(self, *tokens):
        pass

    def _add_scoreboard(self, *tokens):
        pass

    def _add_function(self, *tokens):
        pass

    def _add_simple(self, *tokens):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass

class SimpleCommand:
    """
    Attributes:
        tokens (tuple of Tokens)
    """
    def __init__(self, *tokens):
        self.tokens = tokens

    def build(self, prefix=None):
        pass

    def __str__(self):
        pass

class ExecuteCommand(SimpleCommand):
    def __init__(self, *tokens):
        super().__init__(*tokens)

class ScoreboardCommand(SimpleCommand):
    def __init__(self, *tokens):
        super().__init__(*tokens)

class FunctionCommand(SimpleCommand):
    def __init__(self, *tokens):
        super().__init__(*tokens)
