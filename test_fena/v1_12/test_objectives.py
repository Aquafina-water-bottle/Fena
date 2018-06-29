from test_fena.test_common import test_cmd

def test_objectives():
    test_cmd("objective add asdf",                          expect_error=True)
    test_cmd("objective add asdf dummy",                    "scoreboard objectives add asdf dummy")
    test_cmd("objective add asdf dummy test",               "scoreboard objectives add asdf dummy test")
    test_cmd("objective add asdf dummy display name",       "scoreboard objectives add asdf dummy display name")
    test_cmd("objective add asdf dummy display name again", "scoreboard objectives add asdf dummy display name again")
    test_cmd("objective add asdf stat.leave_game",                    "scoreboard objectives add asdf stat.leave_game")
    test_cmd("objective add asdf stat.leave_game test",               "scoreboard objectives add asdf stat.leave_game test")
    test_cmd("objective add asdf stat.leave_game display name",       "scoreboard objectives add asdf stat.leave_game display name")
    test_cmd("objective add asdf stat.leave_game display name again", "scoreboard objectives add asdf stat.leave_game display name again")

    test_cmd("objective remove asdf",       "scoreboard objectives remove asdf")
    test_cmd("objective remove asdf asdf2", expect_error=True)

    test_cmd("objective setdisplay sidebar",            "scoreboard objectives setdisplay sidebar")
    test_cmd("objective setdisplay sidebar asdf",       "scoreboard objectives setdisplay sidebar asdf")
    test_cmd("objective setdisplay sidebar asdf asdf2", expect_error=True)
