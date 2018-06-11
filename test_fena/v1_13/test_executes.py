from test_fena.test_common import test_cmd

def test_executes():
    # selector -> as(selector) -> as selector
    test_cmd("@a: say test",         "execute as @a run say test")
    test_cmd("as(@a): say test",     "execute as @a run say test")

    # vec3 -> pos(vec3) -> positioned vec3
    test_cmd("1 1 1: say test",      "execute positioned 1 1 1 run say test")
    test_cmd("~ ~ ~: say test",      "execute positioned ~ ~ ~ run say test")
    test_cmd("^ ^ ^: say test",      "execute positioned ^ ^ ^ run say test")

    # pos(selector) -> positioned as selector
    test_cmd("pos(1 1 1): say test", "execute positioned 1 1 1 run say test")
    test_cmd("pos(~ ~ ~): say test", "execute positioned ~ ~ ~ run say test")
    test_cmd("pos(^ ^ ^): say test", "execute positioned ^ ^ ^ run say test")
    test_cmd("pos(@a): say test",    "execute positioned as @a run say test")

    # at(feet) -> anchored feet positioned ^ ^ ^
    # at(eyes) -> anchored eyes positioned ^ ^ ^
    # at(selector) -> at selector
    # at(vec3 vec2) -> positioned vec3 facing vec2
    test_cmd("at(feet): say test",      "execute anchored feet positioned ^ ^ ^ run say test")
    test_cmd("at(eyes): say test",      "execute anchored eyes positioned ^ ^ ^ run say test")
    test_cmd("at(@a): say test",        "execute at @a run say test")
    test_cmd("at(1 2 3 4 5): say test", "execute positioned 1 2 3 facing 4 5 run say test")
    test_cmd("at(1 2 3 4): say test",   expect_error=True) # invalid coords
    test_cmd("at(1 2 3): say test",     expect_error=True)

    # at(axes) -> align axes (axes = combination of xyz)
    test_cmd("at(x): say test",    "execute align x run say test")
    test_cmd("at(y): say test",    "execute align y run say test")
    test_cmd("at(z): say test",    "execute align z run say test")
    test_cmd("at(xy): say test",   "execute align xy run say test")
    test_cmd("at(xz): say test",   "execute align xz run say test")
    test_cmd("at(yx): say test",   "execute align yx run say test")
    test_cmd("at(yz): say test",   "execute align yz run say test")
    test_cmd("at(zx): say test",   "execute align zx run say test")
    test_cmd("at(zy): say test",   "execute align zy run say test")
    test_cmd("at(xyz): say test",  "execute align xyz run say test")
    test_cmd("at(xzy): say test",  "execute align xzy run say test")
    test_cmd("at(yxz): say test",  "execute align yxz run say test")
    test_cmd("at(yzx): say test",  "execute align yzx run say test")
    test_cmd("at(zxy): say test",  "execute align zxy run say test")
    test_cmd("at(zyx): say test",  "execute align zyx run say test")
    test_cmd("at(a): say test",    expect_error=True) # invalid swizzles
    test_cmd("at(xyzx): say test", expect_error=True)
    test_cmd("at(xa): say test",   expect_error=True)

    # facing(vec3) -> facing vec3
    # facing(selector) -> facing(selector feet) -> facing selector feet
    # facing(selector eyes) -> facing selector eyes
    test_cmd("facing(@r): say test",      "execute facing entity @r feet run say test")
    test_cmd("facing(~ ~): say test",     expect_error=True) # invalid coords
    test_cmd("facing(~ ~ ~): say test",   "execute facing ~ ~ ~ run say test")
    test_cmd("facing(@r feet): say test", "execute facing entity @r feet run say test")
    test_cmd("facing(@r eyes): say test", "execute facing entity @r eyes run say test")
    test_cmd("facing(@r nou): say test",  expect_error=True) # invalid position

    # rot(selector) -> rotated as selector
    # rot(vec2) -> rotated vec2
    test_cmd("rot(@r): say test",    "execute rotated as @r run say test")
    test_cmd("rot(~ ~): say test",   "execute rotated ~ ~ run say test")
    test_cmd("rot(~ ~ ~): say test", expect_error=True) # too many coords

    # anchor(feet) -> anchored feet
    # anchor(eyes) -> anchored eyes
    test_cmd("anchor(feet): say test", "execute anchored feet run say test")
    test_cmd("anchor(eyes): say test", "execute anchored eyes run say test")
    test_cmd("anchor(nou): say test",  expect_error=True) # not "feet" or "eyes"

    # in(dimension) -> in dimension
    test_cmd("in(overworld): say test",  "execute in overworld run say test")
    test_cmd("in(nether): say test",     "execute in the_nether run say test")
    test_cmd("in(the_nether): say test", "execute in the_nether run say test")
    test_cmd("in(end): say test",        "execute in the_end run say test")
    test_cmd("in(the_end): say test",    "execute in the_end run say test")
    test_cmd("in(the_nou): say test",    expect_error=True) # invalid dimensions
    test_cmd("in(nou): say test",    expect_error=True)

    # ast(selector) -> as selector at @s
    test_cmd("ast(@r): say test",  "execute as @r at @s run say test")
    test_cmd("ast(nou): say test", expect_error=True) # invalid selectors
    test_cmd("ast(1): say test",   expect_error=True)


    # if(selector) -> if entity selector
    # if(block_type) -> if(~ ~ ~ block_type)
    # if(block_type vec3) -> if block vec3 block_type
    test_cmd("if(@r): say test",                   "execute if entity @r run say test")
    test_cmd("if(nou): say test",                  expect_error=True)
    test_cmd("if(stone_bricks): say test",         "execute if block ~ ~ ~ minecraft:stone_bricks run say test")
    test_cmd("if(stone_bricks ~ ~-1 ~): say test", "execute if block ~ ~-1 ~ minecraft:stone_bricks run say test")

    # if(vec3 vec3 == vec3) -> if(vec3 vec3 == vec3 all) -> if blocks vec3 vec3 vec3 all
    # if(vec3 vec3 == vec3 masked) -> if blocks vec3 vec3 vec3 masked
    test_cmd("if(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498): say test",        "execute if blocks ~1 ~1 ~1 ~-1 ~-1 ~-1 252 12 -498 all run say test")
    test_cmd("if(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498 all): say test",    "execute if blocks ~1 ~1 ~1 ~-1 ~-1 ~-1 252 12 -498 all run say test")
    test_cmd("if(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498 masked): say test", "execute if blocks ~1 ~1 ~1 ~-1 ~-1 ~-1 252 12 -498 masked run say test")
    test_cmd("if(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498 nou): say test",    expect_error=True) # not "masked" or "all"

    # if(target objective operator target2 objective2) -> if score target objective operator target2 objective
    test_cmd("if(@s _pl = @r _pl): say test",    "execute if score @s fena.pl = @r fena.pl run say test")
    test_cmd("if(@s _pl == @r _pl): say test",   "execute if score @s fena.pl = @r fena.pl run say test")
    test_cmd("if(@s _pl < @r _pl): say test",    "execute if score @s fena.pl < @r fena.pl run say test")
    test_cmd("if(@s _pl > @r _pl): say test",    "execute if score @s fena.pl > @r fena.pl run say test")
    test_cmd("if(@s _pl <= @r _pl): say test",   "execute if score @s fena.pl <= @r fena.pl run say test")
    test_cmd("if(@s _pl >= @r _pl): say test",   "execute if score @s fena.pl >= @r fena.pl run say test")
    test_cmd("if(@s _pl asdf @r _pl): say test", expect_error=True) # invalid operator

    # if(target objective == *) -> if score target objective matches -2147483648..
    # if(target objective == int) -> if score target objective matches int
    test_cmd("if(@s _pl == *): say test", "execute if score @s fena.pl matches -2147483648.. run say test")
    test_cmd("if(@s _pl == 0): say test", "execute if score @s fena.pl matches 0 run say test")
    test_cmd("if(@s _pl == a): say test", expect_error=True) # invalid number

    # if(target objective < int) -> if score target objective matches ..(int-1)
    # if(target objective <= int) -> if score target objective matches ..(int)
    # if(target objective > int) -> if score target objective matches (int+1)..
    # if(target objective >= int) -> if score target objective matches (int)..
    test_cmd("if(@s _pl < 0): say test",  "execute if score @s fena.pl matches ..-1 run say test")
    test_cmd("if(@s _pl <= 0): say test", "execute if score @s fena.pl matches ..0 run say test")
    test_cmd("if(@s _pl > 0): say test",  "execute if score @s fena.pl matches 1.. run say test")
    test_cmd("if(@s _pl >= 0): say test", "execute if score @s fena.pl matches 0.. run say test")

    # if(target objective in int..int) -> if score target objective matches int..int
    test_cmd("if(@s _pl in 0..1): say test", "execute if score @s fena.pl matches 0..1 run say test")


    # unless(selector) -> unless entity selector
    # unless(block_type) -> unless(~ ~ ~ block_type)
    # unless(block_type vec3) -> unless block vec3 block_type
    test_cmd("unless(@r): say test",                   "execute unless entity @r run say test")
    test_cmd("unless(nou): say test",                  expect_error=True)
    test_cmd("unless(stone_bricks): say test",         "execute unless block ~ ~ ~ minecraft:stone_bricks run say test")
    test_cmd("unless(stone_bricks ~ ~-1 ~): say test", "execute unless block ~ ~-1 ~ minecraft:stone_bricks run say test")

    # unless(vec3 vec3 == vec3) -> unless(vec3 vec3 == vec3 all) -> unless blocks vec3 vec3 vec3 all
    # unless(vec3 vec3 == vec3 masked) -> unless blocks vec3 vec3 vec3 masked
    test_cmd("unless(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498): say test",        "execute unless blocks ~1 ~1 ~1 ~-1 ~-1 ~-1 252 12 -498 all run say test")
    test_cmd("unless(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498 all): say test",    "execute unless blocks ~1 ~1 ~1 ~-1 ~-1 ~-1 252 12 -498 all run say test")
    test_cmd("unless(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498 masked): say test", "execute unless blocks ~1 ~1 ~1 ~-1 ~-1 ~-1 252 12 -498 masked run say test")
    test_cmd("unless(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498 nou): say test",    expect_error=True) # not "masked" or "all"

    # unless(target objective operator target2 objective2) -> unless score target objective operator target2 objective
    test_cmd("unless(@s _pl = @r _pl): say test",    "execute unless score @s fena.pl = @r fena.pl run say test")
    test_cmd("unless(@s _pl == @r _pl): say test",   "execute unless score @s fena.pl = @r fena.pl run say test")
    test_cmd("unless(@s _pl < @r _pl): say test",    "execute unless score @s fena.pl < @r fena.pl run say test")
    test_cmd("unless(@s _pl > @r _pl): say test",    "execute unless score @s fena.pl > @r fena.pl run say test")
    test_cmd("unless(@s _pl <= @r _pl): say test",   "execute unless score @s fena.pl <= @r fena.pl run say test")
    test_cmd("unless(@s _pl >= @r _pl): say test",   "execute unless score @s fena.pl >= @r fena.pl run say test")
    test_cmd("unless(@s _pl asdf @r _pl): say test", expect_error=True) # invalid operator

    # unless(target objective == *) -> unless score target objective matches -2147483648..
    # unless(target objective == int) -> unless score target objective matches int
    test_cmd("unless(@s _pl == *): say test", "execute unless score @s fena.pl matches -2147483648.. run say test")
    test_cmd("unless(@s _pl == 0): say test", "execute unless score @s fena.pl matches 0 run say test")
    test_cmd("unless(@s _pl == a): say test", expect_error=True) # invalid number

    # unless(target objective < int) -> unless score target objective matches ..(int-1)
    # unless(target objective <= int) -> unless score target objective matches ..(int)
    # unless(target objective > int) -> unless score target objective matches (int+1)..
    # unless(target objective >= int) -> unless score target objective matches (int)..
    test_cmd("unless(@s _pl < 0): say test",  "execute unless score @s fena.pl matches ..-1 run say test")
    test_cmd("unless(@s _pl <= 0): say test", "execute unless score @s fena.pl matches ..0 run say test")
    test_cmd("unless(@s _pl > 0): say test",  "execute unless score @s fena.pl matches 1.. run say test")
    test_cmd("unless(@s _pl >= 0): say test", "execute unless score @s fena.pl matches 0.. run say test")

    # unless(target objective in int..int) -> unless score target objective matches int..int
    test_cmd("unless(@s _pl in 0..1): say test", "execute unless score @s fena.pl matches 0..1 run say test")


    # ifnot(selector) -> unless entity selector
    # ifnot(block_type) -> ifnot(~ ~ ~ block_type)
    # ifnot(block_type vec3) -> unless block vec3 block_type
    test_cmd("ifnot(@r): say test",                   "execute unless entity @r run say test")
    test_cmd("ifnot(nou): say test",                  expect_error=True)
    test_cmd("ifnot(stone_bricks): say test",         "execute unless block ~ ~ ~ minecraft:stone_bricks run say test")
    test_cmd("ifnot(stone_bricks ~ ~-1 ~): say test", "execute unless block ~ ~-1 ~ minecraft:stone_bricks run say test")

    # ifnot(vec3 vec3 == vec3) -> ifnot(vec3 vec3 == vec3 all) -> unless blocks vec3 vec3 vec3 all
    # ifnot(vec3 vec3 == vec3 masked) -> unless blocks vec3 vec3 vec3 masked
    test_cmd("ifnot(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498): say test",        "execute unless blocks ~1 ~1 ~1 ~-1 ~-1 ~-1 252 12 -498 all run say test")
    test_cmd("ifnot(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498 all): say test",    "execute unless blocks ~1 ~1 ~1 ~-1 ~-1 ~-1 252 12 -498 all run say test")
    test_cmd("ifnot(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498 masked): say test", "execute unless blocks ~1 ~1 ~1 ~-1 ~-1 ~-1 252 12 -498 masked run say test")
    test_cmd("ifnot(~1 ~1 ~1 ~-1 ~-1 ~-1 == 252 12 -498 nou): say test",    expect_error=True) # not "masked" or "all"

    # ifnot(target objective operator target2 objective2) -> unless score target objective operator target2 objective
    test_cmd("ifnot(@s _pl = @r _pl): say test",    "execute unless score @s fena.pl = @r fena.pl run say test")
    test_cmd("ifnot(@s _pl == @r _pl): say test",   "execute unless score @s fena.pl = @r fena.pl run say test")
    test_cmd("ifnot(@s _pl < @r _pl): say test",    "execute unless score @s fena.pl < @r fena.pl run say test")
    test_cmd("ifnot(@s _pl > @r _pl): say test",    "execute unless score @s fena.pl > @r fena.pl run say test")
    test_cmd("ifnot(@s _pl <= @r _pl): say test",   "execute unless score @s fena.pl <= @r fena.pl run say test")
    test_cmd("ifnot(@s _pl >= @r _pl): say test",   "execute unless score @s fena.pl >= @r fena.pl run say test")
    test_cmd("ifnot(@s _pl asdf @r _pl): say test", expect_error=True) # invalid operator

    # ifnot(target objective == *) -> unless score target objective matches -2147483648..
    # ifnot(target objective == int) -> unless score target objective matches int
    test_cmd("ifnot(@s _pl == *): say test", "execute unless score @s fena.pl matches -2147483648.. run say test")
    test_cmd("ifnot(@s _pl == 0): say test", "execute unless score @s fena.pl matches 0 run say test")
    test_cmd("ifnot(@s _pl == a): say test", expect_error=True) # invalid number

    # ifnot(target objective < int) -> unless score target objective matches ..(int-1)
    # ifnot(target objective <= int) -> unless score target objective matches ..(int)
    # ifnot(target objective > int) -> unless score target objective matches (int+1)..
    # ifnot(target objective >= int) -> unless score target objective matches (int)..
    test_cmd("ifnot(@s _pl < 0): say test",  "execute unless score @s fena.pl matches ..-1 run say test")
    test_cmd("ifnot(@s _pl <= 0): say test", "execute unless score @s fena.pl matches ..0 run say test")
    test_cmd("ifnot(@s _pl > 0): say test",  "execute unless score @s fena.pl matches 1.. run say test")
    test_cmd("ifnot(@s _pl >= 0): say test", "execute unless score @s fena.pl matches 0.. run say test")

    # ifnot(target objective in int..int) -> unless score target objective matches int..int
    test_cmd("ifnot(@s _pl in 0..1): say test", "execute unless score @s fena.pl matches 0..1 run say test")


    # result(vec3 data_path scale) -> store result block vec3 data_path long scale
    # result(vec3 data_path type scale) -> store result block vec3 data_path type scale
    test_cmd("result(~ ~-1 ~ Items[0].Count 1): say test",      "execute store result block ~ ~-1 ~ Items[0].Count long 1 run say test")
    test_cmd("result(~ ~-1 ~ Items 1): say test",               "execute store result block ~ ~-1 ~ Items long 1 run say test")
    test_cmd("result(~ ~-1 ~ Items[0].Count int 1): say test",  "execute store result block ~ ~-1 ~ Items[0].Count int 1 run say test")
    test_cmd("result(~ ~-1 ~ Items int 1): say test",           "execute store result block ~ ~-1 ~ Items int 1 run say test")
    test_cmd("result(~ ~-1 ~ Items[0].Count 1.1): say test",      "execute store result block ~ ~-1 ~ Items[0].Count double 1.1 run say test")
    test_cmd("result(~ ~-1 ~ Items 1.1): say test",               "execute store result block ~ ~-1 ~ Items double 1.1 run say test")
    test_cmd("result(~ ~-1 ~ Items[0].Count int 1.1): say test",  "execute store result block ~ ~-1 ~ Items[0].Count int 1.1 run say test")
    test_cmd("result(~ ~-1 ~ Items int 1.1): say test",           "execute store result block ~ ~-1 ~ Items int 1.1 run say test")

    # result(selector data_path scale) -> store result entity selector data_path long scale
    # result(selector data_path type scale) -> store result entity selector data_path type scale
    test_cmd("result(@s Attributes[0].Name 1): say test",       "execute store result entity @s Attributes[0].Name long 1 run say test")
    test_cmd("result(@s Invulnerable 1): say test",             "execute store result entity @s Invulnerable long 1 run say test")
    test_cmd("result(@s Attributes[0].Name int 1): say test",   "execute store result entity @s Attributes[0].Name int 1 run say test")
    test_cmd("result(@s Invulnerable int 1): say test",         "execute store result entity @s Invulnerable int 1 run say test")
    test_cmd("result(@s Attributes[0].Name 1.1): say test",     "execute store result entity @s Attributes[0].Name double 1.1 run say test")
    test_cmd("result(@s Invulnerable 1.1): say test",           "execute store result entity @s Invulnerable double 1.1 run say test")
    test_cmd("result(@s Attributes[0].Name int 1.1): say test", "execute store result entity @s Attributes[0].Name int 1.1 run say test")
    test_cmd("result(@s Invulnerable int 1.1): say test",       "execute store result entity @s Invulnerable int 1.1 run say test")

    # result(bossbar_id max) -> store result bossbar bossbar_id max
    # result(bossbar_id value) -> store result bossbar bossbar_id value
    test_cmd("result(_xp max): say test",   "execute store result bossbar minecraft:fena.xp max run say test")
    test_cmd("result(_xp value): say test", "execute store result bossbar minecraft:fena.xp value run say test")

    # result(target objective) -> store result score target objective
    test_cmd("result(@s _pl): say test",  "execute store result score @s fena.pl run say test")
    test_cmd("result(target _pl): say test",  "execute store result score target fena.pl run say test")

    # note that whether it's storing a bossbar is determined primarly by if the objective is 'max' or 'value
    test_cmd("result(_xp nou): say test", "execute store result score _xp nou run say test")


    # success(vec3 data_path scale) -> store success block vec3 data_path long scale
    # success(vec3 data_path type scale) -> store success block vec3 data_path type scale
    test_cmd("success(~ ~-1 ~ Items[0].Count 1): say test",      "execute store success block ~ ~-1 ~ Items[0].Count long 1 run say test")
    test_cmd("success(~ ~-1 ~ Items 1): say test",               "execute store success block ~ ~-1 ~ Items long 1 run say test")
    test_cmd("success(~ ~-1 ~ Items[0].Count int 1): say test",  "execute store success block ~ ~-1 ~ Items[0].Count int 1 run say test")
    test_cmd("success(~ ~-1 ~ Items int 1): say test",           "execute store success block ~ ~-1 ~ Items int 1 run say test")
    test_cmd("success(~ ~-1 ~ Items[0].Count 1.1): say test",      "execute store success block ~ ~-1 ~ Items[0].Count double 1.1 run say test")
    test_cmd("success(~ ~-1 ~ Items 1.1): say test",               "execute store success block ~ ~-1 ~ Items double 1.1 run say test")
    test_cmd("success(~ ~-1 ~ Items[0].Count int 1.1): say test",  "execute store success block ~ ~-1 ~ Items[0].Count int 1.1 run say test")
    test_cmd("success(~ ~-1 ~ Items int 1.1): say test",           "execute store success block ~ ~-1 ~ Items int 1.1 run say test")

    # success(selector data_path scale) -> store success entity selector data_path long scale
    # success(selector data_path type scale) -> store success entity selector data_path type scale
    test_cmd("success(@s Attributes[0].Name 1): say test",       "execute store success entity @s Attributes[0].Name long 1 run say test")
    test_cmd("success(@s Invulnerable 1): say test",             "execute store success entity @s Invulnerable long 1 run say test")
    test_cmd("success(@s Attributes[0].Name int 1): say test",   "execute store success entity @s Attributes[0].Name int 1 run say test")
    test_cmd("success(@s Invulnerable int 1): say test",         "execute store success entity @s Invulnerable int 1 run say test")
    test_cmd("success(@s Attributes[0].Name 1.1): say test",     "execute store success entity @s Attributes[0].Name double 1.1 run say test")
    test_cmd("success(@s Invulnerable 1.1): say test",           "execute store success entity @s Invulnerable double 1.1 run say test")
    test_cmd("success(@s Attributes[0].Name int 1.1): say test", "execute store success entity @s Attributes[0].Name int 1.1 run say test")
    test_cmd("success(@s Invulnerable int 1.1): say test",       "execute store success entity @s Invulnerable int 1.1 run say test")

    # success(bossbar_id max) -> store success bossbar bossbar_id max
    # success(bossbar_id value) -> store success bossbar bossbar_id value
    test_cmd("success(_xp max): say test",   "execute store success bossbar minecraft:fena.xp max run say test")
    test_cmd("success(_xp value): say test", "execute store success bossbar minecraft:fena.xp value run say test")

    # success(target objective) -> store success score target objective
    test_cmd("success(@s _pl): say test",  "execute store success score @s fena.pl run say test")
    test_cmd("success(target _pl): say test",  "execute store success score target fena.pl run say test")

    # note that whether it's storing a bossbar is determined primarly by if the objective is 'max' or 'value
    test_cmd("success(_xp nou): say test", "execute store success score _xp nou run say test")


    test_cmd(
        "@p ~2 ~1 ~-1 at(@a) 3 5.2 -2 @s @r if(stone_bricks 2 ~-1 ~) @e if(stone_bricks): say @a",
        "execute as @p positioned ~2 ~1 ~-1 at @a positioned 3 5.2 -2 as @s as @r if block 2 ~-1 ~ minecraft:stone_bricks as @e if block ~ ~ ~ minecraft:stone_bricks run say @a"
    )

    test_cmd("pos(@p) rot(@s) 3 5.2 -2 @s @r", "execute positioned as @p rotated as @s positioned 3 5.2 -2 as @s as @r")

    test_cmd(
        "if(@a) if(stone_bricks) @e in(nether): say @a",
        "execute if entity @a if block ~ ~ ~ minecraft:stone_bricks as @e in the_nether run say @a"
        )

    test_cmd(
        "if(@a, minecraft:stone_bricks) @e in(nether): say @a",
        "execute if entity @a if block ~ ~ ~ minecraft:stone_bricks as @e in the_nether run say @a"
        )

    test_cmd(
        "if(@r _ti == @s _st, stone_bricks ~ ~-1 ~) at(feet): say @a",
        "execute if score @r fena.ti = @s fena.st if block ~ ~-1 ~ minecraft:stone_bricks anchored feet positioned ^ ^ ^ run say @a"
    )

    test_cmd(
        "ifnot(2 3 4 3 4 5 == ~1 ~1 ~1) at(@a, feet): say @a",
        "execute unless blocks 2 3 4 3 4 5 ~1 ~1 ~1 all at @a anchored feet positioned ^ ^ ^ run say @a"
    )

    test_cmd(
        "at(xy) ~3 ~2 ~5 facing(2 3 4, @r feet, @r): say @a",
        "execute align xy positioned ~3 ~2 ~5 facing 2 3 4 facing entity @r feet facing entity @r feet run say @a"
    )

    # note that some execute commands don't require a leading command to still be a functional command
    test_cmd(
        "@a result(@s _pl) if(@e[type=pig])",
        "execute as @a store result score @s fena.pl if entity @e[type=minecraft:pig]"
    )

    test_cmd(
        "success(~ ~ ~ Items[0].Count 2): say @a",
        "execute store success block ~ ~ ~ Items[0].Count long 2 run say @a"
    )

    test_cmd(
        "result(@s Attributes[0].Base 5, @s Attributes[1].Base 2.5, @s Attributes[2].Base int 2.5): say @a",
        "execute store result entity @s Attributes[0].Base long 5 store result entity @s Attributes[1].Base double 2.5 store result entity @s Attributes[2].Base int 2.5 run say @a"
    )
