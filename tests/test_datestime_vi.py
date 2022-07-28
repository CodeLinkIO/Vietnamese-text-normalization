import unittest
from vi_cleaner.datestime_vi import normalize_date, normalize_time

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Normalize_DatesTime(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner()
        self.fulldate_cases = [
            ("27/02/2001", "ngày hai mươi bảy tháng hai năm hai nghìn không trăm lẻ một"),
            ("27.02.2001", "ngày hai mươi bảy tháng hai năm hai nghìn không trăm lẻ một"),
            ("27-02-2001", "ngày hai mươi bảy tháng hai năm hai nghìn không trăm lẻ một"),
            ("32/02/2001", "32/02/2001"),
            ("ngày 27/02/2001",
             "ngày hai mươi bảy tháng hai năm hai nghìn không trăm lẻ một"),
            ("Vào ngày 27/02/2001, tôi sinh ra.",
             "Vào ngày hai mươi bảy tháng hai năm hai nghìn không trăm lẻ một, tôi sinh ra."),
            ("Hôm nay (2/9/2021), tôi đã được đi chơi.",
             "Hôm nay (ngày hai tháng chín năm hai nghìn không trăm hai mươi mốt), tôi đã được đi chơi."),
        ]
        self.fulldate_range_cases = [
            ("27-28/02/2000",
             "ngày hai mươi bảy đến ngày hai mươi tám tháng hai năm hai nghìn"),
            ("ngày 27-28/02/2000",
             "ngày hai mươi bảy đến ngày hai mươi tám tháng hai năm hai nghìn"),
            ("Từ ngày 27-28/02/2000, tôi đã được đi chơi.",
             "Từ ngày hai mươi bảy đến ngày hai mươi tám tháng hai năm hai nghìn, tôi đã được đi chơi."),
        ]
        self.daymonth_cases = [
            ("ngày 27/02", "ngày hai mươi bảy tháng hai"),
            ("ngày 27.02", "ngày hai mươi bảy tháng hai"),
            ("ngày 27-02", "ngày hai mươi bảy tháng hai"),
            ("ngày 32/7", "ngày 32/7"),
            ("ngày 27/02", "ngày hai mươi bảy tháng hai"),
            ("Ngày sinh của tôi là ngày 27/2.",
             "Ngày sinh của tôi là ngày hai mươi bảy tháng hai."),
            ("0,5-1%", "0,5-1%"),
            ("hôm 17-7", "hôm ngày mười bảy tháng bảy"),
            ("đêm 17-7", "đêm ngày mười bảy tháng bảy")
        ]
        self.daymonth_range_cases = [
            ("1-2/12", "ngày một đến ngày hai tháng mười hai"),
            ("Từ ngày 1-2/09, tôi được nghỉ lễ.",
             "Từ ngày một đến ngày hai tháng chín, tôi được nghỉ lễ."),
            ("Từ đêm 16-17.12, có mưa, mưa nhỏ rải rác.",
             "Từ đêm ngày mười sáu đến ngày mười bảy tháng mười hai, có mưa, mưa nhỏ rải rác."),
            ("32-33/12", "32-33/12"),
        ]
        self.monthyear_cases = [
            ("02/2000", "tháng hai năm hai nghìn"),
            ("tháng 02/2000", "tháng hai năm hai nghìn"),
            ("02.2000", "tháng hai năm hai nghìn"),
            ("02-2000", "tháng hai năm hai nghìn"),
            ("13/2000", "13/2000"),
        ]
        self.monthyear_range_cases = [
            ("02-03/2000", "tháng hai đến tháng ba năm hai nghìn"),
            ("(02-03/2000)", "(tháng hai đến tháng ba năm hai nghìn)"),
            ("02-03.2000", "tháng hai đến tháng ba năm hai nghìn"),
            ("02-03-2000", "ngày hai tháng ba năm hai nghìn"),
            ("12-13/2000", "12-13/2000"),
        ]
        self.time_cases = [
            ("12:00", "mười hai giờ không phút"),
            ("12h00", "mười hai giờ không phút"),
            ("7h12", "bảy giờ mười hai phút"),
            ("17h30p", "mười bảy giờ ba mươi phút"),
            ("Vào lúc 12h27, tôi đi học.",
             "Vào lúc mười hai giờ hai mươi bảy phút, tôi đi học."),
            ("25:00", "25:00"),
            ("12:61", "12:61"),
            ("h12h12", "h12h12"),
        ]
        self.fulltime_cases = [
            ("12:00:00", "mười hai giờ không phút không giây"),
            ("12:30:20", "mười hai giờ ba mươi phút hai mươi giây"),
            ("26:62:20", "26:62:20"),
        ]
        self.quarter_month_years_cases = [
            ("quý 02/2021", "quý hai năm hai nghìn không trăm hai mươi mốt"),
            ("quý 02-2021", "quý hai năm hai nghìn không trăm hai mươi mốt"),
            ("quý 02.2021", "quý hai năm hai nghìn không trăm hai mươi mốt"),
            ("quý II/2021", "quý hai năm hai nghìn không trăm hai mươi mốt"),
            ("quý I-2021", "quý một năm hai nghìn không trăm hai mươi mốt"),
            ("quý III.2021", "quý ba năm hai nghìn không trăm hai mươi mốt"),
        ]
        return super().setUp()

    def test_fulldate(self):
        for value, expected in self.fulldate_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_date(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_fulldate_range(self):
        for value, expected in self.fulldate_range_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_date(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_daymonth(self):
        for value, expected in self.daymonth_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_date(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_daymonth_range(self):
        for value, expected in self.daymonth_range_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_date(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_monthyear(self):
        for value, expected in self.monthyear_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_date(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_monthyear_range(self):
        for value, expected in self.monthyear_range_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_date(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_time(self):
        for value, expected in self.time_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_time(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_fulltime(self):
        for value, expected in self.fulltime_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_time(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_quartermonthyear(self):
        for value, expected in self.quarter_month_years_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_date(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
