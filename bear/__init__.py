"""
Main file for the Bear package.
"""

NAME = 'bear'
PYPI_NAME = 'thebear'
PYPI_INDEX = 'https://pypi.org/simple'
VERSION = '0.5.0'
GITHUB_WEB = 'https://github.com'
GITHUB_API = 'https://api.github.com'
REPO_PATH = 'KeyWeeUsr/Bear'
REPO = f'{GITHUB_WEB}/KeyWeeUsr/Bear'
DESCRIPTION = 'Bear - the decluttering deduplicator'
AUTHOR = 'Peter Badida'
AUTHOR_EMAIL = 'keyweeusr@gmail.com'
LOGO = r"""
 ,--.-'--.,.
/¯  Bear   °¯;
\ , ___ ,\¯ˇ¯
|_;_\ /_;_\
"""
HELP = fr"""
     /¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\
  <  Use {NAME} -h or {NAME} --help |
    \                            /
       ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
"""
LOGO_HELP = '\n'.join([
    left + right
    for left, right in zip(LOGO.split('\n'), HELP.split('\n'))
])
