#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tileboard.
Easily draw high quality board game diagrams.
"""


import io
import os
import re
import string
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


# All exceptions in Tileboard are of this type:

class TileboardError(Exception):
    pass


# Board representation:

class Board(object):
    """
    Represented as a list of rows, where each row is a string
    of characters of *constant* length.

    Do not use this constructor, use "fen_make_board(position)" instead.
    """
    def __init__(self, rows, width, height):
        self.rows = rows
        self.width = width
        self.height = height


# Parsing FEN positions:

def fen_validate(position):
    """ Check that a FEN position has rows and contains valid characters. """
    has_rows = False

    for character in position:
       if not character == '/':
            has_rows = True

    if not has_rows:
        raise TileboardError('Empty FEN position.')


def fen_expand_numbers(position):
    """ Replace numbers from 1..9 with as much spaces as the number value. """
    return re.sub('[1-9]', lambda match: ' ' * int(match.group(0)), position)


def fen_make_board(position):
    """ Create a Board from a FEN position. """
    fen_validate(position)

    rows = fen_expand_numbers(position).split('/')
    width = max(map(len, rows))
    height = len(rows)

    # fill with zeros (holes) to make sure that all the rows
    # have the same length:
    rows = [row.ljust(width, '0') for row in rows]

    return Board(rows, width, height)


# Traversing boards:

def walk_board(board):
    """ Yields all the non-hole tiles in board. """
    for row in board.rows:
        for tile in row:
            if tile != '0':
                yield tile


def walk_board_pieces(board):
    """ Like "walk_board()", but blank squares are ignored. """
    for tile in walk_board(board):
        if tile != ' ':
            yield tile


def walk_rows(board):
    """ Yields (tile, row, col), for all non-hole tiles in the board. """
    for row in range(board.height):
        for col in range(board.width):
            tile = board.rows[row][col]
            if tile != '0':
                yield tile, row, col


def walk_rows_pieces(board):
    """ Like walk_rows(), but blank squares are ignored. """
    for tile, row, col in walk_rows(board):
        if tile != ' ':
            yield tile, row, col


# Loading tilesets:

def piece_to_filename(piece):
    """ Convert a piece mnemonic into a filename to load. """
    filename = piece.lower()

    # some operating systems do not distinguish between uppercase
    # and lowercase characters, therefore we prepend 'u' or 'l':
    if piece in string.ascii_uppercase:
        return 'u' + filename

    if piece in string.ascii_lowercase:
        return 'l' + filename

    return filename


def validate_tile_sizes(images):
    """ Ensure that a set of images are squares of equal size. """
    last_image_size = None
    last_image_filename = None

    for image in images:
        width, height = image.size

        # square?
        if width != height:
            raise TileboardError('Image width and height differ: {}'
                .format(image.filename))

        # the size we want?
        if last_image_size is not None:
            if (width != last_image_size) or (height != last_image_size):
                raise TileboardError('Image sizes do not match each other: {} - {}.'
                    .format(last_image_filename, image.filename))

        last_image_size = width
        last_image_filename = image.filename

    return last_image_size


def load_tileset(board, folder):
    """ Load all the piece images required to draw 'board'."""
    images = {}

    for piece in walk_board_pieces(board):
        if not piece in images:
            filename = piece_to_filename(piece)
            filepath = os.path.join(folder, filename)

            try:
                image = Image.open(filepath)
                image.load()
                images[piece] = image

            except Exception as err:
               raise TileboardError('Unable to load image: {} for: {}: {}'
                    .format(filepath, piece, err))

    return images


# Parser:

def make_parser():
    parser = ArgumentParser(
        description = __doc__,
        formatter_class = RawDescriptionHelpFormatter,
        usage = 'Tileboard.py position filepath [option [options ...]]',
        epilog  = 'example: Tileboard.py rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR chess.png'
    )

    # tileset:
    parser.add_argument("--tilesize",
        help = "board square size",
        default = 42, dest = 'tilesize', metavar = 'int', type = int)

    parser.add_argument("--tileset",
    help = "where to look for piece tiles",
    default = 'Tiles/merida/42', dest = 'tileset', metavar = 'folder', type = str)

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
        board = fen_make_board(options.position)
        tileset = load_tileset(board, options.tileset)

        # determine the base tile size:
        tilesize = validate_tile_sizes(tileset.values())

        if tilesize is None:
            tilesize = options.tilesize

        # board sizes:
        width = tilesize * board.width
        height = tilesize * board.height

    except TileboardError as err:
        errln('{}'.format(err))
        status = 1

    sys.exit(status)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

