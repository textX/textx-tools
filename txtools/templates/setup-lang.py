#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup

__author__ = "TODO <TODO AT somedomain DOT com>"
__version__ = "0.1"

NAME = '{{full_project_name}}'
DESC = 'TODO'
VERSION = __version__
AUTHOR = 'TODO'
AUTHOR_EMAIL = __author__
LICENSE = 'MIT'
URL = 'https://github.com/TODO/%s' % NAME
DOWNLOAD_URL = 'https://github.com/TODO/%s/archive/v%s.tar.gz' % \
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
    packages = ["{{package_name}}"],
    install_requires = ["textX"],
    keywords = "tools language DSL",
    entry_points={
        'textx_lang': [
            '{{package_name}} = {{package_name}}.lang:main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ]

)
