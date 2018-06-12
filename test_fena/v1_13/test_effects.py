from test_fena.test_common import test_cmd

def test_effects():
    test_cmd("effect @a - *",                          "effect clear @a")
    test_cmd("effect @a - saturation",                 "effect clear @a minecraft:saturation")
    test_cmd("effect @a + saturation",                 "effect give @a minecraft:saturation 2 0 true")
    test_cmd("effect @a + saturation 1000000",         "effect give @a minecraft:saturation 1000000 0 true")
    test_cmd("effect @a + saturation 1000000 1",       "effect give @a minecraft:saturation 1000000 1 true")
    test_cmd("effect @a + saturation 1000000 1 true",  "effect give @a minecraft:saturation 1000000 1 true")
    test_cmd("effect @a + saturation 1000000 1 false", "effect give @a minecraft:saturation 1000000 1 false")

    test_cmd("effect @a - minecraft:*",                          expect_error=True)
    test_cmd("effect @a - minecraft:saturation",                 "effect clear @a minecraft:saturation")
    test_cmd("effect @a + minecraft:saturation",                 "effect give @a minecraft:saturation 2 0 true")
    test_cmd("effect @a + minecraft:saturation 1000000",         "effect give @a minecraft:saturation 1000000 0 true")
    test_cmd("effect @a + minecraft:saturation 1000000 1",       "effect give @a minecraft:saturation 1000000 1 true")
    test_cmd("effect @a + minecraft:saturation 1000000 1 true",  "effect give @a minecraft:saturation 1000000 1 true")
    test_cmd("effect @a + minecraft:saturation 1000000 1 false", "effect give @a minecraft:saturation 1000000 1 false")

    test_cmd("effect @a - saturation extra_arg",          expect_error=True)
    test_cmd("effect @a - not_an_effect",                 expect_error=True)
    test_cmd("effect @a + saturation -25",                expect_error=True)
    test_cmd("effect @a + saturation 25 -1",              expect_error=True)
    test_cmd("effect @a + saturation 1000000 1 not_bool", expect_error=True)
    test_cmd("effect @a = invalid_operator",              expect_error=True)
