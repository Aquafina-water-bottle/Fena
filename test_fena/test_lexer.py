if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

import fena.logging_setup as logging_setup
logging_setup.format_file_name("test_lexer")

from test_fena.test_common import test_lexer

text = """

!mfunc outer:
    say outer

!mfunc "outer2":
    say outer2
"""

text2 = """\
!mfunc outer:
    say outer

!mfunc "outer2":
    say outer2"""

text3 = """\
            
!mfunc outer:
    say outer
            
            # hello
!mfunc "outer2":
    say outer2
        """

text4 = """\
!mfunc outer:
    say outer
!mfunc "outer2":
    say outer2
        # comment"""

text5 = """\
!mfunc ego:anvil_drop/test:
    say outer"""

text6 = """\
!mfunc "ego:anvil_drop/test":
    say outer"""

def test_lexers():
    test_lexer(text)
    test_lexer(text2)
    test_lexer(text3)
    test_lexer(text4)
    test_lexer(text5)
    test_lexer(text6)


if __name__ == "__main__":
    test_lexers()
