from test_fena.test_common import test_cmd

def test_simple_cmds():
    test_cmd("tag @s + _lol",                    "tag @s add fena.lol")
    test_cmd("tag @s - _lol",                    "tag @s remove fena.lol")
    test_cmd(r"tag @s + _lol {Invulnerable:1b}", expect_error=True)
    test_cmd(r"tag @s - _lol {Invulnerable:1b}", expect_error=True)

    test_cmd("tag target + _lol",                expect_error=True)
    test_cmd("tag target - _lol",                expect_error=True)
