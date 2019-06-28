# Bear

The decluttering deduplicator.

[![Coverage](https://coveralls.io/repos/KeyWeeUsr/Bear/badge.svg?branch=master)
](https://coveralls.io/r/KeyWeeUsr/Bear?branch=master)
[![Build](https://travis-ci.org/KeyWeeUsr/Bear.svg?branch=master)
](https://travis-ci.org/KeyWeeUsr/Bear)
[![GitHub version](https://badge.fury.io/gh/keyweeusr%2Fbear.svg)
](https://badge.fury.io/gh/keyweeusr%2Fbear)
[![PyPI version](https://img.shields.io/pypi/v/thebear.svg)
](https://pypi.org/project/thebear/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/thebear.svg)
](https://pypi.org/project/thebear/)
[![Latest release deps](https://img.shields.io/librariesio/release/pypi/thebear.svg)
](https://libraries.io/pypi/thebear)
[![GitHub repo deps](https://img.shields.io/librariesio/github/keyweeusr/bear.svg)
](https://libraries.io/pypi/bear)

[![Downloads total](https://pepy.tech/badge/thebear)
](https://pepy.tech/project/thebear)
[![Downloads month](https://pepy.tech/badge/thebear/month)
](https://pepy.tech/project/thebear)
[![Downloads week](https://pepy.tech/badge/thebear/week)
](https://pepy.tech/project/thebear)
[![All Releases](https://img.shields.io/github/downloads/keyweeusr/bear/total.svg)
](https://github.com/KeyWeeUsr/bear/releases)
[![Code bytes](https://img.shields.io/github/languages/code-size/keyweeusr/bear.svg)
](https://github.com/KeyWeeUsr/bear)
[![Repo size](https://img.shields.io/github/repo-size/keyweeusr/bear.svg)
](https://github.com/KeyWeeUsr/bear)

A bear as a spirit animal is strong and confident, it's a guide to take
leadership in your life without fear, provides courage and a stable foundation
to face challenges. The bear spirit helps to dedicate time and energy to
introspective practices.

Same as the bear spirit, this application provides you with confidence to take
leadership in your digital life, find all the mess you've been collecting for
a while and gives you a stable foundation to face the challenge of removing
duplicated data on your machine.

Once you start removing duplicates, soon you realize how much free space you've
gained and looking through the various files from the high-level point of view
will slightly poke you to set the order to the files, to categorize them and
eventually make your machine a clean space.

## Installation

Currently there is only a Python module available, but platform-specific
releases such as Windows .exe, MacOS .App and specific GNU/Linux distros
packages are planned.

### Python package

#### Requirements

* Python 3.7+ (3.6 should work too)

You can install a stable version with:

    pip install thebear
    pip install https://github.com/KeyWeeUsr/bear/zipball/stable

For the cutting-edge available changes use `master` branch:

    pip install https://github.com/KeyWeeUsr/bear/zipball/master

## Usage

There is a list of basic use-cases:

* hashing specific files:

      bear --files file1 file2 ...

* traversing folders for files

      bear --traverse folder1 folder2 ...

* hashing all files in specific folders

      bear --hash folder1 folder2 ...

* finding all duplicate files within specific folders

      bear --duplicates folder1 folder2 ...

There are other, advanced options you can list with `bear --help`.
