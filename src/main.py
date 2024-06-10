# module main

from argparse import ArgumentParser, Namespace

# In order to support multibyte strings, UTF-8 encoding is used; for locale-specific encoding,
# locale.getencoding() would have to be used instead
# https://docs.python.org/3/library/locale.html#locale.getencoding
ENCODING: str = "utf-8"

def get_num_bytes(filepath: str) -> int:
    # For reading and writing raw bytes use binary mode and leave encoding unspecified
    # https://docs.python.org/3/library/functions.html#open
    with open(filepath, "rb") as file:
        # NOTE: 06/10/24 - Reads the entire file into a single stream in memory, potentially
        #       problematic for very large files
        byte_data: bytes = file.read()
        num_bytes: int   = len(byte_data)

        # Alternatively, the file can be read in chunks to reduce memory load at the cost of some
        # performance
        # https://stackoverflow.com/questions/6787233/python-how-to-read-bytes-from-file-and-save-it

    return num_bytes

def get_num_chars(filepath: str) -> int:
    with open(filepath, "rb") as file:
        byte_data: bytes = file.read()
        utf_data:  str   = byte_data.decode(ENCODING)
        num_chars: int   = len(utf_data)

    return num_chars

def get_num_lines(filepath: str) -> int:
    with open(filepath, 'r', encoding=ENCODING) as file:
        num_lines: int = len(file.readlines())

    return num_lines

def get_num_words(filepath: str) -> int:
    with open(filepath, 'r', encoding=ENCODING) as file:
        # Read the entire file into a single string, then split by any whitespace character
        # (including `\n`, `\r`, `\t`, `\f`, and spaces) and remove empty strings

        # NOTE: 06/10/24 - Again there are potential memory issues with reading an entire file into
        #       a single string
        num_words: int = len(file.read().split())

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

    filepath: str = args.filepath

    if filepath is None:
        # TODO: 06/10/24 - Enable reading from stdin if no filename is provided
        print('No file path provided.')
        return

    if not any([args.bytes, args.chars, args.lines, args.words]):
        # If no arguments are provided, enable -c, -l and -w by default as in wc
        args.bytes = True
        args.lines = True
        args.words = True

    counts: dict = {'lines': None, 'words': None, 'chars': None, 'bytes': None}

    if args.bytes:
        counts['bytes'] = get_num_bytes(filepath)

    if args.chars:
        counts['chars'] = get_num_chars(filepath)

    if args.lines:
        counts['lines'] = get_num_lines(filepath)

    if args.words:
        counts['words'] = get_num_words(filepath)

    # The options are always printed in the following order: lines, words, chars, bytes (following
    # convention from wc)
    ordered_counts: list[int] = [counts[key] for key in ['lines', 'words', 'chars', 'bytes']
                                if counts[key] is not None]

    print(' '.join(map(str, ordered_counts)), filepath)

if __name__ == "__main__":
    main()
