# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import pytvc

classifiers = [
    'Development Status :: 5 - Production',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

exclude = ['.idea*', 'build*', f'{pytvc.__package__}.egg-info*', 'dist*', 'venv*', 'doc*', 'lab*']

readme_file = Path(__file__).with_name('README.md')

setup(
    name=pytvc.__package__,
    version=pytvc.__version__,
    packages=find_packages(exclude=exclude),
    package_dir={pytvc.__package__: pytvc.__package__},
    package_data={pytvc.__package__: ['html/*.*', 'json/*.*']},
    entry_points={
        'console_scripts': [
            'pytvc = pytvc.cli:run'
        ]
    },
    url=pytvc.__site__,
    long_description=readme_file.read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    license=pytvc.__license__,
    author=pytvc.__author__,
    author_email=pytvc.__email__,
    description=pytvc.__description__,
    keywords=pytvc.__keywords__,
    classifiers=classifiers,
    install_requires=pytvc.__dependencies__
)
