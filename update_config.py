import json

"""
Automatically updates the following json files for the specified version argument:
    blocks.json
    command_names.json
    effects.json
    entities.json

Dependencies:
    https://github.com/PepijnMC/Minecraft/
    https://github.com/Arcensoth/mcdata/
"""

# specifies the path to get to their respective directories
version = "1.13"
path_to_pepijn = r"../../Github/Minecraft-PepijnMC/Data/"
path_to_arcensoth = r"../../Github/Minecraft-Arcensoth-Generated/generated/reports/"
path_to_config = r"config/"

def update(version):
    update_blocks(path_to_arcensoth + "blocks.json", path_to_config + "blocks.json")
    update_command_names(path_to_arcensoth + "commands.json", path_to_config + "command_names.json")
    update_effects(path_to_pepijn + "potion_colors.json", path_to_config + "effects.json")
    update_entities(path_to_pepijn + "entities.txt", path_to_config + "entities.json")
    update_items(path_to_arcensoth + "items.json", path_to_config + "items.json")

def update_blocks(input_file, config_file):
    """
    Updates blocks by converting the file into a json object
    and getting all the keys from the main json object
    """
    with open(input_file) as file:
        json_object = json.load(file)

    json_list = sorted(remove_id(block) for block in json_object)
    update_file(config_file, json_list)

def update_command_names(input_file, config_file):
    """
    Updates command names by converting the file into a json object
    and getting all the args from "children" from the main json object
    """
    with open(input_file) as file:
        json_object = json.load(file)

    json_list = sorted(json_object["children"])
    update_file(config_file, json_list)

def update_effects(input_file, config_file):
    """
    Updates effects from getting the all string arguments
    from the main json object of pepijn/potion_colors.json
    """
    with open(input_file) as file:
        json_object = json.load(file)

    # removes all "minecraft:" from the effects
    json_list = sorted(remove_id(effect) for effect in json_object)
    update_file(config_file, json_list)

def update_entities(input_file, config_file):
    """
    Updates entities by reading each line under entities.txt and putting it into a list
    """

    # removes all "minecraft:" from the entities.txt file
    with open(input_file) as file:
        json_list = sorted(remove_id(line) for line in file.read().splitlines() if line)

    update_file(config_file, json_list)

def update_items(input_file, config_file):
    """
    Updates items by converting the file into a json object
    and getting all the keys from the main json object
    """

    # removes all "minecraft:" from the entities.txt file
    with open(input_file) as file:
        json_object = json.load(file)

    json_list = sorted(remove_id(item) for item in json_object)
    update_file(config_file, json_list)

def remove_id(string):
    """
    Removes "minecraft:" at the beginning of a string
    """
    assert string.startswith("minecraft:"), string
    return string[len("minecraft:"):]

def update_file(input_file, json_value):
    """
    Updates the input_file by replacing the main json object's version (json argument)
    with the given json value
    """
    with open(input_file) as file:
        json_object = json.load(file)

    json_object[version] = json_value
    json_str = json.dumps(json_object, indent="    ")

    with open(input_file, "w") as file:
        json_str = json.dumps(json_object, indent="    ")
        file.write(json_str)

if __name__ == "__main__":
    update(version)