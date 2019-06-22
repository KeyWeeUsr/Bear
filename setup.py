#!/usr/bin/env python
"""
Basic setup.py
"""

from setuptools import setup, find_packages


setup(
    name='Bear',
    version='0.0.1',
    description='Bear',
    long_description='Bear',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author='Peter Badida',
    author_email='keyweeusr@gmail.com',
    url='https://github.com/KeyWeeUsr/Bear',
    download_url='https://github.com/KeyWeeUsr/Bear/tarball/0.0.1',
    classifiers=[
        'Development Status :: 1 - Planning',
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
