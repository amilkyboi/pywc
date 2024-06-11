# module main
"""
An implementation of GNU wc in Python.
"""

import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace

# In order to support multibyte strings, UTF-8 encoding is used; for locale-specific encoding,
# locale.getencoding() would have to be used instead
# https://docs.python.org/3/library/locale.html#locale.getencoding
ENCODING: str = "utf-8"

def get_num_bytes(byte_data: bytes) -> int:
    """
    Returns the number of bytes in a byte stream.
    """

    return len(byte_data)

def get_num_chars(str_data: str) -> int:
    """
    Returns the number of characters in a string stream.
    """

    # TODO: 06/10/24 - If the current locale does not support multibyte characters this should match
    #       the number of bytes
    return len(str_data)

def get_num_lines(str_data: str) -> int:
    """
    Returns the number of lines in a string stream.
    """

    return len(str_data.splitlines())

def get_num_words(str_data: str) -> int:
    """
    Returns the number of words in a string stream.
    """

    # Split by any whitespace character (including `\n`, `\r`, `\t`, `\f`, and spaces) and remove
    # empty strings
    return len(str_data.split())

def get_args() -> Namespace:
    """
    Returns all possible command line arguments.
    """

    parser: ArgumentParser = ArgumentParser(
                                prog="pywc",
                                description="Print lines, words, and bytes for the specified file.")

    parser.add_argument("-c", "--bytes", help="print the byte counts",      action="store_true")
    parser.add_argument("-m", "--chars", help="print the character counts", action="store_true")
    parser.add_argument("-l", "--lines", help="print the newline counts",   action="store_true")
    parser.add_argument("-w", "--words", help="print the word counts",      action="store_true")
    # The `nargs='*'` means all command-line arguments present are gathered into a list
    # https://docs.python.org/3/library/argparse.html#nargs
    parser.add_argument("filepaths", help="location of the file(s)", nargs='*')

    return parser.parse_args()

def get_ordered_counts(args: Namespace, byte_data: bytes, str_data: str) -> list[int]:
    """
    Returns the number of lines, words, chars, bytes, in that order.
    """

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

    # The options are always printed in the following order: lines, words, chars, bytes
    # (following convention from wc)
    return [counts[key] for key in ["lines", "words", "chars", "bytes"] if counts[key] is not None]

def parse_from_files(args: Namespace) -> None:
    """
    Parses data from files.
    """

    file_strs: list[str] = args.filepaths

    for file_str in file_strs:
        file_path: Path = Path(file_str)

        # Ensure the requested filepath exists
        if not file_path.exists():
            print(f"ERROR: {file_path} not found")
            sys.exit(1)

        # Ensure the requested filepath is a file (or symlink)
        if not file_path.is_file():
            print(f"ERROR: {file_path} is not a file")
            sys.exit(1)

        # For reading and writing raw bytes use binary mode and leave encoding unspecified
        # https://docs.python.org/3/library/functions.html#open
        with open(file_path, "rb") as file:
            # NOTE: 06/11/24 - Reads the entire file into a single stream in memory, potentially
            #       problematic for very large files (think about reading in chunks)
            byte_data = file.read()
            str_data  = byte_data.decode(ENCODING)

        ordered_counts: list[int] = get_ordered_counts(args, byte_data, str_data)

        print(' '.join(map(str, ordered_counts)), file_path)

def parse_from_stdin(args: Namespace) -> None:
    """
    Parses data from stdin.
    """

    str_data  = sys.stdin.read()
    byte_data = str_data.encode(ENCODING)

    ordered_counts: list[int] = get_ordered_counts(args, byte_data, str_data)

    print(' '.join(map(str, ordered_counts)))

def main() -> None:
    """
    Runs the program.
    """

    args: Namespace = get_args()

    # Read from standard input if no filepaths are specified
    if not args.filepaths:
        # NOTE: 06/11/24 - Reads the entire stdin into a single stream in memory, potentially
        #       problematic for very large files
        try:
            parse_from_stdin(args)
        except KeyboardInterrupt:
            # Behaves the same as wc if no input is piped into it
            sys.exit(1)
    else:
        # TODO: 06/11/24 - Align the columns of output and display the total number of lines, words,
        #       chars, and bytes
        parse_from_files(args)

if __name__ == "__main__":
    main()
