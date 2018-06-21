# For future support of modifyitem

def test_item(*args, **kwargs): pass

def test_items():
    # clear <selector> [item] [data] [maxCount] [nbt]
    # data of -1 clears all with arbitrary data
    # maxCount of -1 clears all
    test_item(r"item @a - *",                                    r"clear @a")
    test_item(r"item @a - diamond_pickaxe",                      r"clear @a minecraft:diamond_pickaxe -1 -1")
    test_item(r"item @a - diamond_pickaxe 1",                    r"clear @a minecraft:diamond_pickaxe -1 1")
    test_item(r"item @a - diamond_pickaxe[6]",                   r"clear @a minecraft:diamond_pickaxe 6 -1")
    test_item(r"item @a - diamond_pickaxe[6] 1",                 r"clear @a minecraft:diamond_pickaxe 6 1")
    test_item(r'item @a - diamond_pickaxe{Unbreakable:1b}',      r"clear @a minecraft:diamond_pickaxe -1 -1 {Unbreakable:1b}")
    test_item(r'item @a - diamond_pickaxe{Unbreakable:1b} 1',    r"clear @a minecraft:diamond_pickaxe -1 1 {Unbreakable:1b}")
    test_item(r'item @a - diamond_pickaxe[6]{Unbreakable:1b}',   r"clear @a minecraft:diamond_pickaxe 6 -1 {Unbreakable:1b}")
    test_item(r'item @a - diamond_pickaxe[6]{Unbreakable:1b} 1', r"clear @a minecraft:diamond_pickaxe 6 1 {Unbreakable:1b}")

    test_item(r"item @a + diamond_pickaxe",                      r"give @a minecraft:diamond_pickaxe 1")
    test_item(r"item @a + diamond_pickaxe 1",                    r"give @a minecraft:diamond_pickaxe 1")
    test_item(r"item @a + diamond_pickaxe[6]",                   r"give @a minecraft:diamond_pickaxe 1 6")
    test_item(r"item @a + diamond_pickaxe[6] 1",                 r"give @a minecraft:diamond_pickaxe 1 6")
    test_item(r'item @a + diamond_pickaxe{Unbreakable:1b}',      r'give @a minecraft:diamond_pickaxe 1 0 {Unbreakable:1b}')
    test_item(r'item @a + diamond_pickaxe{Unbreakable:1b} 1',    r'give @a minecraft:diamond_pickaxe 1 0 {Unbreakable:1b}')
    test_item(r'item @a + diamond_pickaxe[6]{Unbreakable:1b}',   r'give @a minecraft:diamond_pickaxe 1 6 {Unbreakable:1b}')
    test_item(r'item @a + diamond_pickaxe[6]{Unbreakable:1b} 1', r'give @a minecraft:diamond_pickaxe 1 6 {Unbreakable:1b}')

    test_item(r"item @a armor.head = diamond_pickaxe",                      r"replaceitem entity @a slot.armor.head minecraft:diamond_pickaxe 1")
    test_item(r"item @a armor.head = diamond_pickaxe 1",                    r"replaceitem entity @a slot.armor.head minecraft:diamond_pickaxe 1")
    test_item(r"item @a armor.head = diamond_pickaxe[6]",                   r"replaceitem entity @a slot.armor.head minecraft:diamond_pickaxe 1 6")
    test_item(r"item @a armor.head = diamond_pickaxe[6] 1",                 r"replaceitem entity @a slot.armor.head minecraft:diamond_pickaxe 1 6")
    test_item(r'item @a armor.head = diamond_pickaxe{Unbreakable:1b}',      r'replaceitem entity @a slot.armor.head minecraft:diamond_pickaxe 1 0 {Unbreakable:1b}')
    test_item(r'item @a armor.head = diamond_pickaxe{Unbreakable:1b} 1',    r'replaceitem entity @a slot.armor.head minecraft:diamond_pickaxe 1 0 {Unbreakable:1b}')
    test_item(r'item @a armor.head = diamond_pickaxe[6]{Unbreakable:1b}',   r'replaceitem entity @a slot.armor.head minecraft:diamond_pickaxe 1 6 {Unbreakable:1b}')
    test_item(r'item @a armor.head = diamond_pickaxe[6]{Unbreakable:1b} 1', r'replaceitem entity @a slot.armor.head minecraft:diamond_pickaxe 1 6 {Unbreakable:1b}')

    test_item(r"item ~ ~-1 ~ container.0 = diamond_pickaxe",                      r"replaceitem block ~ ~-1 ~ slot.container.0 minecraft:diamond_pickaxe 1")
    test_item(r"item ~ ~-1 ~ container.0 = diamond_pickaxe 1",                    r"replaceitem block ~ ~-1 ~ slot.container.0 minecraft:diamond_pickaxe 1")
    test_item(r"item ~ ~-1 ~ container.0 = diamond_pickaxe[6]",                   r"replaceitem block ~ ~-1 ~ slot.container.0 minecraft:diamond_pickaxe 1 6")
    test_item(r"item ~ ~-1 ~ container.0 = diamond_pickaxe[6] 1",                 r"replaceitem block ~ ~-1 ~ slot.container.0 minecraft:diamond_pickaxe 1 6")
    test_item(r'item ~ ~-1 ~ container.0 = diamond_pickaxe{Unbreakable:1b}',      r'replaceitem block ~ ~-1 ~ slot.container.0 minecraft:diamond_pickaxe 1 0 {Unbreakable:1b}')
    test_item(r'item ~ ~-1 ~ container.0 = diamond_pickaxe{Unbreakable:1b} 1',    r'replaceitem block ~ ~-1 ~ slot.container.0 minecraft:diamond_pickaxe 1 0 {Unbreakable:1b}')
    test_item(r'item ~ ~-1 ~ container.0 = diamond_pickaxe[6]{Unbreakable:1b}',   r'replaceitem block ~ ~-1 ~ slot.container.0 minecraft:diamond_pickaxe 1 6 {Unbreakable:1b}')
    test_item(r'item ~ ~-1 ~ container.0 = diamond_pickaxe[6]{Unbreakable:1b} 1', r'replaceitem block ~ ~-1 ~ slot.container.0 minecraft:diamond_pickaxe 1 6 {Unbreakable:1b}')

    # modifyitem
    r'''
    test_item("item @a armor.head ench = fire_aspect",        "modifyitem entity @a slot armor.head enchantment set fire_aspect 1")
    test_item("item @a armor.head ench = fire_aspect 1",      "modifyitem entity @a slot armor.head enchantment set fire_aspect 1")
    test_item("item @a armor.head ench + fire_aspect",        "modifyitem entity @a slot armor.head enchantment add fire_aspect 1")
    test_item("item @a armor.head ench + fire_aspect 1",      "modifyitem entity @a slot armor.head enchantment add fire_aspect 1")
    test_item("item @a armor.head ench - fire_aspect",        "modifyitem entity @a slot armor.head enchantment remove fire_aspect 1")
    test_item("item @a armor.head ench - fire_aspect 1",      "modifyitem entity @a slot armor.head enchantment remove fire_aspect 1")
    test_item("item @a armor.head ench - *",                  "modifyitem entity @a slot armor.head enchantment clear")

    test_item("item @a diamond_sword * ench = fire_aspect",   "modifyitem entity @a item minecraft:diamond_sword -1 enchantment set fire_aspect 1")
    test_item("item @a diamond_sword * ench = fire_aspect 1", "modifyitem entity @a item minecraft:diamond_sword -1 enchantment set fire_aspect 1")
    test_item("item @a diamond_sword * ench + fire_aspect",   "modifyitem entity @a item minecraft:diamond_sword -1 enchantment add fire_aspect 1")
    test_item("item @a diamond_sword * ench + fire_aspect 1", "modifyitem entity @a item minecraft:diamond_sword -1 enchantment add fire_aspect 1")
    test_item("item @a diamond_sword * ench - fire_aspect",   "modifyitem entity @a item minecraft:diamond_sword -1 enchantment remove fire_aspect 1")
    test_item("item @a diamond_sword * ench - fire_aspect 1", "modifyitem entity @a item minecraft:diamond_sword -1 enchantment remove fire_aspect 1")
    test_item("item @a diamond_sword * ench - *",             "modifyitem entity @a item minecraft:diamond_sword -1 enchantment clear")

    test_item("item @a diamond_sword 1 ench = fire_aspect",   "modifyitem entity @a item minecraft:diamond_sword 1 enchantment set fire_aspect 1")
    test_item("item @a diamond_sword 1 ench = fire_aspect 1", "modifyitem entity @a item minecraft:diamond_sword 1 enchantment set fire_aspect 1")
    test_item("item @a diamond_sword 1 ench + fire_aspect",   "modifyitem entity @a item minecraft:diamond_sword 1 enchantment add fire_aspect 1")
    test_item("item @a diamond_sword 1 ench + fire_aspect 1", "modifyitem entity @a item minecraft:diamond_sword 1 enchantment add fire_aspect 1")
    test_item("item @a diamond_sword 1 ench - fire_aspect",   "modifyitem entity @a item minecraft:diamond_sword 1 enchantment remove fire_aspect 1")
    test_item("item @a diamond_sword 1 ench - fire_aspect 1", "modifyitem entity @a item minecraft:diamond_sword 1 enchantment remove fire_aspect 1")

    test_item("item @a diamond_sword 1 ench - *",             "modifyitem entity @a item diamond_sword 1 enchantment clear")


    test_item("item @a armor.head dmg = 10", "modifyitem entity @a slot armor.head damage set 10")
    test_item("item @a armor.head dmg = 10", "modifyitem entity @a slot armor.head damage set 10")
    test_item("item @a armor.head dmg + 10", "modifyitem entity @a slot armor.head damage add 10")
    test_item("item @a armor.head dmg + 10", "modifyitem entity @a slot armor.head damage add 10")
    test_item("item @a armor.head dmg - 10", "modifyitem entity @a slot armor.head damage remove 10")
    test_item("item @a armor.head dmg - 10", "modifyitem entity @a slot armor.head damage remove 10")

    test_item("item @a diamond_sword * dmg = 10", "modifyitem entity @a item minecraft:diamond_sword -1 damage set 10")
    test_item("item @a diamond_sword * dmg = 10", "modifyitem entity @a item minecraft:diamond_sword -1 damage set 10")
    test_item("item @a diamond_sword * dmg + 10", "modifyitem entity @a item minecraft:diamond_sword -1 damage add 10")
    test_item("item @a diamond_sword * dmg + 10", "modifyitem entity @a item minecraft:diamond_sword -1 damage add 10")
    test_item("item @a diamond_sword * dmg - 10", "modifyitem entity @a item minecraft:diamond_sword -1 damage remove 10")
    test_item("item @a diamond_sword * dmg - 10", "modifyitem entity @a item minecraft:diamond_sword -1 damage remove 10")

    test_item("item @a diamond_sword 1 dmg = 10", "modifyitem entity @a item minecraft:diamond_sword 1 damage set 10")
    test_item("item @a diamond_sword 1 dmg = 10", "modifyitem entity @a item minecraft:diamond_sword 1 damage set 10")
    test_item("item @a diamond_sword 1 dmg + 10", "modifyitem entity @a item minecraft:diamond_sword 1 damage add 10")
    test_item("item @a diamond_sword 1 dmg + 10", "modifyitem entity @a item minecraft:diamond_sword 1 damage add 10")
    test_item("item @a diamond_sword 1 dmg - 10", "modifyitem entity @a item minecraft:diamond_sword 1 damage remove 10")
    test_item("item @a diamond_sword 1 dmg - 10", "modifyitem entity @a item minecraft:diamond_sword 1 damage remove 10")
    '''
