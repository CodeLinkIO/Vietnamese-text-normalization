import unittest
from vi_cleaner.currency_vi import normalize_currency_vi

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Normalize_Currency(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner("")
        self.common_currency_cases = [
            ("8usd", "8đô la"),
            ("đồng usd có dấu hiệu tăng", "đồng đô la có dấu hiệu tăng"),
            ("đồng eur có dấu hiệu giảm", "đồng ơ rô có dấu hiệu giảm"),
            ("100 000 VND", "100 000 đồng"),
            ("100 euro", "100 ơ rô"),
            ("100 $", "100 đô la"),
            ("11,085,306 VND", "11,085,306 đồng"),
            ("100 000 ndt", "100 000 nhân dân tệ")
        ]
        self.not_currency_cases = [
            ("tháng 8 đến tháng 9", "tháng 8 đến tháng 9"),
            ("$$$", "$$$"),
        ]
        return super().setUp()

    def test_currency(self):
        for value, expected in self.common_currency_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_currency_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_not_currency(self):
        for value, expected in self.not_currency_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_currency_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
