from test_fena.test_common import test_cmd

def test_xps():
    test_cmd("xp @s + 5", "xp add @s 5 points")
    test_cmd("xp @s - 5", "xp add @s -5 points")
    test_cmd("xp @s = 5", "xp set @s 5 points")

    test_cmd("xp @s + 0", "xp add @s 0 points")
    test_cmd("xp @s - 0", "xp add @s -0 points")
    test_cmd("xp @s = 0", "xp set @s 0 points")

    test_cmd("xp @s + -10", expect_error=True)
    test_cmd("xp @s - -10", expect_error=True)
    test_cmd("xp @s = -10", expect_error=True)

    test_cmd("xp @s + 5 points", "xp add @s 5 points")
    test_cmd("xp @s - 5 points", "xp add @s -5 points")
    test_cmd("xp @s = 5 points", "xp set @s 5 points")

    test_cmd("xp @s + 5 levels", "xp add @s 5 levels")
    test_cmd("xp @s - 5 levels", "xp add @s -5 levels")
    test_cmd("xp @s = 5 levels", "xp set @s 5 levels")

    test_cmd("xp @s <- points",  "xp get @s points")
    test_cmd("xp @s <- levels",  "xp get @s levels")
    test_cmd("xp @s <- invalid", expect_error=True)

