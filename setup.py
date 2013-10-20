#!/usr/bin/env python

import os
import sys

import plyer

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'plyer',
    'plyer.platforms',
    'plyer.platforms.linux',
    'plyer.platforms.android',
    'plyer.platforms.win',
    'plyer.platforms.win.libs',
    'plyer.platforms.ios',
    'plyer.platforms.macosx',
]

setup(
    name='plyer',
    version=plyer.__version__,
    description='Platform-independant wrapper for platform-dependant APIs',
    long_description=open('README.md').read(),
    author='Kivy team',
    author_email='mat@kivy.org',
    url='https://plyer.readthedocs.org/en/latest/',
    packages=packages,
    package_data={'': ['LICENSE', 'README.md']},
    package_dir={'plyer': 'plyer'},
    include_package_data=True,
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',

    ),
)