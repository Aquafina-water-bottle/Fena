import re
# rx_ENDING_INDENT = re.compile(r'((?:\n)[\t ]+)$')
rx_ENDING_INDENT = re.compile(r'\n[\t ]+$')

def test(string):
    search = re.search(rx_ENDING_INDENT, string)
    print(f"string={string!r}, search={search}, groups={'' if search is None else search.group()!r}")

test("test    ")
test("test\n")
test("test\n    ")
test("test\n\n    ")
test("test\n    \n")
test("test\n   \t ")
test("\n    test\n")


