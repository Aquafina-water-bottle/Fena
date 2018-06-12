from test_fena.v1_13.test_selectors import test_selectors
from test_fena.v1_13.test_jsons import test_jsons
from test_fena.v1_12.test_nbts import test_nbts
from test_fena.v1_13.test_scoreboards import test_scoreboards
from test_fena.v1_13.test_coords import test_coords
from test_fena.v1_13.test_blocks import test_blocks
from test_fena.v1_13.test_data_paths import test_data_paths
from test_fena.v1_13.test_executes import test_executes
from test_fena.v1_13.test_bossbars import test_bossbars
from test_fena.v1_13.test_datas import test_datas
from test_fena.v1_13.test_effects import test_effects

def test_all():
    test_selectors()
    test_jsons()
    test_nbts()  # nbt is the same for 1.12 and 1.13
    test_scoreboards()
    test_blocks()
    test_coords()
    test_data_paths()
    test_executes()
    test_bossbars()
    test_datas()
    test_effects()
