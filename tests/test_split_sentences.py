import unittest
from vi_cleaner.abbreviation_vi import normalize_abbreviations_vi

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Split_Sentences(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner("")
        self.cases = [
            
        ]
        return super().setUp()

    def test_speacial_symbol_cases(self):
        for value, expected in self.cases:
            with self.subTest(value=value, expected=expected):
                actual = self.cleaner.split_sentences(value)
                self.assertEqual(len(actual[0]), len(expected[0]))


if __name__ == "__main__":
    unittest.main()
