import datetime
import unittest
import sys
sys.path.append('src')

from src import parse  # noqa: E402


class TestValidateAttrFilters(unittest.TestCase):
    def test_random_string(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, 'abc')

    def test_without_space(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, '>10')

    def test_incorrect_symbol(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, '^ 10')

    def test_non_numeric_val(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, '> abc')

    def test_incorrect_pace_val(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, '> 5:a')

    def test_int_attr(self):
        expected = {'symbol': '>', 'value': 10.0}
        result = parse.validate_attr_filter('> 10')
        self.assertEqual(expected, result)

    def test_float_attr(self):
        expected = {'symbol': '==', 'value': 15.5}
        result = parse.validate_attr_filter('== 15.5')
        self.assertEqual(expected, result)

    def test_correct_pace(self):
        expected = {'symbol': '<=', 'value': datetime.timedelta(minutes=5, seconds=20)}
        result = parse.validate_attr_filter('<= 5:20')
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
