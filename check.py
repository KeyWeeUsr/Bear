"""
Style checker and test + coverage runner for Bear.
"""

from subprocess import Popen
from os.path import join, dirname, abspath

ROOT = dirname(abspath(__file__))
PKG = join(ROOT, 'bear')

CASES = [[
    'pycodestyle',
    '--ignore=none',
    '--show-source',
    '--count',
    '--max-line-length=79',
    ROOT
], [
    'pylint',
    '--jobs=0',
    'release.py', 'check.py', 'setup.py', PKG
], [
    'coverage', 'run', '--branch', '--source', PKG,
    '-m', 'unittest', 'discover',
    '--failfast',
    '--catch',
    '--start-directory', join(PKG, 'tests'),
    '--top-level-directory', PKG
], [
    'coverage', 'report', '--show-missing'
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
