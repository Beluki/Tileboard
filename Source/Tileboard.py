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


# All the exceptions Tileboard raises are of this type:

class TileboardError(Exception):
    pass


# Board representation:

class Board(object):
    """
    Create a Board from a FEN position.
    """
    def __init__(self, position):
        self.validate_position(position)

        self.rows = self.expand_position_numbers(position).split('/')
        self.width = max(map(len, self.rows))
        self.height = len(self.rows)

        # fill with zeros (holes) to make sure that all the rows
        # have the same length:
        self.rows = [row.ljust(self.width, '0') for row in self.rows]

    def validate_position(self, position):
        """
        Check that a FEN position has rows and contains valid characters.
        """
        has_rows = False

        for character in position:
           if not character == '/':
                has_rows = True

        if not has_rows:
            raise TileboardError('Empty FEN position.')

    def expand_position_numbers(self, position):
        """ Replace numbers from 1..9 with as much spaces as the number value. """
        return re.sub('[1-9]', lambda match: ' ' * int(match.group(0)), position)


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


# Loading fonts:

def load_font(filepath, size):
    """
    Load a truetype font.
    """
    try:
        return ImageFont.truetype(filepath, size)

    except Exception as err:
        raise TileboardError('Unable to load font: {}'.format(filepath))


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


# Drawing:

def draw_rectangle_outline(image, x1, y1, x2, y2, width, color):
    """
    Draw a rectangle outline.
    """
    draw = ImageDraw.Draw(image)

    # top left -> bottom left
    rect = [x1, y1, x1 + width, y2]
    draw.rectangle(rect, fill = color)

    # top left -> top right
    rect = [x1, y1, x2, y1 + width]
    draw.rectangle(rect, fill = color)

    # top right -> bottom right
    rect = [x2, y1, x2 - width, y2]
    draw.rectangle(rect, fill = color)

    # bottom left -> bottom right
    rect = [x1, y2, x2, y2 - width]
    draw.rectangle(rect, fill = color)

    del draw


def draw_checkerboard_holes(image, xy, board, tilesize, color0):
    """
    Draw the background (holes) as a single rectangle.
    """
    draw = ImageDraw.Draw(image)
    xoffset, yoffset = xy

    x1 = xoffset
    y1 = yoffset
    x2 = x1 + (tilesize * board.width) - 1
    y2 = y1 + (tilesize * board.height) - 1

    draw.rectangle([x1, y1, x2, y2], fill = color0)
    del draw


def draw_checkerboard_pattern(image, xy, board, tilesize, color1, color2):
    """
    Draw a checkerboard pattern.
    """
    draw = ImageDraw.Draw(image)
    xoffset, yoffset = xy

    for tile, row, col in walk_rows(board):
        x1 = xoffset + (col * tilesize)
        y1 = yoffset + (row * tilesize)
        x2 = x1 + tilesize - 1
        y2 = y1 + tilesize - 1

        if (col % 2) == (row % 2):
            color = color1
        else:
            color = color2

        draw.rectangle([x1, y1, x2, y2], color)

    del draw


def draw_pieces(image, xy, board, tilesize, tileset):
    """
    Draw all the board pieces.
    """
    xoffset, yoffset = xy

    for piece, row, col in walk_rows_pieces(board):
        tile = tileset[piece]
        alpha = tile.split()[3]

        x1 = xoffset + (col * tilesize)
        y1 = yoffset + (row * tilesize)

        image.paste(tile, (x1, y1), alpha)


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

    checkerboard_options.add_argument("--checkerboard-color1",
        help = "first color for the checkerboard pattern",
        default = '#FFCE9E', dest = 'checkerboard_color1', metavar = 'color',
        type = str)

    checkerboard_options.add_argument("--checkerboard-color2",
        help = "second color for the checkerboard pattern",
        default = '#D18B47', dest = 'checkerboard_color2', metavar = 'color',
        type = str)

    checkerboard_options.add_argument('--checkerboard-disable',
        help ='do not draw a checkerboard pattern',
        action = 'store_const', dest = 'checkerboard_disable',
        const = True)

    checkerboard_options.add_argument("--checkerboard-holes-color",
        help = "color for the holes in the board",
        default = '#EEEEEE', dest = 'checkerboard_holes_color', metavar = 'color',
        type = str)

    checkerboard_options.add_argument('--checkerboard-holes-disable',
        help ='do not draw the checkerboard holes (keep them transparent)',
        action = 'store_const', dest = 'checkerboard_holes_disable',
        const = True)


    # optional
    # outer outline options:
    outer_outline_options = parser.add_argument_group('outer outline options')

    outer_outline_options.add_argument("--outer-outline-color",
        help = "color for the outer outline",
        default = '#000000', dest = 'outer_outline_color', metavar = 'color',
        type = str)

    outer_outline_options.add_argument("--outer-outline-disable",
        help = "don't draw an outer outline",
        action = 'store_const', dest = 'outer_outline_disable',
        const = True)


    # optional
    # inner outline options:
    inner_outline_options = parser.add_argument_group('inner outline options')

    inner_outline_options.add_argument("--inner-outline-color",
        help = "color for the inner outline",
        default = '#000000', dest = 'inner_outline_color', metavar = 'color',
        type = str)

    inner_outline_options.add_argument("--inner-outline-disable",
        help = "don't draw an inner outline",
        action = 'store_const', dest = 'inner_outline_disable',
        const = True)


    # optional
    # tile options:
    tileset_options = parser.add_argument_group('tileset options')

    tileset_options.add_argument('--tileset-folder',
        help ='where to look for piece tiles',
        default = 'Tiles/merida/42', dest = 'tileset_folder', metavar = 'folder',
        type = str)

    tileset_options.add_argument('--tileset-size',
        help = 'board square size',
        default = 42, dest = 'tileset_size', metavar = 'int',
        type = int)

    tileset_options.add_argument("--tileset-disable",
        help = "don't draw tiles",
        action = 'store_const', dest = 'tileset_disable',
        const = True)

    return parser


# Entry point:

def main():
    parser = make_parser()
    options = parser.parse_args()
    status = 1

    try:
        # load resources:
        board = Board(options.position)
        tileset = load_tileset(board, options.tileset_folder)

        # determine the base tile size:
        tilesize = validate_tile_sizes(tileset.values())

        # no tiles on board, fallback to the tilesize specified in options:
        if tilesize is None:
            tilesize = options.tileset_size

        # calculate the image size:
        image_width = tilesize * board.width
        image_height = tilesize * board.height

        # add the border and the outlines to the image size:
        outer_outline_size = 0
        border_size = 0
        inner_outline_size = 0

        # calculate and add the outer outline size:
        if not options.outer_outline_disable:
            outer_outline_size = calculate_outline_size(tilesize)

            image_width += (outer_outline_size * 2)
            image_height += (outer_outline_size * 2)

        # calculate and add the border size:
        if not options.border_disable:
            border_font_size = calculate_border_font_size(tilesize)
            border_font = load_font(options.border_font, border_font_size)
            border_size = calculate_border_size(board, tilesize, border_font)

            image_width += (border_size * 2)
            image_height += (border_size * 2)

        # calculate and add the inner outline size:
        if not options.inner_outline_disable:
            inner_outline_size = calculate_outline_size(tilesize)

            image_width += (inner_outline_size * 2)
            image_height += (inner_outline_size * 2)

        # calculate the drawing offsets:
        outer_outline_offset = (0, 0)
        border_offset = (outer_outline_size, outer_outline_size)
        inner_outline_offset = (outer_outline_size + border_size, outer_outline_size + border_size)
        board_offset = (outer_outline_size + border_size + inner_outline_size, outer_outline_size + border_size + inner_outline_size)

        # create the base image, transparent:
        image = Image.new('RGBA', (image_width, image_height))

        # start drawing:

        # outer outline:
        if not options.outer_outline_disable:
            draw_rectangle_outline(image,
                0,
                0,
                image_width - 1,
                image_height - 1,
                outer_outline_size - 1,
                options.outer_outline_color)

        # border:
        if not options.border_disable:
            draw_rectangle_outline(image,
                outer_outline_size,
                outer_outline_size,
                image_width - outer_outline_size - 1,
                image_height - outer_outline_size - 1,
                border_size - 1,
                options.border_color)

        # inner outline:
        if not options.inner_outline_disable:
            draw_rectangle_outline(image,
                outer_outline_size + border_size,
                outer_outline_size + border_size,
                image_width - outer_outline_size - border_size - 1,
                image_height - outer_outline_size - border_size - 1,
                inner_outline_size - 1,
                options.inner_outline_color)

        # checkerboard holes:
        if not options.checkerboard_holes_disable:
            draw_checkerboard_holes(image,
                board_offset,
                board,
                tilesize,
                options.checkerboard_holes_color)

        # checkerboard:
        if not options.checkerboard_disable:
            draw_checkerboard_pattern(image,
                board_offset,
                board,
                tilesize,
                options.checkerboard_color1,
                options.checkerboard_color2)

        # pieces:
        if not options.tileset_disable:
            draw_pieces(image,
                board_offset,
                board,
                tilesize,
                tileset)

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

