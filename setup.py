#!/usr/bin/env python
"""
Basic setup.py
"""

from os.path import abspath, dirname, join, relpath
from setuptools import setup, find_packages
from bear import VERSION, NAME


ROOT = abspath(dirname(__file__))
REPO = 'https://github.com/KeyWeeUsr/Bear'
PKG = join(ROOT, NAME)


with open(join(ROOT, "README.md")) as fd:
    README = fd.read()


DATA = [
    relpath('README.md', ROOT)
]


setup(
    name='thebear',
    version=VERSION,
    description='Bear - the decluttering deduplicator',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author='Peter Badida',
    author_email='keyweeusr@gmail.com',
    url='https://github.com/KeyWeeUsr/Bear',
    download_url=f'https://github.com/KeyWeeUsr/Bear/tarball/{VERSION}',
    entry_points={
        'console_scripts': [f'{NAME} = {NAME}.__main__:run']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: '
        'GNU Affero General Public License v3 or later (AGPLv3+)',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Typing :: Typed'
    ],
    install_requires=['ensure'],
    extras_require={
        'dev': ['pycodestyle', 'pylint', 'coverage'],
        'ci': ['coveralls'],
        'release': [
            'setuptools', 'wheel',
            'pycodestyle', 'pylint',
            'coverage', 'coveralls',
            'twine', 'pyinstaller', 'requests'
        ]
    },
    include_package_data=True,
    data_files=[(NAME, DATA)]
)
