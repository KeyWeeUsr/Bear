"""
Main module for running the package as a Python module from console:

    python -m <package>
"""

import argparse
from bear import hash_file


def main(args):
    """
    Main function for calling the API from the package depending on
    the CLI options.
    """
    for file in args.files:
        print(hash_file(file))


def run():
    """
    CLI arguments parser for the main function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'files', metavar='FILE', type=str, nargs='+',
        help='files for hashing'
    )
    main(parser.parse_args())


if __name__ == '__main__':
    run()
