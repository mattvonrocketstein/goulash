#!/usr/bin/env python
""" setup.py for goulash
"""

import os, sys
from setuptools import setup

# make sure that finding packages works, even
# when setup.py is invoked from outside this dir
this_dir = os.path.dirname(os.path.abspath(__file__))
if not os.getcwd()==this_dir:
    os.chdir(this_dir)

# make sure we can import the version number so that it doesn't have
# to be changed in two places. goulash/__init__.py is also free
# to import various requirements that haven't been installed yet
sys.path.append(os.path.join(this_dir, 'goulash'))
from version import __version__
sys.path.pop()

base_url = 'https://github.com/mattvonrocketstein/goulash/'
setup(
    name         = 'goulash',
    version      = __version__,
    description  = 'toolbox, random shared stuff from my other projects',
    author       = 'mattvonrocketstein',
    author_email = '$author@gmail',
    url          = base_url,
    download_url = base_url + '/tarball/master',
    packages     = ['goulash'],
    keywords     = ['goulash'],
    install_requires = [
        'addict',       # dictionary utility
        'ansi2html',    # required for goulash.ansi
        'werkzeug',     # used for caching helpers
        'fabric',       # misc. automation
        'argparse',     # command line option-parsing
        'configparser', # .ini configurations
        'mkdocs',       # static docs generation
        'epydoc',       # static docs generation
         ],
    entry_points = dict(
        console_scripts=[
            'goulash-boiler = goulash.bin.boiler:entry',
            'goulash-serve = goulash.bin.serv:entry',
            'goulash-docs = goulash.bin.docs:entry',
            'goulash = goulash.bin._goulash:entry',
            ]),
    package_data={'': ['*.*', 'goulash/data/*.*']},
    include_package_data=True,
    )
