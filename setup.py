#!/usr/bin/env python

from setuptools import find_packages
from distutils.core import setup

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
    version='0.1.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    license='MIT',
    description='A python library to note ml experiments on google sheet',
    url='https://github.com/shotarok/labgsheet',
    author='Shotaro Kohama',
    author_email='khmshtr28@gmail.com',
    install_requires=requires,
    classifiers=classifiers
)
