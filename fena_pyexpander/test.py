if __name__ == "__main__":
    import sys
    sys.path.append("..")

import fena_pyexpander.lib as pyexpander

with open("test.txt") as file:
    text = file.read()

output = pyexpander.expandToStr(text, filename="test.txt", auto_indent=True, auto_indent_python=True)[0]
print(output)


