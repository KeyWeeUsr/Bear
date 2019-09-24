"""
Style checker and test + coverage runner for Bear.
"""

from sys import exit
from subprocess import Popen
from os.path import join, dirname, abspath

ROOT = dirname(abspath(__file__))
PKG = join(ROOT, 'bear')

CASES = [[
    'python', '-m', 'pycodestyle',
    '--ignore=none',
    '--show-source',
    '--count',
    '--max-line-length=79',
    ROOT
], [
    'python', '-m', 'pylint',
    '--jobs=0',
    'release.py', 'check.py', 'setup.py', PKG
], [
    'python', '-m', 'coverage', 'run', '--branch', '--source', PKG,
    '-m', 'unittest', 'discover',
    '--failfast',
    '--catch',
    '--start-directory', join(PKG, 'tests'),
    '--top-level-directory', PKG
], [
    'python', '-m', 'coverage', 'report', '--show-missing'
], [
    'python', '-m', 'radon', 'cc', '--show-complexity',
    'release.py', 'check.py', 'setup.py', PKG
], [
    'python', '-m', 'radon', 'mi', '--show',
    'release.py', 'check.py', 'setup.py', PKG
], [
    'python', '-m', 'radon', 'hal',
    'release.py', 'check.py', 'setup.py', PKG
]]


if __name__ == '__main__':
    CASES_LEN = len(CASES)
    for i, test in enumerate(CASES):
        proc = Popen(test)
        proc.communicate()

        current = str(i + 1).zfill(len(str(CASES_LEN)))
        print(f'[{current}/{CASES_LEN}] ', end='')

        if proc.returncode == 0:
            print('Success!')
        else:
            print('Fail!')
            exit(proc.returncode)
