"""
Main module for running the package as a Python module from console:

    python -m <package>
"""

import sys
import logging
from os import stat, remove
from argparse import ArgumentParser, Namespace
from webbrowser import open as open_browser

from ensure import ensure_annotations

from bear import NAME, LOGO, LOGO_HELP, VERSION, COMMUNITY_URL
from bear.common import Hasher
from bear.hashing import hash_file, hash_files
from bear.output import (
    find_files, filter_files, find_duplicates, output_duplicates
)
from bear.context import Context

LOG = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
)


@ensure_annotations
def set_log_levels(level: int):
    """
    Set log levels for all available loggers at runtime.
    """
    loggers = [
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
    ]
    for logger in loggers:
        logger.setLevel(level)


@ensure_annotations
def print_logo(ctx: Context):
    """
    Print logo at the beginning of the CLI output.
    """
    if ctx.quiet or ctx.version:
        return

    if len(sys.argv) == 1:
        print(LOGO_HELP)
    else:
        print(LOGO)


@ensure_annotations
def handle_duplicates(ctx: Context, hasher: Hasher):
    """
    Handle --duplicate related behavior.
    """

    duplicates = find_duplicates(ctx=ctx, hasher=hasher)
    output_duplicates(hashes=duplicates, out=ctx.output)
    if ctx.keep_oldest:
        for dups in duplicates.values():
            # oldest == smallest timestamp
            without_oldest = sorted(
                dups, key=lambda item: stat(item).st_mtime
            )[1:]
            for file in without_oldest:
                remove(file)

    elif ctx.keep_newest:
        for dups in duplicates.values():
            # reverse for oldest
            without_newest = sorted(
                dups, key=lambda item: stat(item).st_mtime, reverse=True
            )[1:]
            for file in without_newest:
                remove(file)


@ensure_annotations
def get_hasher(ctx: Context) -> Hasher:
    """
    Get non-MD5 hasher if desired.
    """
    if ctx.blake2:
        result = Hasher.BLAKE2
    elif ctx.sha256:
        result = Hasher.SHA256
    elif ctx.md5:
        result = Hasher.MD5
    return result


@ensure_annotations
def main(args: Namespace):
    """
    Main function for calling the API from the package depending on
    the CLI options.
    """
    ctx = Context(args)

    print_logo(ctx)

    if ctx.quiet:
        set_log_levels(logging.NOTSET)
    elif 0 < ctx.verbose <= 1:
        set_log_levels(logging.WARNING)
    elif 1 < ctx.verbose <= 2:
        set_log_levels(logging.INFO)
    elif ctx.verbose > 2:
        set_log_levels(logging.DEBUG)

    LOG.info('Setting up default logging level to %s', LOG.level)
    LOG.debug('CLI args: %s', args)
    LOG.debug('Context: %s', vars(ctx))

    hasher = get_hasher(ctx)

    # actions
    if ctx.files:
        for file in ctx.files:
            print(hash_file(path=file, hasher=hasher))
    elif ctx.traverse:
        for folder in ctx.traverse:
            print(find_files(ctx=ctx, folder=folder))
    elif ctx.hash:
        found_lists = [
            find_files(ctx=ctx, folder=folder)
            for folder in ctx.hash
        ]
        print(filter_files(hash_files(files=[
            file
            for file_list in found_lists
            for file in file_list
        ], hasher=hasher)))
    elif ctx.duplicates:
        handle_duplicates(ctx=ctx, hasher=hasher)
    elif ctx.version:
        print(VERSION)
    elif ctx.community:
        open_browser(COMMUNITY_URL)


class BearArgumentParser(ArgumentParser):
    """
    Custom ArgumentParser to display ASCII logo.
    """

    def print_help(self, file=None):
        print(LOGO)
        super(BearArgumentParser, self).print_help(file)

    def error(self, message):
        print(LOGO)
        super(BearArgumentParser, self).error(message)


def run():
    """
    CLI arguments parser for the main function.
    """
    parser = BearArgumentParser(prog=NAME)
    parser.add_argument(
        '-j', '--jobs', action='store', type=int, default=1,
        help='set how many processes will be spawn for hashing, 0=max'
    )
    parser.add_argument(
        '-o', '--output', action='store', type=str, default='',
        help='output file for the list of duplicates'
    )
    parser.add_argument(
        '-x', '--exclude', metavar="VALUE",
        type=str, nargs="+", default=[],
        help='exclude full paths that contain this value'
    )
    parser.add_argument(
        '-X', '--exclude-regex', metavar="REGEX",
        type=str, nargs="+", default=[],
        help='regex pattern for excluding full paths or filenames'
    )
    parser.add_argument(
        "--max-size", metavar="BYTES", action="store", type=int, default=0,
        help="exclude files if their size is above the limit, 0=unlimited"
    )

    group_verbosity = parser.add_mutually_exclusive_group()
    group_verbosity.add_argument(
        '-v', '--verbose', action='count', default=0, help=(
            f"stack up to three times to switch between logging verbosity -"
            f" NONE (default), WARNING, WARNING + INFO, WARNING + INFO + DEBUG"
        )
    )
    group_verbosity.add_argument(
        '-q', '--quiet', action='store_true', help='suppress all output'
    )

    group_action = parser.add_mutually_exclusive_group()
    group_action.add_argument(
        '-f', '--files', metavar='FILE', type=str, nargs='+',
        help='files for hashing'
    )
    group_action.add_argument(
        '-t', '--traverse', metavar='FOLDER', type=str, nargs='+',
        help='list all files in these folders recursively'
    )
    group_action.add_argument(
        '-s', '--hash', metavar='FOLDER', type=str, nargs='+',
        help='hash all files in these folders recursively'
    )
    group_action.add_argument(
        '-d', '--duplicates', metavar='FOLDER', type=str, nargs='+',
        help='find all duplicated files in these folders recursively'
    )
    group_action.add_argument(
        '-V', '--version', action='store_true', help=(
            'print current version in a standard format specified in PEP 440'
            ' (https://www.python.org/dev/peps/pep-0440/)'
        )
    )
    group_action.add_argument(
        '--community', '--support', '--chat', action='store_true', help=(
            f'Open {NAME} Matrix community in your browser'
        )
    )

    group_remove = parser.add_mutually_exclusive_group()
    group_remove.add_argument(
        '-e', '--keep-oldest', action='store_true',
        help='in combination with --duplicates keep only single oldest file'
    )
    group_remove.add_argument(
        '-n', '--keep-newest', action='store_true',
        help='in combination with --duplicates keep only single newest file'
    )

    group_hash = parser.add_mutually_exclusive_group()
    group_hash.add_argument(
        '--md5', action='store_true', default=True,
        help='use MD5 function for hashing (default)'
    )
    group_hash.add_argument(
        '--blake2', action='store_true',
        help='use BLAKE2 function for hashing'
    )
    group_hash.add_argument(
        '--sha256', action='store_true',
        help='use SHA256 function for hashing'
    )
    main(parser.parse_args())


if __name__ == '__main__':
    run()
