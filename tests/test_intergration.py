import unittest

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Intergration(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.cleaner = ViCleaner("", ignore_ambiguity=False)
        self.letter_cases = [
            # ("đồng - kim lại quý", "đồng - kim lại quý"),
            # ("đồng-kim lại quý", "đồng kim lại quý"),
            ("63000 người sẽ tham gia hội nghị thượng đỉnh G7 sẽ diễn ra từ ngày 26-28/6/2022, lúc 8h,  có hơn 9.500 người tham dự",
             "sáu mươi ba nghìn người sẽ tham gia hội nghị thượng đỉnh gờ bảy sẽ diễn ra từ ngày hai mươi sáu đến ngày hai mươi tám tháng sáu năm hai nghìn không trăm hai mươi hai, lúc tám giờ, có hơn chín nghìn năm trăm người tham dự"),
        ]
        return super().setUp()

    def test_intergration(self):
        for value, expected in self.letter_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = self.cleaner.clean(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
