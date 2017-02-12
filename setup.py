# -*- coding: utf-8 -*-
"""
    sqlalchemy_seed
    ~~~~~~~~~~~~~~~

    sqlalchemy_seed is a simple data seeder using SQLAlchemy.


    :copyright: (c) 2017 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup, find_packages

requires = ['sqlalchemy', 'pyyaml', 'flake8']

rst_path = os.path.join(os.path.dirname(__file__), 'README.rst')
description = ''
with open(rst_path) as f:
    description = f.read()

setup(
    name='sqlalchemy_seed',
    version='0.1.1',
    author='Shinya Ohyanagi',
    author_email='sohyanagi@gmail.com',
    url='http://github.com/heavenshell/py-sqlalchemy_seed',
    description='sqlalchemy_seed is simple data seeder using SQLAlchmy.',
    long_description=description,
    license='BSD',
    platforms='any',
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    install_requires=requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Database',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    tests_require=requires,
    test_suite='tests'
)
