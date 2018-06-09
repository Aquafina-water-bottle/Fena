from test_fena.test_common import test_cmd

def test_executes():
    test_cmd(
        "@p ~2 ~1 ~-1 @a 3 5.2 -2 @s @r if(stonebrick[0] 2 ~-1 ~) @e if(stonebrick): say @a",
        "execute @p ~ -4.2 3 execute @a ~ ~ ~ execute @s ~ ~ ~ execute @r ~ ~ ~ detect ~ ~-1 ~ minecraft:stonebrick 0 execute @e ~ ~ ~ detect ~ ~ ~ minecraft:stonebrick * say @a")
    test_cmd(
        "@s @s @s: kill @a",
        "execute @s ~ ~ ~ execute @s ~ ~ ~ execute @s ~ ~ ~  kill @a")
    test_cmd(
        "@a if(stonebrick) @a if(stonebrick): clear",
        "execute @a ~ ~ ~ detect ~ ~ ~ stonebrick * execute @a ~ ~ ~ detect ~ ~ ~ stonebrick * say test")
    test_cmd(
        "@s if(stonebrick ~ ~-1 ~) @s if(stonebrick_stairs[facing=west]) @s if(stonebrick ~ ~1 ~): kill",
        "execute @s ~ ~ ~ detect ~ ~-1 ~ stonebrick * execute @s ~ ~ ~ detect ~ ~ ~ stonebrick_stairs facing=west execute @s ~ ~ ~ detect ~ ~1 ~ stonebrick * kill")
    test_cmd(
        "@s if(stonebrick ~ ~-1 ~, stonebrick_stairs[facing=west], stonebrick ~ ~1 ~): kill",
        "execute @s ~ ~ ~ detect ~ ~-1 ~ stonebrick * execute @s ~ ~ ~ detect ~ ~ ~ stonebrick_stairs facing=west execute @s ~ ~ ~ detect ~ ~1 ~ stonebrick * kill")

    test_cmd("@a: say test", "execute @a ~ ~ ~ say test")
    test_cmd("@a ~ ~ ~: say test", "execute @a ~ ~ ~ say test")
    test_cmd("@a if(stonebrick[0]): say test", "execute @a ~ ~ ~ detect ~ ~ ~ stonebrick 0 say test")

    # no colon
    test_cmd("@a say test", expect_error=True)
