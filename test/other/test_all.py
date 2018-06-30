from test_fena.other.test_pre_pyexpander import test_pre_pyexpander
from test_fena.test_common import test_cmd

def test_all():
    test_pre_pyexpander()
    test_cmd("tp @s ~ ~ ~", "minecraft:tp @s ~ ~ ~")
