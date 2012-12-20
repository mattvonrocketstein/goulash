#!/usr/bin/env python
""" setup.py for channels
"""
from setuptools import setup, find_packages
setup(
    name        ='namespaces',
    version     = '.1',
    description = 'object namespace partitioner',
    author      = 'mattvonrocketstein, in the gmails',
    url         = 'one of these days',
    package_dir = {'': 'lib'},
    packages    = find_packages('lib'),
    )
