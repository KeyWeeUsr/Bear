"""
Release handling for Bear.
"""

from subprocess import Popen
from os import environ
from os.path import join, dirname, abspath, exists
from shutil import rmtree

from bear import NAME

ROOT = dirname(abspath(__file__))
PKG = join(ROOT, NAME)
RELEASE_DIR = join(ROOT, 'release')
PYPI_REPO = environ.get('PYPI_REPO', 'https://upload.pypi.org/legacy/')


def run_proc(args, options=None):
    """
    Run a command outside of the interpreter,
    but block until it's resolved.
    """
    proc = Popen(args, **({} if not options else options))
    proc.communicate()
    return proc.returncode == 0


def run_check():
    """Run style checkers and tests."""
    return run_proc(['python', 'check.py'])


def run_clean():
    """Clean cache folders."""
    run_proc(['pip', 'uninstall', '-y', NAME])

    folders = [
        'dist', 'build', f'{NAME}.egg-info'
    ]
    for folder in folders:
        if not exists(join(ROOT, folder)):
            continue
        rmtree(join(ROOT, folder))
    return True


def run_install():
    """Install deps via installing the packages."""
    return run_proc([
        'pip', 'install', '--upgrade',
        '--editable', '.[release]'
    ])


def run_dist():
    """Create Python package distributions: source + wheel."""
    return run_proc(['python', 'setup.py', 'sdist', 'bdist_wheel'])


def run_upload():
    """Upload created distributions to PyPI."""
    return run_proc([
        'twine', 'upload', '--repository-url', PYPI_REPO, 'dist/*'
    ])


CASES = [
    run_clean,
    run_install,
    run_check,
    run_dist,
    run_upload
]


def main():
    """Main function for release."""
    cases_len = len(CASES)
    for i, test in enumerate(CASES):

        current = str(i + 1).zfill(len(str(cases_len)))
        print(f'<{current}/{cases_len}> ', end='')

        if test():
            print('Success!')
        else:
            print('Fail!')
            exit(1)


if __name__ == '__main__':
    main()
