from test_fena.test_common import test_cmd

def test_simple_cmds():
    test_cmd(r'bossbar add test {"text":"test"}', expect_error=True) # not under command_names.json

