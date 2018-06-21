
def test_item(*args, **kwargs): pass

def test_items():
    test_item(r"item @a - *",                                    r"clear @a")
    test_item(r"item @a - diamond_pickaxe",                      r"clear @a minecraft:diamond_pickaxe -1")
    test_item(r"item @a - diamond_pickaxe 1",                    r"clear @a minecraft:diamond_pickaxe 1")
    test_item(r"item @a - diamond_pickaxe[6]",                   expect_error=True) # damage values are now specified under nbt
    test_item(r"item @a - diamond_pickaxe[6] 1",                 expect_error=True)
    test_item(r'item @a - diamond_pickaxe{Unbreakable:1b}',      r"clear @a minecraft:diamond_pickaxe{Unbreakable:1b} -1")
    test_item(r'item @a - diamond_pickaxe{Unbreakable:1b} 1',    r"clear @a minecraft:diamond_pickaxe{Unbreakable:1b} 1")
    test_item(r'item @a - diamond_pickaxe[6]{Unbreakable:1b}',   expect_error=True)
    test_item(r'item @a - diamond_pickaxe[6]{Unbreakable:1b} 1', expect_error=True)

    test_item(r"item @a + diamond_pickaxe",                      r"give @a minecraft:diamond_pickaxe 1")
    test_item(r"item @a + diamond_pickaxe 1",                    r"give @a minecraft:diamond_pickaxe 1")
    test_item(r"item @a + diamond_pickaxe[6]",                   expect_error=True)
    test_item(r"item @a + diamond_pickaxe[6] 1",                 expect_error=True)
    test_item(r'item @a + diamond_pickaxe{Unbreakable:1b}',      r'give @a minecraft:diamond_pickaxe{Unbreakable:1b} 1')
    test_item(r'item @a + diamond_pickaxe{Unbreakable:1b} 1',    r'give @a minecraft:diamond_pickaxe{Unbreakable:1b} 1')
    test_item(r'item @a + diamond_pickaxe[6]{Unbreakable:1b}',   expect_error=True)
    test_item(r'item @a + diamond_pickaxe[6]{Unbreakable:1b} 1', expect_error=True)


    test_item(r"item @a armor.head = diamond_pickaxe",                      r"replaceitem entity @a armor.head minecraft:diamond_pickaxe 1")
    test_item(r"item @a armor.head = diamond_pickaxe 1",                    r"replaceitem entity @a armor.head minecraft:diamond_pickaxe 1")
    test_item(r"item @a armor.head = diamond_pickaxe[6]",                   expect_error=True)
    test_item(r"item @a armor.head = diamond_pickaxe[6] 1",                 expect_error=True)
    test_item(r'item @a armor.head = diamond_pickaxe{Unbreakable:1b}',      r'replaceitem entity @a armor.head minecraft:diamond_pickaxe{Unbreakable:1b} 1')
    test_item(r'item @a armor.head = diamond_pickaxe{Unbreakable:1b} 1',    r'replaceitem entity @a armor.head minecraft:diamond_pickaxe{Unbreakable:1b} 1')
    test_item(r'item @a armor.head = diamond_pickaxe[6]{Unbreakable:1b}',   expect_error=True)
    test_item(r'item @a armor.head = diamond_pickaxe[6]{Unbreakable:1b} 1', expect_error=True)

    test_item(r"item ~ ~-1 ~ container.0 = diamond_pickaxe",                      r"replaceitem block ~ ~-1 ~ container.0 minecraft:diamond_pickaxe 1")
    test_item(r"item ~ ~-1 ~ container.0 = diamond_pickaxe 1",                    r"replaceitem block ~ ~-1 ~ container.0 minecraft:diamond_pickaxe 1")
    test_item(r"item ~ ~-1 ~ container.0 = diamond_pickaxe[6]",                   expect_error=True)
    test_item(r"item ~ ~-1 ~ container.0 = diamond_pickaxe[6] 1",                 expect_error=True)
    test_item(r'item ~ ~-1 ~ container.0 = diamond_pickaxe{Unbreakable:1b}',      r'replaceitem block ~ ~-1 ~ container.0 minecraft:diamond_pickaxe{Unbreakable:1b} 1')
    test_item(r'item ~ ~-1 ~ container.0 = diamond_pickaxe{Unbreakable:1b} 1',    r'replaceitem block ~ ~-1 ~ container.0 minecraft:diamond_pickaxe{Unbreakable:1b} 1')
    test_item(r'item ~ ~-1 ~ container.0 = diamond_pickaxe[6]{Unbreakable:1b}',   expect_error=True)
    test_item(r'item ~ ~-1 ~ container.0 = diamond_pickaxe[6]{Unbreakable:1b} 1', expect_error=True)

