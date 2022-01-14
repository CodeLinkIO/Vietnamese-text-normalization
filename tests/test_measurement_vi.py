import unittest
from vi_cleaner.measurement_vi import normalize_measurement_vi

from vi_cleaner.vi_cleaner import ViCleaner


class Test_Normalize_Measurement(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = ViCleaner("")
        self.measurement_cases = [
            ("8cm", "8 xen ti mét"),
            ("Khối sapphire nặng 310 kg", "Khối sapphire nặng 310 ki lô gam"),
            ("Hầu hết TV ngày nay đều đạt thông số là 60 Hz và 120 Hz", "Hầu hết TV ngày nay đều đạt thông số là 60 héc và 120 héc"),
            ("Mỗi lần hiến máu toàn phần không quá 250 ml", "Mỗi lần hiến máu toàn phần không quá 250 mi li lít"),
            ("Thu hồi hơn 81.000 m2 đất xây dựng đường vành đai, kế bên khu đất 43 ha", "Thu hồi hơn 81.000 mét vuông đất xây dựng đường vành đai, kế bên khu đất 43 héc ta"),
            ("Lúc 8h", "Lúc 8 giờ"),
            ("Khoảng 20p", "Khoảng 20 phút"),
            ("Tôi chỉ mất có 5s", "Tôi chỉ mất có 5 giây"),
            ("Tôi có RAM 8GB", "Tôi có RAM 8 gi ga bai"),
            ("gps", "gps"),
        ]
        self.measurement_with_splash_cases = [
            ("Với nồng độ cồn 0,751 mg/l khí thở", "Với nồng độ cồn 0,751 mi li gam trên lít khí thở"),
            ("0,751 mg/L", "0,751 mi li gam trên lít"),
            ("Chạy xe với tốc độ 300 km/h nhanh cỡ nào?", "Chạy xe với tốc độ 300 ki lô mét trên giờ nhanh cỡ nào?"),
        ]
        return super().setUp()

    def test_measurement(self):
        for value, expected in self.measurement_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_measurement_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)

    def test_measurement_with_splash(self):
        for value, expected in self.measurement_with_splash_cases:
            with self.subTest(value=value, expected=expected):
                value = self.cleaner.clean_basic(value)
                actual = normalize_measurement_vi(value)
                actual = self.cleaner.collapse_whitespace(actual)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
