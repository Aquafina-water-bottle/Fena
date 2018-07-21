from test_fena.test_common import test_block

def test_blocks():
    # block states as simple values
    test_block("stone_brick[0]",  expect_error=True)
    test_block("stone_brick[1]",  expect_error=True)
    test_block("stone_brick[-1]", expect_error=True)
    test_block("stone_brick[*]",  expect_error=True)
    test_block("stone_brick[]",   expect_error=True)
    test_block("stone_brick",     expect_error=True)
    test_block("minecraft:stone_brick[0]",  expect_error=True)
    test_block("minecraft:stone_brick[1]",  expect_error=True)
    test_block("minecraft:stone_brick[-1]", expect_error=True)
    test_block("minecraft:stone_brick[*]",  expect_error=True)
    test_block("minecraft:stone_brick[]",   expect_error=True)
    test_block("minecraft:stone_brick",     expect_error=True)

    # actual block states
    test_block("stone_brick_stairs[facing=south]",                   "minecraft:stone_brick_stairs[facing=south]")
    test_block("stone_brick_stairs[facing=south,half=top]",          "minecraft:stone_brick_stairs[facing=south,half=top]")
    test_block("stone_brick_stairs[facing=south, half=top]",         "minecraft:stone_brick_stairs[facing=south,half=top]")
    test_block("stone_brick_stairs[facing = south, half = top]",     "minecraft:stone_brick_stairs[facing=south,half=top]")
    test_block("stone_brick_stairs [ facing = south, half = top ] ", "minecraft:stone_brick_stairs[facing=south,half=top]")
    test_block("minecraft:stone_brick_stairs[facing=south]",                   "minecraft:stone_brick_stairs[facing=south]")
    test_block("minecraft:stone_brick_stairs[facing=south,half=top]",          "minecraft:stone_brick_stairs[facing=south,half=top]")
    test_block("minecraft:stone_brick_stairs[facing=south, half=top]",         "minecraft:stone_brick_stairs[facing=south,half=top]")
    test_block("minecraft:stone_brick_stairs[facing = south, half = top]",     "minecraft:stone_brick_stairs[facing=south,half=top]")
    test_block("minecraft:stone_brick_stairs [ facing = south, half = top ] ", "minecraft:stone_brick_stairs[facing=south,half=top]")

    # nbt tags
    test_block(r'chest[facing=west]{}',           r'minecraft:chest[facing=west]{}')
    test_block(r'chest[facing=west]{Lock:"lol"}', r'minecraft:chest[facing=west]{Lock:"lol"}')
    test_block(r'minecraft:chest[facing=west]{}')
    test_block(r'minecraft:chest[facing=west]{Lock:"lol"}')

    # errors
    test_block('not_a_block', expect_error=True)
    test_block("wrong_id:stone_brick", expect_error=True)
    test_block("stone_brick:stone_brick", expect_error=True)

    test_block('stone_brick[0,1]', expect_error=True)
    test_block('stone_brick[0=0,1=1]', expect_error=True)
    test_block('stone_brick[asdf=0,nou=1]', expect_error=True)
    test_block("stone_brick_stairs[=]", expect_error=True)
    test_block("stone_brick_stairs[facing]", expect_error=True)
    test_block("stone_brick_stairs[facing=]", expect_error=True)
    test_block("stone_brick_stairs[facing=south=north]", expect_error=True)
    test_block("stone_brick_stairs[facing=south half=top]", expect_error=True)

    test_block('minecraft:not_a_block', expect_error=True)
    test_block('minecraft:stone_brick[0,1]', expect_error=True)
    test_block('minecraft:stone_brick[0=0,1=1]', expect_error=True)
    test_block('minecraft:stone_brick[asdf=0,nou=1]', expect_error=True)
    test_block("minecraft:stone_brick_stairs[=]", expect_error=True)
    test_block("minecraft:stone_brick_stairs[facing]", expect_error=True)
    test_block("minecraft:stone_brick_stairs[facing=]", expect_error=True)
    test_block("minecraft:stone_brick_stairs[facing=south=north]", expect_error=True)
    test_block("minecraft:stone_brick_stairs[facing=south half=top]", expect_error=True)
