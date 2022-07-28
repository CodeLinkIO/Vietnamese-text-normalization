import unittest
from vi_cleaner.abbreviation_vi import normalize_abbreviations_vi, normalize_speacial_symbol_vi

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Normalize_Abbreviation(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner("")
        self.speacial_symbol_cases = [
            ("Tôi & em", "Tôi và em"),
            ("trong@gmail.com", "trong a còng gmail.com"),
            ("8 + 2", "8 cộng 2"),
        ]
        self.abbreviation_cases = [
            ("em ko bit, sao anh bik", "em không biết, sao anh biết"),
            ("v/v học sinh A", "về việc học sinh A"),
            ("gà, bò, chó...", "gà, bò, chó..."),
            ("K/g anh chị, đ/c mà chị gửi sai thì phải", "kính gửi anh chị, địa chỉ mà chị gửi sai thì phải"),
            ("kounde","kounde"),
            ("ko ko kook","không không kook")
        ]
        return super().setUp()

    def test_speacial_symbol_cases(self):
        for value, expected in self.speacial_symbol_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_speacial_symbol_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_abbreviation_cases(self):
        for value, expected in self.abbreviation_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_abbreviations_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
