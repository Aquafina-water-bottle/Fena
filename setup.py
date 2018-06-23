import os
from setuptools import setup

"""
Resourses:
    https://pythonhosted.org/an_example_pypi_project/setuptools.html
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
    with open(os.path.join(os.path.dirname(__file__), fname)) as file:
        string = file.read()
    return string


setup(
    name="fena",
    version="0.0.4",
    author="Austin Siew",
    author_email="glowing.locker@gmail.com",
    description=("Fena Preprocessor Language for Minecaft"),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    keywords="minecaft language fena preprocessor",
    url="https://github.com/Aquafina-water-bottle/Fena",
    # packages=['fena', 'fena_pyexpander'],
    install_requires=["pyexpander"],
    packages=["fenalib"],
    scripts=["fena.py"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Natural Language :: English',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
)

