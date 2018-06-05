from test_fena.v1_12.test_selectors import test_selectors
from test_fena.v1_12.test_jsons import test_jsons

def test_all():
    test_selectors()
    test_jsons()