"""
Singleton class that contains:
    objectives dict
    tags dict
    teams dict
    functions dict

    constobj
    prefix
"""

class InFileConfigData:
    def __init__(self):
        self.objectives = {}
        self.tags = {}
        self.teams = {}
        self.functions = {}
        self.constobj = None
        self.prefix = None
    
    def __new__(cls):
        """
        Ensures they are the same class
        """
        if not hasattr(cls, '_in_file_config_data'):
            cls._in_file_config_data = super().__new__(cls)
        return cls._in_file_config_data
