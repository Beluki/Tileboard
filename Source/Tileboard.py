#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tileboard.
Easily draw high quality board game diagrams.
"""


import io
import os
import re
import sys

from argparse import ArgumentParser, RawDescriptionHelpFormatter


# Information and error messages:

def outln(line):
    """ Write 'line' to stdout, using the platform encoding and newline format. """
    print(line, flush = True)


def errln(line):
    """ Write 'line' to stderr, using the platform encoding and newline format. """
    print('Tileboard.py: error:', line, file = sys.stderr, flush = True)


# Non-builtin imports:

try:
    from PIL import Image

except ImportError:
    errln('Tileboard requires the following modules:')
    errln('Pillow 3.0.0+ - <https://pypi.python.org/pypi/Pillow>')
    sys.exit(1)


# All exceptions in tileboard are of this type:

class TileboardError(Exception):
    pass


# Board representation:

class Board(object):
    """
    Represented as a list of rows, where each row is a string
    of characters of variable length.

    Do not use this constructor, use "make_board()" instead.
    """
    def __init__(self, rows, width, height):
        self.rows = rows
        self.width = width
        self.height = height


# Fen position parsing:

def validate_fen(fen):
    """ Check that a FEN position has rows and contains valid characters. """
    has_rows = False

    for character in fen:
       if not character == '/':
            has_rows = True

    if not has_rows:
        raise TileboardError('Empty FEN position.')


def expand_numbers(fen):
    """ Replace numbers from 1..9 with as much spaces as the number value. """
    return re.sub('[1-9]', lambda match: ' ' * int(match.group(0)), fen)


def make_board(fen):
    """ Create a Board from a FEN position. """
    validate_fen(fen)

    rows = expand_numbers(fen).split('/')
    width = max(map(len, rows))
    height = len(rows)

    # fill with holes to make sure all the rows have the same length:
    rows = [row.ljust(width, '0') for row in rows]

    return Board(rows, width, height)


# Parser:

def make_parser():
    parser = ArgumentParser(
        description = __doc__,
        formatter_class = RawDescriptionHelpFormatter,
        usage = 'Tileboard.py position filepath [option [options ...]]',
        epilog  = 'example: Tileboard.py rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR chess.png'
    )

    # required:
    parser.add_argument('position',
        help = "board position in FEN notation",
        type = str)

    parser.add_argument('filepath',
        help = "output file, including extension",
        type = str)

    return parser


# Entry point:

def main():
    parser = make_parser()
    options = parser.parse_args()
    status = 1

    try:
        # load resources:
        board = make_board(options.position)

    except TileboardError as err:
        errln('{}'.format(err))
        status = 1

    sys.exit(status)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

