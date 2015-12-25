#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tileboard.
Easily draw high quality board game diagrams.
"""


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
    from PIL import Image, ImageDraw, ImageFont

except ImportError:
    errln('Tileboard requires the following modules:')
    errln('Pillow 3.0.0+ - <https://pypi.python.org/pypi/Pillow>')
    sys.exit(1)


# Board representation:

class Board(object):
    """
    Represented as a list of rows, where each row is a string
    of characters of *constant* length.

    Do not use this constructor, use: "fen_make_board(position)" instead.
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
        raise ValueError('Empty FEN position.')


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


# Base 26 conversions:
# http://en.wikipedia.org/wiki/Hexavigesimal

def to_base26(number):
    """ Convert a zero-based integer to a (lowercase) base-26 string. """
    s = []
    first_letter = True

    while True:
        remainder = number % 26

        if not first_letter and number < 25:
            remainder -= 1

        s[0:0] = chr(97 + remainder)
        first_letter = False

        number = (number - remainder) // 26
        if number == 0:
            return ''.join(s)


def from_base26(string):
    """
    Convert a base-26 string to a zero-based integer.
    The input string may be either lowercase or uppercase.
    """
    string = string.lower()

    size = len(string)
    number = ord(string[0]) - 97

    if size > 1:
        if number < 25:
            number += 1

        for i in range(1, size):
            number *= 26
            number += ord(string[i]) - 97

    return number


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
            raise ValueError('Image width and height differ: {}'
                .format(image.filename))

        # the size we want?
        if last_image_size is not None:
            if (width != last_image_size) or (height != last_image_size):
                raise ValueError('Image sizes do not match each other: {} - {}.'
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
               raise ValueError('Unable to load image: {} for: {}: {}'
                    .format(filepath, piece, err))

    return images


# Loading fonts:

def load_font(filepath, size):
    """
    Load a truetype font.
    """
    try:
        return ImageFont.truetype(filepath, size)

    except Exception as err:
        raise ValueError('Unable to load font: {}'.format(filepath))


# Calculating sizes:

def calculate_border_font_size(tilesize):
    """ Calculate ideal border font size. """
    # this could be more clever, right now we just have a minimum
    # readable size (12px) and scale to the tile size:
    return max(tilesize // 3, 12)


def calculate_border_size(board, tilesize, font):
    """ Calculate the minimum border size needed to draw the border text. """
    border_size = tilesize // 2

    max_col_text = to_base26(board.width)
    max_row_text = str(board.height)

    max_col_text_width, _ = font.getsize(max_col_text)
    max_row_text_width, _ = font.getsize(max_row_text)

    # include 10px padding:
    max_col_text_width += 10
    max_row_text_width += 10

    return max(border_size, max_col_text_width, max_row_text_width)


def calculate_outline_size(tilesize):
    """ Calculate ideal outline size. """
    # so that big tilesizes get a bigger outline:
    return max(tilesize // 100, 1)


def make_base_image(image_width, image_height, border_color, outline_color, outline_size):
    """ Create the target image. """

    # the initial image already contains the outline color:
    image = Image.new('RGBA', (image_width, image_height), color = outline_color)
    draw = ImageDraw.Draw(image)

    # draw the border:
    x1 = outline_size
    y1 = outline_size
    x2 = image_width - outline_size - 1
    y2 = image_height - outline_size - 1

    draw.rectangle([x1, y1, x2, y2], fill = border_color)
    del draw

    return image


# Drawing:

class BoardDraw(object):
    """
    Encapsulates board drawing in a single class that holds
    the common shared parameters.
    """
    def __init__(self, image, board, tilesize):
        self.image = image
        self.board = board
        self.tilesize = tilesize

    def draw_checkerboard(self, xy, color0, color1, color2):
        """ Draw a checkerboard pattern. """
        xoffset, yoffset = xy
        draw = ImageDraw.Draw(self.image)

        # draw the background (holes) as a single rectangle:
        x1 = xoffset
        y1 = yoffset
        x2 = x1 + (self.tilesize * self.board.width) - 1
        y2 = y1 + (self.tilesize * self.board.height) - 1

        draw.rectangle([x1, y1, x2, y2], fill = color0)

        # draw the checkerboard:
        for tile, row, col in walk_rows(self.board):
            x1 = xoffset + (col * self.tilesize)
            y1 = yoffset + (row * self.tilesize)
            x2 = x1 + self.tilesize - 1
            y2 = y1 + self.tilesize - 1

            if (col % 2) == (row % 2):
                color = color1
            else:
                color = color2

            draw.rectangle([x1, y1, x2, y2], color)

        del draw


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
        help = 'board position in FEN notation',
        type = str)

    parser.add_argument('filepath',
        help = 'output file, including extension',
        type = str)


    # optional
    # border options:
    border_options = parser.add_argument_group('border options')

    border_options.add_argument('--border-color',
        help = 'color for the border background',
        default = '#FFFFFF', dest = 'border_color', metavar = 'color',
        type = str)

    border_options.add_argument('--border-disable',
        help ='do not draw the coordinates border',
        action = 'store_const', dest = 'border_disable',
        const = True)

    border_options.add_argument('--border-uppercase',
        help = 'use uppercase letters in the border',
        action = 'store_const', dest = 'border_uppercase',
        const = True)

    border_options.add_argument('--border-font',
        help = 'font to use for border letters and numbers',
        default = 'Font/LiberationMono-Regular.ttf', dest = 'border_font', metavar = 'file.ttf',
        type = str)

    border_options.add_argument('--border-font-color',
        help = 'color to use for border letters and numbers',
        default = '#000000', dest = 'border_font_color', metavar = 'color',
        type = str)


    # optional:
    # checkerboard options:
    checkerboard_options = parser.add_argument_group('checkerboard options')

    checkerboard_options.add_argument("--color0",
        help = "color for the holes in the board",
        default = '#EEEEEE', dest = 'color0', metavar = 'color',
        type = str)

    checkerboard_options.add_argument("--color1",
        help = "first color for the checkerboard pattern",
        default = '#FFCE9E', dest = 'color1', metavar = 'color',
        type = str)

    checkerboard_options.add_argument("--color2",
        help = "second color for the checkerboard pattern",
        default = '#D18B47', dest = 'color2', metavar = 'color',
        type = str)


    # optional
    # outline options:
    outline_options = parser.add_argument_group('outline options')

    outline_options.add_argument("--outline-color",
        help = "color for the outer outline",
        default = '#000000', dest = 'outline_color', metavar = 'color',
        type = str)

    outline_options.add_argument("--outline-disable",
        help = "don't draw an outer outline",
        action = 'store_const', dest = 'outline_disable',
        const = True)


    # optional
    # tile options:
    tile_options = parser.add_argument_group('tile options')

    tile_options.add_argument('--tilesize',
        help = 'board square size',
        default = 42, dest = 'tilesize', metavar = 'int',
        type = int)

    tile_options.add_argument('--tileset',
        help ='where to look for piece tiles',
        default = 'Tiles/merida/42', dest = 'tileset', metavar = 'folder',
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

        # no tiles on board, fallback to the tilesize:
        if tilesize is None:
            tilesize = options.tilesize

        # calculate the image size:
        image_width = tilesize * board.width
        image_height = tilesize * board.height

        # add the border and the outline to the image size:
        border_size = 0
        outline_size = 0

        # calculate and add the border size:
        if not options.border_disable:
            border_font_size = calculate_border_font_size(tilesize)
            border_font = load_font(options.border_font, border_font_size)
            border_size = calculate_border_size(board, tilesize, border_font)

            image_width += (border_size * 2)
            image_height += (border_size * 2)

        # calculate and add the outline size:
        if not options.outline_disable:
            outline_size = calculate_outline_size(tilesize)

            image_width += (outline_size * 2)
            image_height += (outline_size * 2)

        # calculate the drawing offsets:
        outline_offset = (0, 0)
        border_offset = (outline_size, outline_size)
        board_offset = (outline_size + border_size, outline_size + border_size)

        # create the target image:
        image = make_base_image(image_width, image_height, options.border_color, options.outline_color, outline_size)

        # and draw on it:
        draw = BoardDraw(image, board, tilesize)
        draw.draw_checkerboard(board_offset, options.color0, options.color1, options.color2)

        # save to disk:
        image.save(options.filepath)

    except Exception as err:
        errln('{}'.format(err))
        status = 1

    sys.exit(status)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

