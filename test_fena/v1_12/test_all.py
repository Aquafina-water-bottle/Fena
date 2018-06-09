from test_fena.v1_12.test_selectors import test_selectors
from test_fena.v1_12.test_jsons import test_jsons
from test_fena.v1_12.test_nbts import test_nbts
from test_fena.v1_12.test_scoreboards import test_scoreboards

def test_all():
    test_selectors()
    test_jsons()
    test_nbts()
    test_scoreboards()