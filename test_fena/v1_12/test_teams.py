from test_fena.test_common import test_cmd

def test_teams():
    test_cmd("team add _team team_test", "scoreboard teams add fena.team team_test")
    test_cmd("team add _team team test", "scoreboard teams add fena.team team test")
    test_cmd("team empty _team",         "scoreboard teams empty fena.team")
    test_cmd("team _team + @a",          "scoreboard teams join fena.team @a")
    test_cmd("team _team + target",      "scoreboard teams join fena.team target")
    test_cmd("team leave @a",            "scoreboard teams leave @a")
    test_cmd("team leave target",        "scoreboard teams leave target")
    test_cmd("team remove _team",        "scoreboard teams remove fena.team")

    test_cmd("team _team friendlyfire = true",               "scoreboard teams option fena.team friendlyfire true")
    test_cmd("team _team color = green",                     "scoreboard teams option fena.team color green")
    test_cmd("team _team seeFriendlyInvisibles = false",     "scoreboard teams option fena.team seeFriendlyInvisibles false")
    test_cmd("team _team nametagVisibility = hideForOwnTeam", "scoreboard teams option fena.team nametagVisibility hideForOwnTeam")
    test_cmd("team _team deathMessageVisibility = never",    "scoreboard teams option fena.team deathMessageVisibility never")
    test_cmd("team _team collisionRule = pushOwnTeam",       "scoreboard teams option fena.team collisionRule pushOwnTeam")

    test_cmd(r'team _team prefix = {"text":"PREFIX","color":"blue"}', expect_error=True)
    test_cmd(r'team _team suffix = {"text":"SUFFIX","color":"red"}',  expect_error=True)