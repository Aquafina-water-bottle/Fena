import os
import json
import logging
from types import MappingProxyType
from typing import NamedTuple, Set

if __name__ == "__main__":
    import sys
    sys.path.append("..")

from fenalib.assert_utils import assert_type
from fenalib.singleton import Singleton

"""
Gets all config data from the config folder
[
    "output"
    "debug"
    "clean"
    "ego"
    "debug_log"
    "plugin_cmds"
    "leading_cmds"
]
"""

PATH_TO_CONFIG_DIR = "config/"
MAIN_CONFIG_NAME = "config.ini"


class PreConfigDataBase(NamedTuple):
    input_file: str
    output_dir: str
    version: str
    simple: bool

class PreConfigData(Singleton, PreConfigDataBase):
    """
    Attributes:
        input_file (str): the input file as the main fena file
        output_dir (str): the output directory
        version (str): pass
        simple (bool): pass
    """
    pass


class ConfigDataBase(NamedTuple):
    debug: bool
    clean: bool
    ego: bool
    debug_log: bool
    plugin_cmds: Set[str]
    leading_cmds: Set[str]

class ConfigData(Singleton, ConfigDataBase):
    """
    Attributes:
        debug (bool): whether the mcfunctions should be in debug mode or not
        clean (bool): whether mcfunctions should be cleaned in general or not
        ego (bool): whether this is specifically used for EdgeGamers' servers
            Currently, it does the following:
            - warns for a lack of prefixes
        debug_log (bool): Whether the log files should be written during the interpreting
        plugin_cmds (Set[str]): All command names that should be proceeded with `minecraft:`
            - eg. if `tp` is inside it, the parsed command name is `minecraft:tp`
        leading_cmds (Set[str]): The commands that can have commands after it
    """


def _get_file_str(file_name):
    """
    Gets the data in the file string with the file path relative to this python file (config_data.py)

    Returns:
        str: The full file as a str
    """
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, PATH_TO_CONFIG_DIR + file_name)

    with open(file_path, "r") as file:
        file_data = file.read()

    return file_data


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
    file_data = _get_file_str(MAIN_CONFIG_NAME)
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
        replaceitem.json
        selector.json
        team_options.json

    Returns:
        dict: Maps "blocks", "command_names" and "entities" to their respective lists
    """
    # result for all files
    json_options = {}
    option_names = ("blocks", "bossbar", "command_names", "effects", "entities", "execute", "items", "selector", "scoreboard", "replaceitem", "team_options")

    for option_name in option_names:
        file_name = f"{option_name}.json"
        file_str = _get_file_str(file_name)
        json_object = json.loads(file_str)

        # if it's a string, it refers back to the previous version completely
        # note that this does not prevent recursion
        # use 'temp_version' to not change the actual version variable for the next usage
        temp_version = version
        while isinstance(json_object[temp_version], str):
            temp_version = json_object[temp_version]

        # when config data has new versions
        if isinstance(json_object[temp_version], list):
            json_options[option_name] = json_object[temp_version]
        elif isinstance(json_object[temp_version], dict):
            for option in json_object[temp_version]:
                json_options[option] = json_object[temp_version][option]
        elif json_object[temp_version] is None:
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
        raise SyntaxError(f"{set(missing_options)}: Option(s) were not found")

    if extra_options:
        raise SyntaxError(f"{set(extra_options)}: Extra option(s) were detected")


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
        raise SyntaxError(f"{version}: Invalid version in config (must be in {valid_versions})")

    # makes sure "ego" is set to true or false (with any capitalization)
    valid_bool = frozenset({"true", "false"})
    ego = general_options["ego"].lower()
    if ego in valid_bool:
        general_options["ego"] = (ego == "true")
    else:
        raise SyntaxError(f"{ego}: Invalid ego boolean value (must be in {valid_bool})")

    # gets all selector config options from the config data
    # selector_options = _get_selector_config_data(version)

    # gets all blocks, commands and entities
    json_options = _get_json_config_data(version)

    # ensures that this is the first instance of the ConfigData object
    all_options = {**general_options, **json_options}
    config_data = ConfigData(**all_options)
    logging.debug(f"Got the config data: {config_data}")


# get_all_data()

if __name__ == "__main__":
    import fenalib.logging_setup as logging_setup
    # get_all_data(version="1.12")
    # print(json.dumps(dict(ConfigData().variables), indent=4))
    # print(list(ConfigData().team_options))
    # get_all_data(version="1.13")
    # print(list(ConfigData().team_options))
    # print(ConfigData().variables)
    # print(list(ConfigData().variables))
    # print(ConfigData().replaceitem_entity_slots)
    # print(config_data)
    # test()



