if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

    import fena.logging_setup as logging_setup

import os
import json
import logging

from fena.assert_utils import assert_type

"""
Gets all config data from the config folder
"""

class ConfigData:
    """
    Singleton class based off of:
        https://colab.research.google.com/drive/1eajT5Rl9tA-7RmSHMME54B81U5aSKSni#scrollTo=nfQZINGxuUdK

    Sets its own attributes based off of:
        https://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python

    Attributes:
        version (str)
        ego (bool)
        leading_commands (list of strs)
        plugin_conflict_commands (list of strs)

        selector_variable_specifiers (list of strs)
        selector_arguments (list of strs)
        selector_replacements (dict): maps the shorthand version to the minecraft selector argument
        selector_argument_details (dict): maps each selector argument to the parse type and any other details
            - Uses the command json parse type

        execute_dimensions (dict)
        execute_comparison_operators (dict)
        execute_keywords (list)
        execute_data_types (list)

        scoreboard_math (dict)
        scoreboard_special (dict)

        blocks (list of strs)
        command_names (list of str objects): All possible command names
        bossbar_get (list of str objects)
        bossbar_set (dict)
        effects (list of strs)
        entities (list of strs)
        items (list of str objects)
        team_options (dict): maps each team option to its possible values
    """
    def __init__(self, **options):
        # for key in options:
        #     setattr(self, key, options[key])

        # changing the above to having all customly defined for pylint
        if options:
            self.version = options["version"]
            self.ego = options["ego"]
            self.leading_commands = options["leading_commands"]
            self.plugin_conflict_commands = options["plugin_conflict_commands"]

            self.selector_variable_specifiers = options["selector_variable_specifiers"]
            self.selector_arguments = options["selector_arguments"]
            self.selector_replacements = options["selector_replacements"]
            self.selector_argument_details = options["selector_argument_details"]

            self.execute_dimensions = options["execute_dimensions"]
            self.execute_keywords = options["execute_keywords"]
            self.execute_data_types = options["execute_data_types"]
            self.execute_comparison_operators = options["execute_comparison_operators"]

            self.scoreboard_math = options["scoreboard_math"]
            self.scoreboard_special = options["scoreboard_special"]

            self.blocks = options["blocks"]
            self.bossbar_set = options["bossbar_set"]
            self.bossbar_get = options["bossbar_get"]
            self.command_names = options["command_names"]
            self.effects = options["effects"]
            self.entities = options["entities"]
            self.items = options["items"]
            self.team_options = options["team_options"]

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

def _get_file_str(file_name):
    """
    Gets the data in the file string with the file path relative to this python file (config_data.py)

    Returns:
        str: The full file as a str
    """
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, "../config/" + file_name)

    with open(file_path, "r") as file:
        file_data = file.read()

    return file_data


# def _get_file_name(option_name, extension="txt"):
#     """
#     Gets the data inside the file given the version, option and extension
#
#     Args:
#         version (str)
#         option_name (str)
#         extension (str)
#     """
#     return f"{option_name}.{extension}"


def _get_config_data(version=None):
    """
    Gets all data from config.ini

    For each line:
     - splits with = to get the left hand side (LHS) and right hand side (RHS)
     - splits on "," at the RHS to get all the config options
     - creates the first of the singleton class of ConfigData

    Args:
        version (str or None): The file contents for testing purposes

    Returns:
        dict: All options found in config.ini
    """
    assert_type(version, str, optional=True)

    # the config file should be placed one directory below
    config_name = "config.ini"
    file_data = _get_file_str(config_name)
    options = {}

    # gets rid of empty lines, trailing whitespace and comments
    lines = [line.strip() for line in file_data.splitlines() if line.strip() if line.strip()[0] != "#"]

    # gets the list as a split through "," on the RHS unless it is the version
    for line in lines:
        option, data = line.split("=")
        if option == "version":
            options[option] = (data if version is None else version)
        elif option == "ego":
            options[option] = data
        else:
            options[option] = data.split(",")

    return options


def _get_json_config_data(version):
    """
    Gets data from:
        blocks.json
        bossbar.json
        command_names.json
        effects.json
        entities.json
        execute.json
        items.json
        scoreboard.json
        selector.json
        team_options.json

    Returns:
        dict: Maps "blocks", "command_names" and "entities" to their respective lists
    """
    # result for all files
    json_options = {}
    option_names = ("blocks", "bossbar", "command_names", "effects", "entities", "execute", "items", "selector", "scoreboard", "team_options")

    for option_name in option_names:
        file_name = f"{option_name}.json"
        file_str = _get_file_str(file_name)
        json_object = json.loads(file_str)

        # if it's a string, it refers back to the previous version completely
        # note that this does not prevent recursion
        while isinstance(json_object[version], str):
            version = json_object[version]

        # when config data has new versions
        if isinstance(json_object[version], list):
            json_options[option_name] = json_object[version]
        elif isinstance(json_object[version], dict):
            for option in json_object[version]:
                json_options[option] = json_object[version][option]
        elif json_object[version] is None:
            # doesn't do anything since there is no need to replace None with a different value
            pass
        else:
            raise SyntaxError("Unexpected default case")

    return json_options


def _validate_options(options, valid_options):
    """
    General function to validate that all valid options are found inside the options with no extra options

    Args:
        options (dict): All options found in the config file
        valid_options (frozenset): All expected options
    """
    # checks for a missing option using set difference
    missing_options = valid_options - frozenset(options.keys())
    extra_options = frozenset(options.keys()) - valid_options

    if missing_options:
        raise SyntaxError("{}: Option(s) were not found".format(set(missing_options)))

    if extra_options:
        raise SyntaxError("{}: Extra option(s) were detected".format(set(extra_options)))


def get_all_data(version=None):
    """
    Main function to get all data from all config files
    If a minecraft version needs to be specified, use this function with the requested version

    Args:
        version (str or None): Optional version to force the config to be read with a specific version
    """
    # gets all config data from config.ini and validates
    general_options = _get_config_data(version=version)
    valid_general_options = frozenset({"version", "ego", "leading_commands", "plugin_conflict_commands"})
    _validate_options(general_options, valid_general_options)

    # makes sure the version is correct
    valid_versions = frozenset({"1.12", "1.13"})
    version = general_options["version"]
    if version not in valid_versions:
        raise SyntaxError("{}: Invalid version in config (must be in {})".format(version, valid_versions))

    # makes sure "ego" is set to true or false (with any capitalization)
    valid_bool = frozenset({"true", "false"})
    ego = general_options["ego"].lower()
    if ego in valid_bool:
        if ego == "true":
            general_options["ego"] = True
        else:
            general_options["ego"] = False
    else:
        raise SyntaxError("{}: Invalid ego boolean value (must be in {})".format(ego, valid_bool))

    # gets all selector config options from the config data
    # selector_options = _get_selector_config_data(version)

    # gets all blocks, commands and entities
    json_options = _get_json_config_data(version)

    selector_json_args = {"selector_variable_specifiers", "selector_arguments", "selector_replacements", "selector_argument_details"}
    scoreboard_json_args = {"scoreboard_math", "scoreboard_special"}
    execute_json_args = {"execute_dimensions", "execute_keywords", "execute_data_types", "execute_comparison_operators"}
    general_json_args = {"blocks", "command_names", "effects", "entities", "items", "team_options"}
    bossbar_json_args = {"bossbar_set", "bossbar_get"}

    all_json_args = (selector_json_args | scoreboard_json_args | execute_json_args | general_json_args | bossbar_json_args)
    _validate_options(json_options, all_json_args)

    # ensures that this is the first instance of the ConfigData object
    all_options = {**general_options, **json_options}
    config_data = ConfigData(**all_options)
    logging.debug("Got the config data: {}".format(config_data))


get_all_data()

def test():
    # should be the original from the config file
    config_data = ConfigData()
    print(config_data)

    # completely different options
    # _get_config_data(file_data)
    # print(config_data)

    # check id value
    config_data_2 = ConfigData()
    assert id(config_data) == id(config_data_2), (id(config_data), id(config_data_2))

if __name__ == "__main__":
    config_data = ConfigData()
    print(json.dumps(vars(config_data), indent=4))
    print(list(vars(config_data)))
    # print(config_data)
    # test()
