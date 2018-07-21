from test_fena.test_common import test_cmd

def test_xps():
    test_cmd("xp @s + 5", "xp @s 5")
    test_cmd("xp @s - 5", expect_error=True)
    test_cmd("xp @s = 5", expect_error=True)

    test_cmd("xp @s + 0", "xp @s 0")
    test_cmd("xp @s - 0", expect_error=True)
    test_cmd("xp @s = 0", expect_error=True)

    test_cmd("xp @s + -10", expect_error=True)
    test_cmd("xp @s - -10", expect_error=True)
    test_cmd("xp @s = -10", expect_error=True)

    test_cmd("xp @s + 5 points", "xp @s 5")
    test_cmd("xp @s - 5 points", expect_error=True)
    test_cmd("xp @s = 5 points", expect_error=True)

    test_cmd("xp @s + 5 levels", "xp @s 5L")
    test_cmd("xp @s - 5 levels", "xp @s -5L")
    test_cmd("xp @s = 5 levels", expect_error=True)

    test_cmd("xp @s <- points",  expect_error=True)
    test_cmd("xp @s <- levels",  expect_error=True)
    test_cmd("xp @s <- invalid", expect_error=True)


