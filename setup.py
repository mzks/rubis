#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, re, ast
from setuptools import setup, find_packages


PACKAGE_NAME = 'rubis'
with open(os.path.join(PACKAGE_NAME, '__init__.py')) as f:
    match = re.search(r'__version__\s+=\s+(.*)', f.read())
version = str(ast.literal_eval(match.group(1)))

setup(
    name="rubis",
    version=version,
    url='https://github.com/mzks/rubis',
    author='Keita Mizukoshi',
    author_email='mzks@stu.kobe-u.ac.jp',
    maintainer='Keita Mizukoshi',
    maintainer_email='mzks@stu.kobe-u.ac.jp',
    description='Control tool of ADC monitor board, "rubis" on Raspberry Pi',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['PyMySQL', 'adafruit-circuitpython-ads1x15', 'psutil'],
    license="MIT",
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
    'console_scripts': [ 'rubis=rubis.cli:main' ]
    }
)
