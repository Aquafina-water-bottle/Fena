from test_fena.test_common import test_cmd

def test_executes():
    test_cmd(
        "@p ~2 ~1 ~-1 @a 3 5.2 -2 @s @r if(stonebrick[0] 2 ~-1 ~) @e if(stonebrick): say @a",
        "execute @p ~2 ~1 ~-1 execute @a 3 5.2 -2 execute @s ~ ~ ~ execute @r ~ ~ ~ detect 2 ~-1 ~ minecraft:stonebrick 0 execute @e ~ ~ ~ detect ~ ~ ~ minecraft:stonebrick * say @a")
    test_cmd(
        "@s @s @s: kill @a",
        "execute @s ~ ~ ~ execute @s ~ ~ ~ execute @s ~ ~ ~ kill @a")
    test_cmd(
        "@a if(stonebrick) @a if(stonebrick): clear",
        "execute @a ~ ~ ~ detect ~ ~ ~ minecraft:stonebrick * execute @a ~ ~ ~ detect ~ ~ ~ minecraft:stonebrick * clear")
    test_cmd(
        "@s if(stonebrick ~ ~-1 ~) @s if(stone_brick_stairs[facing=west]) @s if(minecraft:stonebrick ~ ~1 ~): kill",
        "execute @s ~ ~ ~ detect ~ ~-1 ~ minecraft:stonebrick * execute @s ~ ~ ~ detect ~ ~ ~ minecraft:stone_brick_stairs facing=west execute @s ~ ~ ~ detect ~ ~1 ~ minecraft:stonebrick * kill")
    test_cmd(
        "@s if(stonebrick ~ ~-1 ~, stone_brick_stairs[facing=west], stonebrick ~ ~1 ~): kill",
        "execute @s ~ ~ ~ detect ~ ~-1 ~ minecraft:stonebrick * execute @s ~ ~ ~ detect ~ ~ ~ minecraft:stone_brick_stairs facing=west execute @s ~ ~ ~ detect ~ ~1 ~ minecraft:stonebrick * kill")

    test_cmd("@a: say test", "execute @a ~ ~ ~ say test")
    test_cmd("@a ~ ~ ~: say test", "execute @a ~ ~ ~ say test")
    test_cmd("@a if(stonebrick[0]): say test", "execute @a ~ ~ ~ detect ~ ~ ~ minecraft:stonebrick 0 say test")

    test_cmd("@a: clear",                  "execute @a ~ ~ ~ clear")
    test_cmd("@a: clear @s",               "execute @a ~ ~ ~ clear @s")
    # test_cmd("@a: clear @s stonebrick",    "execute @a ~ ~ ~ clear @s minecraft:stonebrick 0")
    test_cmd("@a: clear @s stonebrick",    "execute @a ~ ~ ~ clear @s stonebrick")

    # no colon
    test_cmd("@a clear", expect_error=True)
    test_cmd("@a clear @s", expect_error=True)
    test_cmd("@a clear @s stonebrick", expect_error=True)
    test_cmd("@a clear @s stonebrick 0", expect_error=True)
