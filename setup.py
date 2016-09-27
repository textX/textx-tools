#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages

__author__ = "Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>"
__version__ = "0.1"

NAME = 'textx-tools'
DESC = 'The developer tool infrastructure for textX'
VERSION = __version__
AUTHOR = 'Igor R. Dejanovic'
AUTHOR_EMAIL = 'igor DOT dejanovic AT gmail DOT com'
LICENSE = 'MIT'
URL = 'https://github.com/igordejanovic/%s' % NAME
DOWNLOAD_URL = 'https://github.com/igordejanovic/%s/archive/v%s.tar.gz' % \
    (NAME, VERSION)
README = codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'),
                     'r', encoding='utf-8').read()

setup(
    name = NAME,
    version = VERSION,
    description = DESC,
    long_description = README,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    maintainer = AUTHOR,
    maintainer_email = AUTHOR_EMAIL,
    license = LICENSE,
    url = URL,
    download_url = DOWNLOAD_URL,
    packages = find_packages(),
    package_data={
        'txtools.cli': ['templates/*.template'],
    },
    zip_safe=False,
    install_requires = ["textX", "click", "Jinja2"],
    keywords = "tools parser generator meta-language meta-model language DSL",
    entry_points={
        'console_scripts': [
            'textx = txtools.cli:textx'
        ],
        'textx_commands': [
            'vis = txtools.cli.vis:vis',
            'check = txtools.cli.check:check',
            'startproject = txtools.cli.startproject:startproject',
            'list-gens = txtools.cli.list_gens:list_gens',
            'list-langs = txtools.cli.list_langs:list_langs',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ]

)
