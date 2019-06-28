"""
Release handling for Bear.
"""

import sys
import json
from subprocess import Popen
from os import environ
from os.path import join, dirname, abspath, exists
from shutil import rmtree
from platform import platform
from urllib.parse import quote

from bear import NAME, VERSION

ROOT = dirname(abspath(__file__))
PKG = join(ROOT, NAME)
RELEASE_DIR = join(ROOT, 'release')
PYPI_REPO = environ.get('PYPI_REPO', 'https://upload.pypi.org/legacy/')
GITHUB_API = 'https://api.github.com'
GITHUB_REPO = 'KeyWeeUsr/Bear'
EXTENSIONS = {
    # meh... GitHub won't handle same-named binaries
    # therefore MacOS vs GNU/Linux name collision
    'linux': 'linux',
    'darwin': 'macos',
    'win32': 'exe'
}


def run_proc(args, options=None):
    """
    Run a command outside of the interpreter,
    but block until it's resolved.
    """
    proc = Popen(args, **({} if not options else options))
    proc.communicate()
    return proc.returncode == 0


def package_check():
    """Run style checkers and tests."""
    return run_proc(['python', 'check.py'])


def package_clean():
    """Clean cache folders."""
    run_proc(['python', '-m', 'pip', 'uninstall', '-y', NAME])

    folders = [
        'dist', 'build', f'{NAME}.egg-info'
    ]
    for folder in folders:
        if not exists(join(ROOT, folder)):
            continue
        rmtree(join(ROOT, folder))
    return True


def package_install():
    """Install deps via installing the packages."""
    return run_proc([
        'python', '-m', 'pip', 'install', '--upgrade',
        '--editable', '.[release]'
    ])


def package_dist():
    """Create Python package distributions: source + wheel."""
    return run_proc(['python', 'setup.py', 'sdist', 'bdist_wheel'])


def package_upload():
    """Upload created distributions to PyPI."""
    return run_proc([
        'python', '-m', 'twine', 'upload',
        '--repository-url', PYPI_REPO, 'dist/*'
    ])


def _create_executable_unix():
    return run_proc([
        'python', '-m', 'PyInstaller', '--name', NAME, '--clean',
        '--onefile', '--console', 'bear/__main__.py'
    ])


def create_executable_linux():
    """Create a binary for GNU/Linux platform."""
    result = True
    if sys.platform == 'linux':
        result = _create_executable_unix()
    return result


def create_executable_macos():
    """Create a binary for MacOS platform."""
    result = True
    if sys.platform == 'darwin':
        result = _create_executable_unix()
    return result


def create_github_release():
    """Draft a new release for a tag (application version) on GitHub."""
    import requests

    result = False
    resp = requests.post(
        f'{GITHUB_API}/repos/{GITHUB_REPO}/releases', data=json.dumps({
            'tag_name': VERSION,
            'name': VERSION,
            'draft': False
        }), headers={
            'Authorization': f'token {environ.get("GITHUB_TOKEN")}',
            'Content-Type': 'application/json'
        }
    )
    if resp.status_code == 201:
        result = True
    elif resp.status_code == 422:
        resp = requests.get(
            f'{GITHUB_API}/repos/{GITHUB_REPO}/releases/tags/{VERSION}',
            headers={
                'Authorization': f'token {environ.get("GITHUB_TOKEN")}'
            }
        )
        # confirmed that release available on GitHub
        result = resp.status_code == 200
    else:
        raise Exception((resp, resp.headers, resp.json()))
    return result


def _upload_executable(binary_name, upload_name):
    """Upload GNU/Linux executable to GitHub release page."""
    import requests

    result = False
    resp = requests.get(
        f'{GITHUB_API}/repos/{GITHUB_REPO}/releases/tags/{VERSION}',
        headers={
            'Authorization': f'token {environ.get("GITHUB_TOKEN")}'
        }
    )

    with open(join(ROOT, 'dist', binary_name), 'rb') as file:
        content = file.read()

    asset_props = f'?name={upload_name}&label={quote(platform())}'
    resp = requests.post(
        resp.json()['upload_url'].replace('{?name,label}', asset_props),
        data=content, headers={
            'Authorization': f'token {environ.get("GITHUB_TOKEN")}',
            'Content-Type': 'application/octet-stream'
        }
    )

    if resp.status_code in (201, 422):
        result = True
    else:
        raise Exception((resp, resp.headers, resp.json()))
    return result


def upload_executable_linux():
    """Upload GNU/Linux executable to GitHub release page."""
    result = True
    if sys.platform == 'linux':
        result = _upload_executable(NAME, f'{NAME}.{EXTENSIONS[sys.platform]}')
    return result


def upload_executable_macos():
    """Upload GNU/Linux executable to GitHub release page."""
    result = True
    if sys.platform == 'darwin':
        result = _upload_executable(NAME, f'{NAME}.{EXTENSIONS[sys.platform]}')
    return result


CASES = [
    package_clean,
    package_install,
    package_check,
    package_dist,
    # package_upload,
    package_clean,
    package_install,
    create_github_release,
    create_executable_linux,
    upload_executable_linux,
    create_executable_macos,
    upload_executable_macos
]


def main():
    """Main function for release."""
    cases_len = len(CASES)
    for i, case in enumerate(CASES):

        current = str(i + 1).zfill(len(str(cases_len)))
        print(f'<{current}/{cases_len}> ', end='')

        if case():
            print('Success!')
        else:
            print('Fail!')
            exit(1)


if __name__ == '__main__':
    main()
