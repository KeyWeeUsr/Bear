#!/usr/bin/env python
"""
Basic setup.py
"""

from setuptools import setup, find_packages
from bear import VERSION, NAME

setup(
    name=NAME,
    version=VERSION,
    description='Bear',
    long_description='Bear',
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
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: '
        'GNU Affero General Public License v3 or later (AGPLv3+)',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
