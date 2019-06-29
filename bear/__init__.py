"""
Main file for the Bear package.
"""

NAME = 'bear'
VERSION = '0.3.1'
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
