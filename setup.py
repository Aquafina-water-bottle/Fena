from setuptools import setup

from fenalib.general import semantic_version

"""
Resourses:
    https://pythonhosted.org/an_example_pypi_project/setuptools.html
    https://packaging.python.org/tutorials/packaging-projects/
    https://packaging.python.org/guides/distributing-packages-using-setuptools/

Examples:
    pylint: https://github.com/PyCQA/pylint/blob/master/setup.py
    pyexpander: https://bitbucket.org/goetzpf/pyexpander/src/b466de6fd801545650edfa790a18f022dc7e151a/setup.py?at=default&fileviewer=file-view-default

# update
python3 setup.py sdist bdist_wheel

# upload to testpypi
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# upload to regular pypi
twine upload dist/*

python3 -m pip install --user --index-url https://test.pypi.org/simple/ fena
python3 -m pip install --user fena
python3 -m pip install --user --upgrade fena
"""


setup(
    name="fena",
    version=semantic_version,
    author="Austin Siew",
    author_email="glowing.locker@gmail.com",
    description=("Fena Preprocessor Language for Minecaft"),
    keywords="minecaft language fena preprocessor",
    url="https://github.com/Aquafina-water-bottle/Fena",
    license='MIT',
    packages=["fenalib", "fena_pyexpander", "fenalib/config"],
    package_data={'fenalib/config': ["*.json", "*.ini"]},
    scripts=["fena.py"],
    install_requires=[
        'fenautils',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        'Natural Language :: English',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
)

