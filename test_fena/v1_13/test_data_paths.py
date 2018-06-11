from test_fena.test_common import test_data_path

def test_data_paths():
    test_data_path("Invulnerable")
    test_data_path("Test[0][1][2]")
    test_data_path("Test[0].Test[1].Test[2]")
    test_data_path("Test.Test.Test")
    test_data_path("Test.Test.", expect_error=True)
    test_data_path("Test.Test.[0]", expect_error=True)
    test_data_path("Test.Test.[0]", expect_error=True)
    test_data_path("Test,Test", expect_error=True)
    test_data_path("Test[0", expect_error=True)
    test_data_path("[0]", expect_error=True)
    test_data_path(".", expect_error=True)