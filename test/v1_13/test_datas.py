from test_fena.test_common import test_cmd

def test_datas():
    test_cmd("data ~ ~ ~ <-",             "data get block ~ ~ ~")
    test_cmd("data ~ ~ ~ <- Items",       "data get block ~ ~ ~ Items")
    test_cmd("data ~ ~ ~ <- Items.0",     "data get block ~ ~ ~ Items.0")
    test_cmd("data ~ ~ ~ <- Items.0 1",   "data get block ~ ~ ~ Items.0 1")
    test_cmd("data ~ ~ ~ <- Items.0 1.1", "data get block ~ ~ ~ Items.0 1.1")

    test_cmd("data @s <-",                "data get entity @s")
    test_cmd("data @s <- Movement",       "data get entity @s Movement")
    test_cmd("data @s <- Movement.2",     "data get entity @s Movement.2")
    test_cmd("data @s <- Movement.2 1",   "data get entity @s Movement.2 1")
    test_cmd("data @s <- Movement.2 1.1", "data get entity @s Movement.2 1.1")

    test_cmd(r'data ~ ~ ~ + {Lock:"asdf"}',  r'data merge block ~ ~ ~ {Lock:"asdf"}')
    test_cmd(r'data @s + {Invulnerable:1b}', r'data merge entity @s {Invulnerable:1b}')

    test_cmd("data ~ ~ ~ - Lock",      "data remove block ~ ~ ~ Lock")
    test_cmd("data @s - Invulnerable", "data remove entity @s Invulnerable")


    test_cmd("data (~ ~ ~) <-",             "data get block ~ ~ ~")
    test_cmd("data (~ ~ ~) <- Items",       "data get block ~ ~ ~ Items")
    test_cmd("data (~ ~ ~) <- Items.0",     "data get block ~ ~ ~ Items.0")
    test_cmd("data (~ ~ ~) <- Items.0 1",   "data get block ~ ~ ~ Items.0 1")
    test_cmd("data (~ ~ ~) <- Items.0 1.1", "data get block ~ ~ ~ Items.0 1.1")

    test_cmd("data (@s) <-",                "data get entity @s")
    test_cmd("data (@s) <- Movement",       "data get entity @s Movement")
    test_cmd("data (@s) <- Movement.2",     "data get entity @s Movement.2")
    test_cmd("data (@s) <- Movement.2 1",   "data get entity @s Movement.2 1")
    test_cmd("data (@s) <- Movement.2 1.1", "data get entity @s Movement.2 1.1")

    test_cmd(r'data (~ ~ ~) + {Lock:"asdf"}',  r'data merge block ~ ~ ~ {Lock:"asdf"}')
    test_cmd(r'data (@s) + {Invulnerable:1b}', r'data merge entity @s {Invulnerable:1b}')

    test_cmd("data (~ ~ ~) - Lock",      "data remove block ~ ~ ~ Lock")
    test_cmd("data (@s) - Invulnerable", "data remove entity @s Invulnerable")

