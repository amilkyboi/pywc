# module main

import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace

# In order to support multibyte strings, UTF-8 encoding is used; for locale-specific encoding,
# locale.getencoding() would have to be used instead
# https://docs.python.org/3/library/locale.html#locale.getencoding
ENCODING: str = "utf-8"

def get_num_bytes(byte_data: bytes) -> int:
    num_bytes: int = len(byte_data)

    return num_bytes

def get_num_chars(str_data: str) -> int:
    # TODO: 06/10/24 - If the current locale does not support multibyte characters this should match
    #       the number of bytes
    num_chars: int = len(str_data)

    return num_chars

def get_num_lines(str_data: str) -> int:
    num_lines: int = len(str_data.splitlines())

    return num_lines

def get_num_words(str_data: str) -> int:
    # Split by any whitespace character (including `\n`, `\r`, `\t`, `\f`, and spaces) and remove
    # empty strings
    num_words: int = len(str_data.split())

    return num_words

def main() -> None:
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("-c", "--bytes", help="print the byte counts",      action="store_true")
    parser.add_argument("-m", "--chars", help="print the character counts", action="store_true")
    parser.add_argument("-l", "--lines", help="print the newline counts",   action="store_true")
    parser.add_argument("-w", "--words", help="print the word counts",      action="store_true")
    # The `nargs='?'` means one argument will be consumed from the command line if possible; if no
    # command-line argument is present, the value from default will be produced
    # https://docs.python.org/3/library/argparse.html#nargs
    parser.add_argument("filepath", help="location of the file", nargs='?', type=str, default=None)

    args: Namespace = parser.parse_args()

    str_data:  str
    byte_data: bytes

    # Read from standard input if no filepath is specified
    if args.filepath is None:
        # NOTE: 06/11/24 - Reads the entire stdin into a single stream in memory, potentially
        #       problematic for very large files
        str_data  = sys.stdin.read()
        byte_data = str_data.encode(ENCODING)
    else:
        filepath: Path = Path(args.filepath)

        # Ensure the requested filepath exists
        if not filepath.exists():
            print(f"ERROR: {filepath} not found")
            sys.exit(1)

        # Ensure the requested filepath is a file (or symlink)
        if not filepath.is_file():
            print(f"ERROR: {filepath} is not a file")
            sys.exit(1)

        # For reading and writing raw bytes use binary mode and leave encoding unspecified
        # https://docs.python.org/3/library/functions.html#open
        with open(filepath, "rb") as file:
            # NOTE: 06/11/24 - Reads the entire file into a single stream in memory, potentially
            #       problematic for very large files (think about reading in chunks)
            byte_data = file.read()
            str_data  = byte_data.decode(ENCODING)

    if not any([args.bytes, args.chars, args.lines, args.words]):
        # If no arguments are provided, enable -c, -l and -w by default as in wc
        args.bytes = True
        args.lines = True
        args.words = True

    counts: dict = {"lines": None, "words": None, "chars": None, "bytes": None}

    if args.bytes:
        counts["bytes"] = get_num_bytes(byte_data)

    if args.chars:
        counts["chars"] = get_num_chars(str_data)

    if args.lines:
        counts["lines"] = get_num_lines(str_data)

    if args.words:
        counts["words"] = get_num_words(str_data)

    # The options are always printed in the following order: lines, words, chars, bytes (following
    # convention from wc)
    ordered_counts: list[int] = [counts[key] for key in ["lines", "words", "chars", "bytes"]
                                 if counts[key] is not None]

    if args.filepath is None:
        print(' '.join(map(str, ordered_counts)))
    else:
        print(' '.join(map(str, ordered_counts)), args.filepath)

if __name__ == "__main__":
    main()
