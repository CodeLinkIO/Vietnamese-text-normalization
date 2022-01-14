import unittest
from vi_cleaner.letter_vi import normalize_letter_vi

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Normalize_Letter(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner("")
        self.letter_cases = [
            ("kí tự Z, chữ cái 'w', hình chữ S, chữ C viết hoa, chữ c viết thường", "kí tự dét, chữ cái 'vê kép', hình chữ ét, chữ xê viết hoa, chữ xê viết thường"),
            ("H 5 N 1", "hát 5 en nờ 1"),
            ("Anh Đ. cho biết anh cùng vợ và hai con là F 0", "Anh đê cho biết anh cùng vợ và hai con là ép 0"),
            ("máy bay B 52", "máy bay bê 52"),
        ]
        return super().setUp()

    def test_letter(self):
        for value, expected in self.letter_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_letter_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
