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
        self.assertRaises(TypeError, utils.speed_to_pace, speed)

    def test_correct_speed(self):
        speed = 2.91
        result = utils.speed_to_pace(speed)
        self.assertEqual(result, datetime.timedelta(minutes=5, seconds=43))


class TestPaceFromString(unittest.TestCase):
    def test_pace_as_int(self):
        pace = 5.3
        self.assertRaises(TypeError, utils.pace_from_string, pace)

    def test_pace_as_timedelta(self):
        pace = datetime.timedelta(minutes=5, seconds=20)
        self.assertRaises(TypeError, utils.pace_from_string, pace)

    def test_correct_pace(self):
        pace = '05:30'
        expected_result = datetime.timedelta(minutes=5, seconds=30)
        result = utils.pace_from_string(pace)
        self.assertEqual(result, expected_result)

    def test_pace_without_leading_zero(self):
        pace = '5:30'
        expected_result = datetime.timedelta(minutes=5, seconds=30)
        result = utils.pace_from_string(pace)
        self.assertEqual(result, expected_result)

    def test_pace_with_hours(self):
        pace = '01:05:30'
        self.assertRaises(ValueError, utils.pace_from_string, pace)


class TestFormatValue(unittest.TestCase):
    def test_unlisted_attr(self):
        attr = 'unlisted_attr'
        value = 42
        result = utils.format_value(attr, value)
        self.assertEqual(result, value)

    def test_format_distance(self):
        result = utils.format_value('distance', 69000)
        self.assertEqual(result, 69)

    def test_format_distance_not_int(self):
        attr = 'distance'
        value = 'abc'
        self.assertRaises(TypeError, utils.format_value, attr, value)

    def test_format_speed(self):
        result = utils.format_value('average_speed', 7)
        self.assertEqual(result, 25.2)

    def test_format_pace(self):
        result = utils.format_value('average_pace', 7)
        self.assertEqual(result.seconds, 142)


if __name__ == '__main__':
    unittest.main()
