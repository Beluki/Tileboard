
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

![Screenshot1](https://raw.github.com/Beluki/Tileboard/master/Screenshot/Screenshot1.png)

## Installation

I've used Python 3.5.0 and [Pillow 3.1.0][] to develop Tileboard. It's likely that it
will work with older versions of Python 3.x (back to 3.3 or so) or Pillow 2.x.

Python 2.x is not supported.

[Pillow 3.1.0]: https://pypi.python.org/pypi/Pillow/3.1.0

## Features

Although the basic syntax is: `Tileboard.py position filepath`, Tileboard
has a metric ton of command-line options to customize the output.

Instead of a boring list (see --help), I'll just put example screenshots in the readme
with the command-line options that generated them.

## Examples

Let's start with pretty colors. Tileboard is easily themable. The following colors
are copied from one of my favorite chess programs, [Lucas Chess][].

[Lucas Chess]: https://www-lucaschess.rhcloud.com/index.html

![Screenshot2](https://raw.github.com/Beluki/Tileboard/master/Screenshot/Screenshot2.png)

To mark interesting positions, available piece moves, or other situations on the board
you can place dots and crosses in any given coordinates:

![Screenshot3](https://raw.github.com/Beluki/Tileboard/master/Screenshot/Screenshot3.png)

The FEN notation is extended in various useful ways. For example, you can use any number
of board rows or columns instead of 8x8. From 1x1 up to any size. It's also possible to
use a different number of rows and columns.

Here are some small chess variants:

![Screenshot4](https://raw.github.com/Beluki/Tileboard/master/Screenshot/Screenshot4.png)

As well as a (completely made-up) board that goes beyond 'z' and '9' in the borders:

![Screenshot5](https://raw.github.com/Beluki/Tileboard/master/Screenshot/Screenshot5.png)

Another interesting addition to the FEN notation is that you can use zeros to represent holes
in the board. This makes it possible to draw games such as [Cam][] or [Amazons][] which use
irregular boards:

[Cam]: http://www.worldcamelotfederation.com
[Amazons]: https://en.wikipedia.org/wiki/Game_of_the_Amazons

![Screenshot6](https://raw.github.com/Beluki/Tileboard/master/Screenshot/Screenshot6.png)

## Status

This program is finished!

Tileboard is feature-complete and has no known bugs. Unless issues are reported
I plan no further development on it other than maintenance.

## License

Like all my hobby projects, this is Free Software. See the [Documentation][]
folder for more information. No warranty though.

[Documentation]: https://github.com/Beluki/Tileboard/tree/master/Documentation

