import unittest
from vi_cleaner.acronym_vi import spell_acronyms_vi

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Normalize_Acronym(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner("")
        self.acronym_cases = [
            ("UBND TPHCM, TP.HCM, Thành Phố HCM", "uỷ ban nhân dân thành phố hồ chí minh, thành phố hồ chí minh, Thành Phố hồ chí minh"),
            ("Trường ĐH Quốc tế dành 80% chỉ tiêu xét điểm tốt nghiệp THPT", "Trường đại học Quốc tế dành 80% chỉ tiêu xét điểm tốt nghiệp trung học phổ thông"),
            ("UBND tỉnh, Trưởng BTC Giải bóng đá trao cho CLB Bắc Kạn", "uỷ ban nhân dân tỉnh, Trưởng ban tổ chức Giải bóng đá trao cho câu lạc bộ Bắc Kạn"),
            ("TTTM Sài Gòn","trung tâm thương mại Sài Gòn"),
            ("WTO, IQ, EQ, BBC, GPRS", "W T O, I Q, E Q, B B C, G P R S"),
            ("PSG","PSG"),
            ("COVID-19","cô vít-19"),
            ("có 1-0-2", "có một không hai")
        ]
        return super().setUp()

    def test_acronym(self):
        for value, expected in self.acronym_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = spell_acronyms_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
