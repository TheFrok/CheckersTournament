#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='CheckersTournament',
    version='0.2',
    packages=find_packages('src'),
    # packages=['CheckersTournament'],
    package_dir={'': 'src'},
    # package_dir={'CheckersTournament': 'src/CheckersTournament'},
    url='https://github.com/TheFrok',
    license='BSD-2-Clause',
    author='TheFrok',
    author_email='',
    description='A utility to create a tournament between different Checkers strategies'
)
