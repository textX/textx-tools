#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
from setuptools import setup, find_packages
import txtools

NAME = 'textx-tools'
DESC = 'The developer tool infrastructure for textX'
VERSION = txtools.__version__
AUTHOR = 'Igor R. Dejanovic'
AUTHOR_EMAIL = 'igor DOT dejanovic AT gmail DOT com'
LICENSE = 'MIT'
URL = 'https://github.com/igordejanovic/%s' % NAME
DOWNLOAD_URL = 'https://github.com/igordejanovic/%s/archive/v%s.tar.gz' % \
    (NAME, VERSION)
README = codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'),
                     'r', encoding='utf-8').read()

if sys.argv[-1].startswith('publish'):
    if os.system("pip list | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip list | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    if sys.argv[-1] == 'publishtest':
        os.system("twine upload -r test dist/*")
    else:
        os.system("twine upload dist/*")
        print("You probably want to also tag the version now:")
        print("  git tag -a {0} -m 'version {0}'".format(VERSION))
        print("  git push --tags")
    sys.exit()

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
    include_package_data=True,
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
            'generate = txtools.cli.generate:generate',
            'startproject = txtools.cli.startproject:startproject',
            'list-gens = txtools.cli.list_gens:list_gens',
            'list-langs = txtools.cli.list_langs:list_langs',
        ],
        'textx_lang': [
            'genconf = txtools.lang.genconf:meta'
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
