# module main

FILEPATH: str = "../data/test.txt"
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

def get_num_chars(filepath: str) -> int:
    with open(filepath, "rb") as file:
        byte_data: bytes = file.read()
        utf_data:  str   = byte_data.decode(ENCODING)
        num_chars: int   = len(utf_data)

    return num_chars

def main() -> None:
    print(f"bytes: {get_num_bytes(FILEPATH)}")
    print(f"lines: {get_num_lines(FILEPATH)}")
    print(f"words: {get_num_words(FILEPATH)}")
    print(f"chars: {get_num_chars(FILEPATH)}")

if __name__ == "__main__":
    main()
