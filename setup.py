#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

packages = [
    "nodefactinfo",
    "nodefactinfo.api",
]

setup(
    name='nodefactinfo',
    version='0.0.1',
    description='Query puppetdb via the cli to get node and fact information',
    long_description=readme + '\n\n' + history,
    author='Daniel Lawrence',
    author_email='dannyla@linux.com',
    url='https://github.com/daniellawrence/nodefactinfo',
    packages=packages,
#    package_dir={'': ''},
    include_package_data=True,
    install_requires=[
        "pypuppetdb",
    ],
    license="BSD",
    zip_safe=False,
    keywords='nodefactinfo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    entry_points = {
        'console_scripts': [
            'nfi = nodefactinfo.nodefactinfo:main'
            ]
    },
)
