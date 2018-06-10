from test_fena.test_common import test_cmd

def test_executes():
    # selector -> as(selector) -> as selector
    test_cmd("@a: say test",         "execute as @a run say test")
    test_cmd("as(@a): say test",     "execute as @a run say test")

    # vec3 -> pos(vec3) -> positioned vec3
    test_cmd("1 1 1: say test",      "execute positioned 1 1 1 run say test")
    test_cmd("~ ~ ~: say test",      "execute positioned ~ ~ ~ run say test")
    test_cmd("^ ^ ^: say test",      "execute positioned ^ ^ ^ run say test")
    test_cmd("pos(1 1 1): say test", "execute positioned 1 1 1 run say test")
    test_cmd("pos(~ ~ ~): say test", "execute positioned ~ ~ ~ run say test")
    test_cmd("pos(^ ^ ^): say test", "execute positioned ^ ^ ^ run say test")
    test_cmd("pos(@a): say test",    "execute positioned as @a run say test")

    test_cmd("at(feet): say test", "execute anchored feet positioned ^ ^ ^ run say test")
    test_cmd("at(eyes): say test", "execute anchored eyes positioned ^ ^ ^ run say test")
    test_cmd("at(@a): say test",   "execute at @a run say test")

    test_cmd("at(x): say test",    "execute allign axes x run say test")
    test_cmd("at(y): say test",    "execute allign axes y run say test")
    test_cmd("at(z): say test",    "execute allign axes z run say test")
    test_cmd("at(xy): say test",   "execute allign axes xy run say test")
    test_cmd("at(xz): say test",   "execute allign axes xz run say test")
    test_cmd("at(yx): say test",   "execute allign axes yx run say test")
    test_cmd("at(yz): say test",   "execute allign axes yz run say test")
    test_cmd("at(zx): say test",   "execute allign axes zx run say test")
    test_cmd("at(zy): say test",   "execute allign axes zy run say test")
    test_cmd("at(xyz): say test",  "execute allign axes xyz run say test")
    test_cmd("at(xzy): say test",  "execute allign axes xzy run say test")
    test_cmd("at(yxz): say test",  "execute allign axes yxz run say test")
    test_cmd("at(yzx): say test",  "execute allign axes yzx run say test")
    test_cmd("at(zxy): say test",  "execute allign axes zxy run say test")
    test_cmd("at(zyx): say test",  "execute allign axes zyx run say test")
    test_cmd("at(a): say test",    expect_error=True) # invalid swizzles
    test_cmd("at(xyzx): say test", expect_error=True)
    test_cmd("at(xa): say test",   expect_error=True)

    # at(axes) -> align axes (axes = combination of xyz)
    # at(vec3 vec2) -> positioned vec3 facing vec2
    # facing(vec3) -> facing vec3
    # facing(selector) -> facing(selector feet) -> facing selector feet
    # facing(selector eyes) -> facing selector eyes
    # rot(selector) -> rotated as selector
    # rot(vec2) -> rotated vec2
    # anchor(feet) -> anchored feet
    # anchor(eyes) -> anchored eyes
    # in(dimension) -> in dimension
    # ast(selector) -> as selector at @s

"""
# all round brackets () are only used when:
# defining execute shortcut
# surrounding coords
# surrounding a selector argument value
# creating a selector group

# selector -> as(selector) -> as selector
# vec3 -> pos(vec3) -> positioned vec3
# pos(selector) -> positioned as selector
# at(feet) -> anchored feet positioned ^ ^ ^
# at(eyes) -> anchored eyes positioned ^ ^ ^
# at(selector) -> at selector
# at(axes) -> align axes (axes = combination of xyz)
# at(vec3 vec2) -> positioned vec3 facing vec2
# facing(vec3) -> facing vec3
# facing(selector) -> facing(selector feet) -> facing selector feet
# facing(selector eyes) -> facing selector eyes
# rot(selector) -> rotated as selector
# rot(vec2) -> rotated vec2
# anchor(feet) -> anchored feet
# anchor(eyes) -> anchored eyes
# in(dimension) -> in dimension
# ast(selector) -> as selector at @s

# if(selector) -> if entity selector
# if(block_type) -> if(block_type ~ ~ ~)
# if(block_type vec3) -> if block vec3 block_type
# if(vec3 vec3 == vec3) -> if(vec3 vec3 == vec3 all) -> if blocks vec3 vec3 vec3 all
# if(vec3 vec3 == vec3 masked) -> if blocks vec3 vec3 vec3 masked
# if(target objective operator target2 objective2) -> if score target objective operator target2 objective
# if(target objective == int) -> if score target objective matches int
# if(target objective == *) -> if score target objective matches -2147483648..
# if(target objective != int) -> unless(target objective == int)
# if(target objective < int) -> if score target objective matches ..(int-1)
# if(target objective <= int) -> if score target objective matches ..(int)
# if(target objective > int) -> if score target objective matches (int+1)..
# if(target objective >= int) -> if score target objective matches (int)..
# if(target objective in int..int) -> if score target objective matches int..int
# unless(...) -> ifnot(...) -> (Literally any if statement but replace "if" with "unless")

# note that auto_type = smallest stored value for integers, double when integer
# eg. 6 -> byte, 8234 -> short, 628137057 -> int, 2345766241356 -> long, 36.73461 and 5.0 -> double
# result(vec3 data_path scale) -> store result block vec3 data_path auto_type scale
# success(vec3 data_path scale) -> store success block vec3 data_path auto_type scale
# result(selector data_path scale) -> store result entity selector data_path auto_type scale
# success(selector data_path scale) -> store success entity selector data_path auto_type scale

# result(vec3 data_path type scale) -> store result block vec3 data_path type scale
# success(vec3 data_path type scale) -> store success block vec3 data_path type scale
# result(selector data_path type scale) -> store result entity selector data_path type scale
# success(selector data_path type scale) -> store success entity selector data_path type scale

# result(bossbar_id max) -> store result bossbar bossbar_id max
# result(bossbar_id value) -> store result bossbar bossbar_id value
# success(bossbar_id max) -> store success bossbar bossbar_id max
# success(bossbar_id value) -> store success bossbar bossbar_id value
# result(selector objective) -> store result score selector objective
# success(selector objective) -> store success score selector objective

!mfunc execute_test
    @p ~2 ~1 ~-1 at(@a) 3 5.2 -2 @s @r if(2 ~-1 ~ stone_brick) @e if(stone_brick): say @a
    
    # @s @r -> execute as @s as @r ...
    # pos(@p) -> execute positioned as @p ...
    # rot(@a) -> execute rotated as @a ...
    # 3 5.2 -2 -> execute positioned 3 5.2 -2 ...
    pos(@p) rot(@a) 3 5.2 -2 @s @r:

        # if(@a) -> execute if entity @a ...
        # if(stone_brick) -> execute if block ~ ~ ~ stone_brick ...
        # in(nether) -> execute in nether ...
        if(@a) if(stone_brick) @e in(nether): say @a
        if(@a, stone_brick) @e in(nether): say @a

        # if(@r _ti == @s _st) -> execute if score @r _ti = @s _st ...
        # if(stone_brick ~ ~-1 ~) -> execute if block ~ ~-1 ~ stone_brick
        # if(@r _ti == @s _st, stone_brick ~ ~-1 ~) -> execute if score @r _ti = @s _st if block ~ ~ ~ stone_brick ...
        # at(feet) -> execute anchored feet ...
        if(@r _ti == @s _st, stone_brick ~ ~-1 ~) at(feet): say @a
        
        # ifnot(stone_brick 2 3 4 3 4 5) -> execute unless block 2 3 4 3 4 5 stone_brick ...
        # at(@a) -> execute at @a ...
        ifnot(stone_brick 2 3 4 3 4 5) at(@a; feet): say @a

    # at(xy) -> execute align xy ...
    # facing(2 3 4) -> execute facing 2 3 4 ...
    # facing(@r) -> facing(@r feet) -> execute facing @r feet...
    # facing(@r eyes) -> execute facing @r eyes...
    at(xy) ~3 ~2 ~5 facing(2 3 4, @r feet, @r): say @a

    # rot(7, ~3) -> execute rotated 7 ~3 ...
    # ast(@s[_tag]) -> execute as @s[_tag] at @s ...
    # result(@s _af) -> execute store result score @s _af ...
    rot(7 ~3) ast(@s[_tag]) result(@s _af): say @a

    # note that some execute commands don't require a leading command to still be a functional command
    @a result(@s _pl) if(@e[type=pig])

    # and scoreboard shortcuts can start with selectors too
    @s _tp + 1

    # success(~ ~ ~ Items[0].Count 2) -> execute store success block ~ ~ ~ Items[0].Count byte 2 run ...
    success(~ ~ ~ Items[0].Count 2): say @a

    # automatically assigns the type
    # if there are no decimals, it assigns it to the lowest numeric type
    # if there are, it autmomatically assigns double precision
    # result(@s Attributes[0].Base 5) -> execute store result entity @s Attributes[0].Base byte 5 ...
    # result(@s Attributes[1].Base 2.5) -> execute store result entity @s Attributes[1].Base double 2.5 ...
    # result(@s Attributes[2].Base int 2.5) -> execute store result entity @s Attributes[1].Base int 2.5 ...
    result(@s Attributes[0].Base 5, @s Attributes[1].Base 2.5, @s Attributes[2].Base int 2.5): say @a

    # note that data merge requires the entire nbt tag, while execute store result entity just requires a position and integer
    # execute store result score @s a run data get entity @e[type=pig,limit=1] Attributes[0].Base 2
    # execute store result entity @e[type=pig,limit=1] Attributes[0].Base double 2 say @s

    # to store bossbar, note that we have to store either max or value too
    # result(minecraft:green max) -> execute store result bossbar minecraft:green max ...
    # success(idk value) -> execute store success bossbar minecraft:idk value ...


"""