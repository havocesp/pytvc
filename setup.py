# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages
import sys
sys.path.append(os.path.dirname(__file__))
from . import pvtvc

classifiers = [
    'Development Status :: 5 - Production',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

exclude = ['.idea*', 'build*', '{}.egg-info*'.format(__package__), 'dist*', 'venv*', 'doc*', 'lab*']

setup(
    name=pytvc.__package__,
    version=pytvc.__version__,
    packages=find_packages(exclude=exclude),
    entry_points={
        'console_scripts': [
            'pytvc = pytvc.cli:main.start'
        ]
    },
    url=pytvc.__site__,
    long_description=pytvc.__long_description__,
    long_description_content_type='text/markdown',
    license=pytvc.__license__,
    author=pytvc.__author__,
    author_email=pytvc.__email__,
    description=pytvc.__description__,
    keywords=pytvc.__keywords__,
    classifiers=classifiers,
    install_requires=pytvc.__dependencies__
)
