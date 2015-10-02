# -*- coding: utf-8 -*-
import ast
import re
from codecs import open
from os import path

from setuptools import setup, find_packages


"""
PyPI configuration module.

This is prepared for easing the generation of deployment files, offering the following features:

- No need to set up the packages
It will automatically search for source files inside the source folder, thanks to setuptools, removing the need of
manually configuring them.

- External version number
The version number will be read from the __init__.py file on the source files, meaning that it can be stored in a
clear and concrete place of the project.

- Long description created from the readme
The readme will be used for the long description. Meaning that the readme file should be written using restructured
text.

- Pypi required fields
All the fields required and used by Pypi are already included. Just fill them up as you need.

- Python 2 & 3
This setup module is prepared for both Python 2 and 3. Should work at least on the latest versions, and can be used
for preparing tox test executions.
"""

__license__ = 'MIT'
__version__ = '1.0.11'

# Regular expression for the version
_version_re = re.compile(r'__version__\s+=\s+(.*)')

# Test requirements
_tests_require = ['rdflib', 'pymongo']

# Path to the project's root
here = path.abspath(path.dirname(__file__))

# Gets the long description from the readme
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Gets the version for the source folder __init__.py file
with open('wmera/__init__.py', 'rb', encoding='utf-8') as f:
    version = f.read()
    version = _version_re.search(version).group(1)
    version = str(ast.literal_eval(version.rstrip()))

setup(
    name='wmera',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'data': ['data/*.csv', 'data/*.yml', 'data/*.xml'],
    },
    version=version,
    description='MERA',
    author='Dani F',
    author_email='author@domain.com',
    license='MIT',
    url='https://github.com/author/Project-Name',
    download_url='https://pypi.python.org/pypi/Project-Name',
    keywords=['keyword1', 'keyword2'],
    platforms='any',
    classifiers=['License :: OSI Approved :: MIT License', 
                 'Intended Audience :: Developers', 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules'],
    long_description=long_description,
    install_requires=[
        'rdflib',
		'pymongo'
    ],
    tests_require=_tests_require,
    extras_require={'test': _tests_require},
)