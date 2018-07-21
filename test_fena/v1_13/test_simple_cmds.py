from test_fena.test_common import test_cmd

def test_simple_cmds():
    test_cmd("tag @s + _lol",                    "tag @s add fena.lol")
    test_cmd("tag @s - _lol",                    "tag @s remove fena.lol")
    test_cmd(r"tag @s + _lol {Invulnerable:1b}", expect_error=True)
    test_cmd(r"tag @s - _lol {Invulnerable:1b}", expect_error=True)

    test_cmd("tag target + _lol",                expect_error=True)
    test_cmd("tag target - _lol",                expect_error=True)

    test_cmd("particle happy_villager ~ ~ ~")
    test_cmd("particle minecraft:happy_villager ~ ~ ~")
    # TODO: rework of the entire damn parser (must create whitespace tokens with replacement=' ')
    # test_cmd(r'give @s diamond_pickaxe{display:{Name:"\"test\""}}')
    # test_cmd(r'give @s minecraft:diamond_pickaxe{display:{Name:"\"test\""}}')
    test_cmd(r'give @s minecraft:diamond_pickaxe')
