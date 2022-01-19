import unittest

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Intergration(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner("")
        self.letter_cases = [
            ("đồng - kim lại quý", "đồng - kim lại quý"),
            ("đồng-kim lại quý", "đồng kim lại quý"),
            ("Hội nghị thượng đỉnh G7 sẽ diễn ra từ ngày 26-28/6/2022", "hội nghị thượng đỉnh gờ bảy sẽ diễn ra từ ngày hai mươi sáu đến ngày hai mươi tám tháng sáu năm hai nghìn không trăm hai mươi hai"),
        ]
        return super().setUp()

    def test_intergration(self):
        for value, expected in self.letter_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = self.cleaner.clean_text(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
