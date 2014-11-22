#! /usr/bin/python

"""speck -- rpm spec modification tool

Usage:
    se.py <spec> add patch <file>

Options:
    -h --help   Show this screen
    -d --debug  Print debug information
"""

from docopt import docopt
from speck import parser

if __name__ == '__main__':
    arguments = docopt(__doc__)

    parser.parse(arguments['<spec>'])

    if arguments['add'] and arguments['patch']:
        parser.add_patch(arguments['<file>'])
