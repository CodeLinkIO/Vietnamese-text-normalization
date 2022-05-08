import unittest

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Normalize_Monthtime(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner()
        self.month_cases = [
            ("04/2021", "tháng tư năm hai nghìn không trăm hai mươi mốt"),
            ("04.2021", "tháng tư năm hai nghìn không trăm hai mươi mốt"),
            ("04-2021", "tháng tư năm hai nghìn không trăm hai mươi mốt"),
            ("tháng 4 năm nay", "tháng tư năm nay"),
            ("ngày 27/04/2001", "ngày hai mươi bảy tháng tư năm hai nghìn không trăm lẻ một"),
            ("vào ngày 27/04/2001, tôi sinh ra.",
             "vào ngày hai mươi bảy tháng tư năm hai nghìn không trăm lẻ một, tôi sinh ra."),
            ("hôm nay (2/4/2021), tôi đã được đi chơi.",
             "hôm nay (ngày hai tháng tư năm hai nghìn không trăm hai mươi mốt), tôi đã được đi chơi."),
        ]
        return super().setUp()

    def test_thang_bon_to_thang_tu(self):
        for value, expected in self.month_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = self.cleaner.clean_text(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
