import os
from collections import deque

from config_data import ConfigData

class SimpleCommandBuilder:
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

class ExecuteCommandBuilder(SimpleCommandBuilder):
    def __init__(self, *tokens):
        super().__init__(*tokens)

class ScoreboardCommandBuilder(SimpleCommandBuilder):
    def __init__(self, *tokens):
        super().__init__(*tokens)

class FunctionCommandBuilder(SimpleCommandBuilder):
    def __init__(self, *tokens):
        super().__init__(*tokens)
