#! /usr/bin/python

"""speck -- rpm spec modification tool

Usage:
    se.py <spec> patch add <file>
    se.py <spec> patch disable <number>
    se.py <spec> patch enable <number>
    se.py <spec> patch list

Options:
    -h --help   Show this screen
    -d --debug  Print debug information
"""

from docopt import docopt
from speck import parser

if __name__ == '__main__':
    arguments = docopt(__doc__)

    parser.parse(arguments['<spec>'])

    if arguments['patch']:
        if arguments['add']:
            parser.add_patch(arguments['<file>'])
        elif arguments['enable']:
            parser.enable_patch(arguments['<number>'])
        elif arguments['disable']:
            parser.disable_patch(arguments['<number>'])
        elif arguments['list']:
            for patch in parser.patches:
                print str(patch)
