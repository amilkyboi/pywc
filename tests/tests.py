# module tests

import sys
sys.path.append("../src")
import unittest

from main import get_num_bytes, get_num_lines, get_num_words, get_num_chars

FILEPATH: str = "../data/test.txt"

class TestFunctions(unittest.TestCase):
    def test_get_num_bytes(self):
        expected_bytes: int = 342190
        self.assertEqual(get_num_bytes(FILEPATH), expected_bytes)

    def test_get_num_chars(self):
        expected_chars: int = 339292
        self.assertEqual(get_num_chars(FILEPATH), expected_chars)

    def test_get_num_lines(self):
        expected_lines: int = 7145
        self.assertEqual(get_num_lines(FILEPATH), expected_lines)

    def test_get_num_words(self):
        expected_words: int = 58164
        self.assertEqual(get_num_words(FILEPATH), expected_words)

if __name__ == "__main__":
    unittest.main()
