if __name__ == "__main__":
    import sys
    sys.path.append("../..")
    del sys

from test_fena.test_common import test_selector

test_selector("@a[obj=25,obj=24]", expect_error=True)
