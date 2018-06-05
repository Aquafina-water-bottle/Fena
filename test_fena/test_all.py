if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

import test_fena.v1_12.test_all
import test_fena.v1_13.test_all

from fena.config_data import get_all_data

get_all_data("1.12")
test_fena.v1_12.test_all.test_all()

get_all_data("1.13")
test_fena.v1_13.test_all.test_all()