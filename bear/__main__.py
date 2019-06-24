"""
Main module for running the package as a Python module from console:

    python -m <package>
"""

import logging
from os import stat, remove
from argparse import ArgumentParser
from bear import (
    hash_file, find_files, hash_files, filter_files,
    find_duplicates, output_duplicates, NAME, LOGO
)

LOG = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
)


def set_log_levels(level):
    """
    Set log levels for all available loggers at runtime.
    """
    loggers = [
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
    ]
    for logger in loggers:
        logger.setLevel(level)


def handle_duplicates(args):
    """
    Handle --duplicate related behavior.
    """
    duplicates = find_duplicates(args.duplicates, args.jobs)
    output_duplicates(duplicates, args.output)
    if args.keep_oldest:
        for dups in duplicates.values():
            # oldest == smallest timestamp
            without_oldest = sorted(
                dups, key=lambda item: stat(item).st_mtime
            )[1:]
            for file in without_oldest:
                remove(file)

    elif args.keep_newest:
        for dups in duplicates.values():
            # reverse for oldest
            without_newest = sorted(
                dups, key=lambda item: stat(item).st_mtime, reverse=True
            )[1:]
            for file in without_newest:
                remove(file)


def main(args):
    """
    Main function for calling the API from the package depending on
    the CLI options.
    """
    if not args.quiet:
        print(LOGO)

    if args.quiet:
        set_log_levels(logging.NOTSET)
    elif 0 < args.verbose <= 1:
        set_log_levels(logging.WARNING)
    elif 1 < args.verbose <= 2:
        set_log_levels(logging.INFO)
    elif args.verbose > 2:
        set_log_levels(logging.DEBUG)

    LOG.info('Setting up default logging level to %s', LOG.level)
    LOG.debug('CLI args: %s', args)

    if args.files:
        for file in args.files:
            print(hash_file(file))
    elif args.traverse:
        for folder in args.traverse:
            print(find_files(folder))
    elif args.hash:
        print(filter_files(hash_files([
            file
            for file_list in [find_files(folder) for folder in args.hash]
            for file in file_list
        ])))
    elif args.duplicates:
        handle_duplicates(args)


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
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument(
        '--files', metavar='FILE', type=str, nargs='+',
        help='files for hashing'
    )
    parser.add_argument(
        '--traverse', metavar='FOLDER', type=str, nargs='+',
        help='list all files in these folders recursively'
    )
    parser.add_argument(
        '--hash', metavar='FOLDER', type=str, nargs='+',
        help='hash all files in these folders recursively'
    )
    parser.add_argument(
        '--duplicates', metavar='FOLDER', type=str, nargs='+',
        help='find all duplicated files in these folders recursively'
    )
    parser.add_argument(
        '-j', '--jobs', action='store', type=int, default=1,
        help='set how many processes will be spawn for hashing, 0=max'
    )
    parser.add_argument(
        '-o', '--output', action='store', type=str,
        help='output file for the list of duplicates'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_true',
        help='suppress all output'
    )
    parser.add_argument(
        '-e', '--keep-oldest', action='store_true',
        help='in combination with --duplicates keep only single oldest file'
    )
    parser.add_argument(
        '-n', '--keep-newest', action='store_true',
        help='in combination with --duplicates keep only single newest file'
    )
    main(parser.parse_args())


if __name__ == '__main__':
    run()
