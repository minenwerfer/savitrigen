#!/usr/bin/env python3

from setuptools import setup, find_packages
version = 1.0

setup(
    name='savitrigen',
    version=version,
    description='Savitri code generator',
    author='João Santos',
    license='ISC',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'savitrigen = savitrigen.main:main'
        ]
    },
)
