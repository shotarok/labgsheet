#!/usr/bin/env python

from os import path

from setuptools import find_packages
from distutils.core import setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requires = [
    'gspread'
]

classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: Implementation :: PyPy',
]

setup(
    name='labgsheet',
    version='0.1.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    license='MIT',
    description='A python library to note ml experiments on google sheet',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shotarok/labgsheet',
    author='Shotaro Kohama',
    author_email='khmshtr28@gmail.com',
    install_requires=requires,
    classifiers=classifiers
)
