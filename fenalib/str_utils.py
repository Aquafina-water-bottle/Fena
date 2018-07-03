"""
Simply provides the encode/decode function to turn a literal string into a regular string and back
"""

import codecs

def decode_str(string):
    """
    Examples:
        >>> decode_str(r'"hello"')
        'hello'
        >>> decode_str(r'""')
        ''
        >>> decode_str(r'"\\x89\\t"')
        '\\x89\\t'

        >>> decode_str(r'')
        Traceback (most recent call last):
            ...
        SyntaxError: Expected the string '' to be longer than two characters so it can begin and end with a quotation

        >>> decode_str(r'hello')
        Traceback (most recent call last):
            ...
        SyntaxError: Expected the string 'hello' to begin with a quotation

        >>> decode_str(r'"hello')
        Traceback (most recent call last):
            ...
        SyntaxError: Expected the string '"hello' to end with a quotation
    """
    if not len(string) >= 2:
        raise SyntaxError(f"Expected the string {string!r} to be longer than two characters so it can begin and end with a quotation")
    if not string.startswith('"'):
        raise SyntaxError(f"Expected the string {string!r} to begin with a quotation")
    if not string.endswith('"'):
        raise SyntaxError(f"Expected the string {string!r} to end with a quotation")

    return codecs.decode(string[1:-1], "unicode_escape")

def encode_str(string):
    """
    Examples:
        >>> encode_str('hello')
        '"hello"'
        >>> encode_str('\\x89\\t')
        '"\\\\x89\\\\t"'
    """
    return '"' + codecs.encode(string, "unicode_escape").decode("utf-8").replace('"', r'\"') + '"'

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print(encode_str(r'{CustomName:"{\"text\":\"test\"}"}'))
    print(encode_str(r'{CustomName:"\n"}'))
    print(decode_str(r'"{CustomName:\"\\n\"}"'))
    print(encode_str(decode_str(r'"{CustomName:\"\\n\"}"')))


