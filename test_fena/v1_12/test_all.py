from test_fena.v1_12.test_selectors import test_selectors
from test_fena.v1_12.test_jsons import test_jsons
from test_fena.v1_12.test_nbts import test_nbts
from test_fena.v1_12.test_scoreboards import test_scoreboards
from test_fena.v1_12.test_blocks import test_blocks
from test_fena.v1_12.test_coords import test_coords
from test_fena.v1_12.test_executes import test_executes
from test_fena.v1_12.test_simple_cmds import test_simple_cmds
from test_fena.v1_12.test_datas import test_datas
from test_fena.v1_12.test_effects import test_effects
from test_fena.v1_12.test_items import test_items
from test_fena.v1_12.test_objectives import test_objectives
from test_fena.v1_12.test_teams import test_teams
from test_fena.v1_12.test_xps import test_xps

def test_all():
    test_selectors()
    test_jsons()
    test_nbts()
    test_scoreboards()
    test_blocks()
    test_coords()
    test_executes()
    test_simple_cmds()
    test_effects()
    test_datas()
    test_items()
    test_objectives()
    test_teams()
    test_xps()

