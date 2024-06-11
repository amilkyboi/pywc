# module tests

import sys
sys.path.append("../src")
import unittest

from main import get_num_bytes, get_num_lines, get_num_words, get_num_chars

FILEPATH: str = "../data/test.txt"
ENCODING: str = "utf-8"

with open(FILEPATH, "rb") as file:
    byte_data = file.read()
    str_data  = byte_data.decode(ENCODING)

class TestFunctions(unittest.TestCase):
    def test_get_num_bytes(self):
        expected_bytes: int = 342190
        self.assertEqual(get_num_bytes(byte_data), expected_bytes)

    def test_get_num_chars(self):
        expected_chars: int = 339292
        self.assertEqual(get_num_chars(str_data), expected_chars)

    def test_get_num_lines(self):
        expected_lines: int = 7145
        self.assertEqual(get_num_lines(str_data), expected_lines)

    def test_get_num_words(self):
        expected_words: int = 58164
        self.assertEqual(get_num_words(str_data), expected_words)

if __name__ == "__main__":
    unittest.main()
