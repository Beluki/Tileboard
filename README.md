
## About

Tileboard is a small command-line program that generates board game diagrams.
You write positions in [FEN][] and a image comes out ready to be posted in a blog
or any other media.

[FEN]: https://en.wikipedia.org/wiki/Forsyth-Edwards_Notation

For example, the initial chess position:

```bash
$ Tileboard.py rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR chess.png
```

Generates the following image:

![Screenshot1](Screenshot/Screenshot1.png)

## Installation

I've used Python 3.5.0 and [Pillow 3.1.0][] to develop Tileboard.
It's likely that it will work with older versions of Python 3.x
(back to 3.3 or so) or with Pillow 2.x.

Python 2.x is not supported.

[Pillow 3.1.0]: https://pypi.python.org/pypi/Pillow/3.1.0

## Features

Although the basic syntax is: `Tileboard.py position filepath`, Tileboard
has a metric ton of command-line options to customize the output.

Instead of a boring list (see `--help`), I'll just put example screenshots
in the readme with the command-line options that generated them.

## Examples

Let's start with pretty colors. Tileboard is easily themable. The following colors
are copied from one of my favorite chess programs, [Lucas Chess][].

[Lucas Chess]: https://www-lucaschess.rhcloud.com/index.html

![Screenshot2](Screenshot/Screenshot2.png)

To mark interesting positions, available piece moves, or other situations
on the board you can place dots and crosses in any given coordinates:

![Screenshot3](Screenshot/Screenshot3.png)

The FEN notation is extended in various useful ways. For example, you can use
any number of board rows or columns instead of 8x8. From 1x1 up to any size.
It's also possible to use a different number of rows and columns.

Here are some small chess variants:

![Screenshot4](Screenshot/Screenshot4.png)

As well as a (completely made-up) board that
goes beyond `z` and `9` in the borders:

![Screenshot5](Screenshot/Screenshot5.png)

Another interesting addition to the FEN notation is that you can use zeros
to represent holes in the board. This makes it possible to draw games such
as [Cam][] or [Amazons][] which use irregular boards:

[Cam]: http://www.worldcamelotfederation.com
[Amazons]: https://en.wikipedia.org/wiki/Game_of_the_Amazons

![Screenshot6](Screenshot/Screenshot6.png)

Note: you can skip trailing zeros in a given position.
For example the positions: `00ppp0000` and: `00ppp` are identical when the
board has 9 columns.

## Sizes and tilesets

The final image size depends on the size of each piece in the board.
Tileboard can use any size as long as all the pieces are squares of the same size.
The short version is: it can generate small images for your blog or huge images
that won't even fit on a monitor.

Everything else in the image, such as the outlines, border coordinates,
the checkerboard or the crosses and dots is scaled automatically:

![Screenshot7](Screenshot/Screenshot7.png)

Included in the distribution are three high-quality tilesets for chess,
with sizes ranging from 20x20 px to 300x300 px made by [Eric de Mund][] for the
Jin chess program.

[Eric de Mund]: http://ixian.com/chess/jin-piece-sets

They look like this:

![Screenshot8](Screenshot/Screenshot8.png)

## Beyond chess

Tilesets in Tileboard are not hardcoded. They just follow a very simple rule.
Each letter in a FEN position is translated to a filename, prepended with
`l` or `u` depending on whether it's lowercase/uppercase in the position.

For example, the [/Source/Tiles/merida/42][] folder contains the files (those
are just .png images without the extension):

```
lb  lk  ln  lp  lq  lr  ub  uk  un  up  uq  ur
```

If a letter has no different lowercase/uppercase representation (e.g: `#` or
unicode symbols), no prefix is needed. No extension either, because Pillow
detects it (you can mix formats).

Here are two examples (the tiles are included in the [/Tools/checkers][] folder):

![Screenshot9](Screenshot/Screenshot9.png)

[/Source/Tiles/merida/42]: Source/Tiles/merida/42
[/Tools/checkers]: Tools/checkers

In fact, you can think of Tileboard as a paint program that draws sprites instead
of pixels, with a single layer. Here's a more crazy example (the tiles are included
in the [/Tools/freegemas][] folder):

![Screenshot10](Screenshot/Screenshot10.png)

[/Tools/freegemas]: Tools/freegemas

## Performance and memory usage

The only limitation on how big the output image can be is the memory available.
Internally, Tileboard draws everything using offsets on a single image.
It caches pieces, dots and crosses.

In practice, this means that on a decent machine you can draw huge images
without issues. I've used it to draw at resolutions up to more than
20.000x20.000 px.

As a guideline, generating a blank board at 1000x1000 px each tile
takes 3 seconds on an Intel i5 3.5 ghz and needs about 400 mb of memory
resulting in a 9040x9040 px image.

```bash
$ Tileboard.py 8/8/8/8/8/8/8/8 blank.png --tileset-size 1000
```

## Tileboard + ImageMagick

I deliberately avoided adding features that would bloat the program if they
could be done in a single command in [ImageMagick][]. One such example is text
below the images (e.g. "White to play and win").

[ImageMagick]: http://imagemagick.org

Almost all of the images in this README have labels below them. Take a look
at [generate-screenshots.sh][] for the script that generated them. I'm not
proficient in either bash or ImageMagick but it worked fine.

[generate-screenshots.sh]: Tools/generate-screenshots.sh

## Portability

Information and error messages are written to stdout and stderr
respectively, using the current platform newline format and encoding.

The exit status is 0 on success and 1 on errors.

Tileboard is tested on Windows 7 and 8 and on Debian (both x86 and x86-64).

The tilesets and output images can use any format that Pillow supports.

## Status

This program is finished!

Tileboard is feature-complete and has no known bugs. Unless issues are reported
I plan no further development on it other than maintenance.

## License

Like all my hobby projects, this is Free Software. See the [Documentation][]
folder for more information. No warranty though.

[Documentation]: Documentation

