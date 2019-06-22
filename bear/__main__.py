"""
Main module for running the package as a Python module from console:

    python -m <package>
"""

import argparse
from bear import hash_file, find_files, hash_files


def main(args):
    """
    Main function for calling the API from the package depending on
    the CLI options.
    """
    if args.files:
        for file in args.files:
            print(hash_file(file))
    elif args.traverse:
        for folder in args.traverse:
            print(find_files(folder))
    elif args.hash:
        for folder in args.hash:
            print(hash_files(find_files(folder)))


def run():
    """
    CLI arguments parser for the main function.
    """
    parser = argparse.ArgumentParser()
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
    main(parser.parse_args())


if __name__ == '__main__':
    run()
