from test_fena.test_common import test_cmd

def test_simple_cmds():
    test_cmd(r'bossbar add test {"text":"test"}', expect_error=True) # not under command_names.json

    test_cmd("tag @s + _lol",     "scoreboard players tag @s add fena.lol")
    test_cmd("tag @s - _lol",     "scoreboard players tag @s remove fena.lol")
    test_cmd("tag target + _lol", expect_error=True)
    test_cmd("tag target - _lol", expect_error=True)
    test_cmd(r"tag @s + _lol {Invulnerable:1b}", r"scoreboard players tag @s add fena.lol {Invulnerable:1b}")
    test_cmd(r"tag @s - _lol {Invulnerable:1b}", r"scoreboard players tag @s remove fena.lol {Invulnerable:1b}")

    test_cmd("particle happy_villager ~ ~ ~")
    test_cmd("particle minecraft:happy_villager ~ ~ ~")
    test_cmd(r'give @s diamond_pickaxe 1 0 {display:{Name:"test"}}')
    test_cmd(r'give @s minecraft:diamond_pickaxe 1 0 {display:{Name:"test"}}')
    test_cmd(r'give @s minecraft:diamond_pickaxe')

