if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fenalib.pre_pyexpander import parse_pre_pyexpander

input_str = """
# python code
$py(
code = "unchanged"
)

$py:
    idk = []

    for x in range(15):
        idk.append(x*2)

!mfunc hello
    $py:
        somedict = {}
        for x in range(15):
            somedict[x] = "ayylmao"

# macros
$macro(edit_give_porkchops):
    say this is a macro

$macro(unchanged)
    say this is an unchanged macro
$endmacro

# for loops as simple blocks
$for(x in range(5)):
    !mfunc give_porkchop_$(x)
        give @s minecraft:porkchop $(x)

!mfunc give_porkchops
    $for(x in range(5)):
        @s[porkchop=$(x)] function give_porkchop_$(x)

    $for(_ in range(3))
    $("say unchanged code")
    $endfor

!folder test
    $if(something == "test"):
        $for(x in range(5)):
            @s[porkchop=$(x)] function give_porkchop_$(x)

        $for(_ in range(3))
        $("say unchanged code")
        $endfor

# if/elif/else as compound block
$if(yo_mama == 1):
    !constobj Number

$elif(yo_mama == 2):
    !constobj constants

$else:
    !constobj g.constants

$if(yo_mama == 1)
!prefix unchanged
$elif(yo_mama == 2)
!prefix t2
$else
!prefix t3
$endif

!mfunc give_porkchops
    $for(x in range(5)):
        $if(x >= 3):
            replaceitem entity @s[porkchop=$(x)] slot.weapon.offhand porkchop 1 0
        $else:
            replaceitem entity @s[porkchop=$(x)] slot.hotbar.$(x) porkchop 1 0
"""

output_str = """$py(
code = "unchanged"
)
$py(
idk = []
for x in range(15):
    idk.append(x*2)
)
!mfunc hello
$py(
somedict = {}
for x in range(15):
    somedict[x] = "ayylmao"
)
$macro(edit_give_porkchops)
say this is a macro
$endmacro
$macro(unchanged)
    say this is an unchanged macro
$endmacro
$for(x in range(5))
!mfunc give_porkchop_$(x)
    give @s minecraft:porkchop $(x)
$endfor
!mfunc give_porkchops
    $for(x in range(5))
    @s[porkchop=$(x)] function give_porkchop_$(x)
    $endfor
    $for(_ in range(3))
    $("say unchanged code")
    $endfor
!folder test
    $if(something == "test")
    $for(x in range(5))
    @s[porkchop=$(x)] function give_porkchop_$(x)
    $endfor
    $for(_ in range(3))
    $("say unchanged code")
    $endfor
    $endif
$if(yo_mama == 1)
!constobj Number
$elif(yo_mama == 2)
!constobj constants
$else
!constobj g.constants
$endif
$if(yo_mama == 1)
!prefix unchanged
$elif(yo_mama == 2)
!prefix t2
$else
!prefix t3
$endif
!mfunc give_porkchops
    $for(x in range(5))
    $if(x >= 3)
    replaceitem entity @s[porkchop=$(x)] slot.weapon.offhand porkchop 1 0
    $else
    replaceitem entity @s[porkchop=$(x)] slot.hotbar.$(x) porkchop 1 0
    $endif
    $endfor
"""


def test_pre_pyexpander():
    assert output_str == parse_pre_pyexpander(input_str)

    # print(repr(parse_pre_expander(input_str)))
    # print(repr(output_str))
    # parser = Parser(input_str)
    # parsed_lines = parser.parse_lines()
    # parsed_lines = parse_pre_expander(input_str)
    # parsed_lines = list(parsed_lines)
    # expected_lines = output_str.splitlines()
    # assert len(parsed_lines) == len(expected_lines)
    # assert (parsed_lines) == (expected_lines)

    # for parsed_line, expected_line in zip(parsed_lines, expected_lines):
    #     print(parsed_line == expected_line, "" if parsed_line == expected_line else f"parsed_line={parsed_line!r}, expected_line={expected_line!r}")
    #     if not parsed_line == expected_line:
    #         raise SyntaxError(f"parsed_line={parsed_line!r}, expected_line={expected_line!r}")


if __name__ == "__main__":
    test_pre_pyexpander()

