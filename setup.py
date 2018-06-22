
import os
from setuptools import setup

"""
Resourses:
    https://packaging.python.org/tutorials/packaging-projects/
    https://packaging.python.org/guides/distributing-packages-using-setuptools/

Examples:
    pylint: https://github.com/PyCQA/pylint/blob/master/setup.py
    pyexpander: https://bitbucket.org/goetzpf/pyexpander/src/b466de6fd801545650edfa790a18f022dc7e151a/setup.py?at=default&fileviewer=file-view-default
"""



# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# pylint: disable=bad-whitespace
setup(
    name = "fena",
    version = "0.0.4",
    author = "Austin Siew",
    author_email = "glowing.locker@gmail.com",
    description = ("Fena Preprocessor Language for Minecaft"),
    long_description = read('README'),
    long_description_content_type="text/markdown",
    license = "MIT",
    keywords = "minecaft language fena preprocessor",
    url = "https://github.com/Aquafina-water-bottle/Fena",
    # packages = ['fena', 'fena_pyexpander'],
    install_requires = ["pyexpander"],
    packages = ["fena"],
    scripts = ["fena.py"],
    classifiers = [
        "Development Status :: 3 - Alpha",
        'Natural Language :: English',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
)
