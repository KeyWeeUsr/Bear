import sys
from bear import hash_file


def main(parameters):
    for file in parameters[1:]:
        print(hash_file(file))


if __name__ == '__main__':
    main(sys.argv)
