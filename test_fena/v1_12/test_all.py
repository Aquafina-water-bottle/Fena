from test_fena.v1_12.test_selectors import test_selectors
from test_fena.v1_12.test_jsons import test_jsons
from test_fena.v1_12.test_nbts import test_nbts
from test_fena.v1_12.test_scoreboards import test_scoreboards
from test_fena.v1_12.test_blocks import test_blocks
from test_fena.v1_12.test_executes import test_executes
from test_fena.v1_12.test_coords import test_coords

def test_all():
    test_selectors()
    test_jsons()
    test_nbts()
    test_scoreboards()
    test_blocks()
    test_blocks()
    test_coords()