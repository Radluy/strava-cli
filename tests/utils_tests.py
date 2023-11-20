import unittest
import datetime

from src import utils


class TestStripAccents(unittest.TestCase):
    def test_without_accents(self):
        string = 'test_string_without_accents'
        stripped = utils.strip_accents(string)
        self.assertEqual(string, stripped)

    def test_slovak_accents(self):
        string = 'ľščťžýáíéúäôň'
        expected_result = 'lsctzyaieuaon'
        stripped = utils.strip_accents(string)
        self.assertEqual(stripped, expected_result)

    def test_non_alfanumeric(self):
        string = '|#$asdf%^'
        stripped = utils.strip_accents(string)
        self.assertEqual(string, stripped)

    def test_unicode_emoji(self):
        string = "\"taper\" 🤓"
        stripped = utils.strip_accents(string)
        self.assertEqual(string, stripped)

    def test_numbers(self):
        string = '123456789'
        stripped = utils.strip_accents(string)
        self.assertEqual(string, stripped)


class TestSpeedToPace(unittest.TestCase):
    def test_zero_speed(self):
        speed = 0
        result = utils.speed_to_pace(speed)
        self.assertEqual(result, 0)

    def test_non_int(self):
        speed = 'abc'
        try:
            utils.speed_to_pace(speed)
        except TypeError:
            pass

    def test_correct_speed(self):
        speed = 2.91
        result = utils.speed_to_pace(speed)
        self.assertEqual(result, datetime.timedelta(minutes=5, seconds=43))


if __name__ == '__main__':
    unittest.main()
