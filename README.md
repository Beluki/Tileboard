
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

## Status

This program is finished!

Tileboard is feature-complete and has no known bugs. Unless issues are reported
I plan no further development on it other than maintenance.

## License

Like all my hobby projects, this is Free Software. See the [Documentation][]
folder for more information. No warranty though.

[Documentation]: https://github.com/Beluki/Tileboard/tree/master/Documentation

