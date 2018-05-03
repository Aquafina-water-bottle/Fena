import os
import logging
import json

"""
Gets all config data from the config folder
"""

class ConfigData:
    """
    Singleton class based off of:
        https://colab.research.google.com/drive/1eajT5Rl9tA-7RmSHMME54B81U5aSKSni#scrollTo=nfQZINGxuUdK

    Sets its own attributes based off of:
        https://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python
    """
    def __init__(self, **options):
        # for key in options:
        #     setattr(self, key, options[key])

        # changing the above to having all customly defined for pylint
        if options:
            self.commands = options["commands"]
            self.leading_commands = options["leading_commands"]
            self.plugin_conflict_commands = options["plugin_conflict_commands"]
            self.version = options["version"]
            self.selector_variables = options["selector_variables"]
            self.selector_arguments = options["selector_arguments"]
            self.selector_replacements = options["selector_replacements"]
            self.selector_argument_details = options["selector_argument_details"]

    def __new__(cls, **options):
        """
        Ensures they are the same class
        """
        if not hasattr(cls, '_config_data'):
            cls._config_data = super().__new__(cls)
        return cls._config_data

    def __str__(self):
        return "ConfigData[vars={}]".format(vars(self))

    __repr__ = __str__

def _get_config_data(file_data=None):
    """
    For each line:
     - splits with = to get the left hand side (LHS) and right hand side (RHS)
     - splits on "," at the RHS to get all the config options
     - creates the first of the singleton class of ConfigData

    Args:
        file_data (str): The file contents for testing purposes
            It is default to none so the config file can be read.
    """

    # the config file should be placed one directory below
    CONFIG_NAME = "../config.ini"

    # all possible option keys
    valid_config_options = frozenset({"commands", "leading_commands", "plugin_conflict_commands", "version"})
    valid_versions = frozenset({"1.12", "1.13"})

    # all keys that have been retrieved
    # this is stored as a set since order doesn't really matter
    retrieved_options = set()
    options = {}

    if file_data is None:
        # gets absolute path of this config_data.py file
        dir_path = os.path.dirname(__file__)
        file_path = os.path.join(dir_path, CONFIG_NAME)

        with open(file_path, "r") as file:
            file_data = file.read()

    # gets rid of empty lines, trailing whitespace and comments
    lines = [line.strip() for line in file_data.splitlines() if line.strip() if line.strip()[0] != "#"]
    for line in lines:
        option, data = line.split("=")

        if option in valid_config_options:
            # finds duplicate by checking if there is a new option already inside the retireved options
            if option in retrieved_options:
                raise SyntaxError("Repeated option {} found in the config file".format(option))
            retrieved_options.add(option)

        else:
            raise SyntaxError("Option {} was not found inside existing config options {}".format(repr(option), valid_config_options))

        # gets the list as a split through "," on the RHS unless it is the version
        if option == "version":
            if data not in valid_versions:
                raise SyntaxError("{}: Invalid version in config (must be in {})".format(data, valid_versions))
            options[option] = data
        else:
            options[option] = data.split(",")

    # checks for a missing option using set difference
    options_difference = valid_config_options - retrieved_options

    # runs only if there are items in the set difference
    # meaning all in the difference are missing
    if options_difference:
        raise SyntaxError("Option(s) {} were not found".format(options_difference))

    # gets all selector config options from the config data
    valid_selector_config_options = frozenset({"selector_variables", "selector_arguments", "selector_replacements", "selector_argument_details"})
    json_data = _get_selector_config_data(options["version"])

    # checks whether the options defined in the config file are more or less than expected
    if frozenset(json_data.keys()) != valid_selector_config_options:
        # TODO specify which
        raise SyntaxError("Missing keys or too many keys in the json data")

    for selector_option in valid_selector_config_options:
        options[selector_option] = json_data[selector_option]

    # ensures that this is the first instance of the ConfigData object
    config_data = ConfigData(**options)
    logging.debug("Got the config data: {}".format(config_data))


def _get_selector_config_data(version, file_data=None):
    """
    Gets the full json file with the standard library json decoder

    Args:
        file_data (str): The file contents for testing purposes
            It is default to none so the config file can be read.
    """
    # the config file should be placed one directory below
    CONFIG_NAME = "../selector_config_{}.json".format(version)

    if file_data is None:
        # gets absolute path of this config_data.py file
        dir_path = os.path.dirname(__file__)
        file_path = os.path.join(dir_path, CONFIG_NAME)

        with open(file_path, "r") as file:
            return json.load(file)


# this should only be ran inside this folder, hence why it is private
_get_config_data()

def test():
    file_data = """
        # comment=lol,lolol
        commands=totally_a_command,yep
        leading_commands=execute
        plugin_conflict_commands=nope,avi

        version=1.13
    """

    # should be the original from the config file
    config_data = ConfigData()
    print(config_data)

    # completely different options
    _get_config_data(file_data)
    print(config_data)

    # check id value
    config_data_2 = ConfigData()
    print(id(config_data), id(config_data_2))

if __name__ == "__main__":
    test()
