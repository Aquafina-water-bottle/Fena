from test_fena.test_common import test_cmd

def test_datas():
    test_cmd("data ~ ~ ~ <-",             expect_error=True)
    test_cmd("data ~ ~ ~ <- Items",       expect_error=True)
    test_cmd("data ~ ~ ~ <- Items.0",     expect_error=True)
    test_cmd("data ~ ~ ~ <- Items.0 1",   expect_error=True)
    test_cmd("data ~ ~ ~ <- Items.0 1.1", expect_error=True)

    test_cmd("data @s <-",                expect_error=True)
    test_cmd("data @s <- Movement",       expect_error=True)
    test_cmd("data @s <- Movement.2",     expect_error=True)
    test_cmd("data @s <- Movement.2 1",   expect_error=True)
    test_cmd("data @s <- Movement.2 1.1", expect_error=True)

    test_cmd(r'data ~ ~ ~ + {Lock:"asdf"}',  r'blockdata ~ ~ ~ {Lock:"asdf"}')
    test_cmd(r'data @s + {Invulnerable:1b}', r'entitydata @s {Invulnerable:1b}')

    test_cmd("data ~ ~ ~ - Lock",      expect_error=True)
    test_cmd("data @s - Invulnerable", expect_error=True)


    test_cmd("data (~ ~ ~) <-",             expect_error=True)
    test_cmd("data (~ ~ ~) <- Items",       expect_error=True)
    test_cmd("data (~ ~ ~) <- Items.0",     expect_error=True)
    test_cmd("data (~ ~ ~) <- Items.0 1",   expect_error=True)
    test_cmd("data (~ ~ ~) <- Items.0 1.1", expect_error=True)

    test_cmd("data (@s) <-",                expect_error=True)
    test_cmd("data (@s) <- Movement",       expect_error=True)
    test_cmd("data (@s) <- Movement.2",     expect_error=True)
    test_cmd("data (@s) <- Movement.2 1",   expect_error=True)
    test_cmd("data (@s) <- Movement.2 1.1", expect_error=True)

    test_cmd(r'data (~ ~ ~) + {Lock:"asdf"}',  r'blockdata ~ ~ ~ {Lock:"asdf"}')
    test_cmd(r'data (@s) + {Invulnerable:1b}', r'entitydata @s {Invulnerable:1b}')

    test_cmd("data (~ ~ ~) - Lock",      expect_error=True)
    test_cmd("data (@s) - Invulnerable", expect_error=True)


