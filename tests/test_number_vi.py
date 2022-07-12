import unittest
from vi_cleaner.numberical_vi import normalize_number_vi
from vi_cleaner.roman_number_vi import normalize_roman_numbers

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Normalize_Number(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner("")
        self.normal_number_cases = [
            ("1", "một"),
            ("-1", "âm một"),
            ("12", "mười hai"),
            ("123", "một trăm hai mươi ba"),
            ("03", "ba"),
            ("Tôi có 9999 cái áo.", "Tôi có chín nghìn chín trăm chín mươi chín cái áo."),
        ]
        self.number_with_dot_cases = [
            ("1.000", "một nghìn"),
            ("-1.000", "âm một nghìn"),
            ("1.123", "một nghìn một trăm hai mươi ba"),
            ("1.000.000.000", "một tỷ"),
            ("Tôi có 9.000.000 đồng.", "Tôi có chín triệu đồng."),
            ("Tôi có 9.999 cái áo.", "Tôi có chín nghìn chín trăm chín mươi chín cái áo."),
        ]
        self.number_with_space_cases = [
            ("1 000", "một nghìn"),
            ("1 123", "một nghìn một trăm hai mươi ba"),
            ("2 000 000 000", "hai tỷ"),
            ("Tôi có 9 000 000 đồng.", "Tôi có chín triệu đồng."),
            ("Tôi có 9 999 cái áo.", "Tôi có chín nghìn chín trăm chín mươi chín cái áo."),
        ]
        self.float_number_cases = [
            ("1,23", "một phẩy hai mươi ba"),
            ("1,002", "một phẩy không không hai"),
            ("0,02", "không phẩy không hai"),
            ("-2,7", "âm hai phẩy bảy"),
        ]
        self.ordinal_cases = [
            ("xếp hạng 1", "xếp hạng nhất"),
            ("về thứ 4", "về thứ tư"),
        ]
        self.phone_number_cases = [
            ("SĐT: 0987654321", "SĐT: không chín tám bảy sáu năm bốn ba hai một"),
            ("Liên hệ: +84987654321", "Liên hệ: không chín tám bảy sáu năm bốn ba hai một"),
            ("Liên hệ: +84987654321, ĐC: 108 Hùng Vương", "Liên hệ: không chín tám bảy sáu năm bốn ba hai một, ĐC: một trăm lẻ tám Hùng Vương"),
        ]
        self.multiphy_number_cases = [
            ("Mảnh đất có diện tích 8x8 mét vuông", "Mảnh đất có diện tích tám nhân tám mét vuông"),
            ("Hình chữ nhật 5 x 10", "Hình chữ nhật năm nhân mười"),
        ]
        self.range_number_cases = [
            ("từ 1-2", "từ một đến hai"),
            ("còn 1-3", "còn một đến ba")
        ]
        self.roman_number_cases = [
            ("XI", "mười một"),
            ("số I", "số một"),
            ("thế kỉ XXI", "thế kỉ hai mươi mốt"),
            ("chữ V", "chữ v"),
        ]

        return super().setUp()

    def test_normal_number_cases(self):
        for value, expected in self.normal_number_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_number_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_number_with_dot_cases(self):
        for value, expected in self.number_with_dot_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_number_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_number_with_space_cases(self):
        for value, expected in self.number_with_space_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_number_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_float_number_cases(self):
        for value, expected in self.float_number_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_number_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_ordinal_cases(self):
        for value, expected in self.ordinal_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_number_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_phone_number_cases(self):
        for value, expected in self.phone_number_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_number_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_multiphy_number_cases(self):
        for value, expected in self.multiphy_number_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_number_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_range_number_cases(self):
        for value, expected in self.range_number_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_number_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_roman_number_cases(self):
        for value, expected in self.roman_number_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_roman_numbers(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
