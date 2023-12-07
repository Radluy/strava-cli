import datetime
import json
import unittest
import sys
sys.path.append('src')

from src import parse  # noqa: E402


def load_example_data():
    with open('tests/example_data.json') as f:
        data = json.load(f)
    return data


class TestValidateAttrFilters(unittest.TestCase):
    def test_random_string(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, 'abc', '_')

    def test_without_space(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, '>10', '_')

    def test_incorrect_symbol(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, '^ 10', '_')

    def test_non_numeric_val(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, '> abc', '_')

    def test_incorrect_pace_val(self):
        self.assertRaises(ValueError, parse.validate_attr_filter, '> 5:a', '_')

    def test_int_attr(self):
        expected = {'symbol': '>', 'value': 10.0}
        result = parse.validate_attr_filter('> 10', 'distance')
        self.assertEqual(expected, result)

    def test_float_attr(self):
        expected = {'symbol': '==', 'value': 15.5}
        result = parse.validate_attr_filter('== 15.5', 'distance')
        self.assertEqual(expected, result)

    def test_correct_pace(self):
        expected = {'symbol': '<=', 'value': datetime.timedelta(minutes=5, seconds=20)}
        result = parse.validate_attr_filter('<= 5:20', 'average_pace')
        self.assertEqual(expected, result)


class TestFilterActivityTypes(unittest.TestCase):
    def test_incorrect_act_type(self):
        data = load_example_data()
        filtered_data = parse.filter_activity_types(data, 'SpaceFlying')
        self.assertEqual(filtered_data, [])

    def test_type_run(self):
        data = load_example_data()
        filtered_data = parse.filter_activity_types(data, 'run')
        self.assertEqual(filtered_data[0]['name'], 'Bondcliff')

    def test_empty_data(self):
        result = parse.filter_activity_types([], 'run')
        self.assertEqual(result, [])

    def test_multiple_filters(self):
        data = load_example_data()
        filtered_data = parse.filter_activity_types(data, ['run', 'ride'])
        activity_names = [act['name'] for act in filtered_data]
        self.assertEqual(set(activity_names), {'Bondcliff', 'Happy Friday'})


class TestMatchName(unittest.TestCase):
    def test_incorrect_name(self):
        data = load_example_data()
        filtered_data = parse.match_name(data, 'random_name')
        self.assertEqual(filtered_data, [])

    def test_match_exact_name(self):
        data = load_example_data()
        filtered_data = parse.match_name(data, 'Bondcliff')
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]['name'], 'Bondcliff')

    def test_match_lowercase_name(self):
        data = load_example_data()
        filtered_data = parse.match_name(data, 'bondcliff')
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]['name'], 'Bondcliff')

    def test_match_partial_name(self):
        data = load_example_data()
        filtered_data = parse.match_name(data, 'happy')
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]['name'], 'Happy Friday')

    def test_empty_data(self):
        result = parse.match_name([], 'Bondcliff')
        self.assertEqual(len(result), 0)


class TestApplyAttrFilters(unittest.TestCase):
    def test_incorrect_attr(self):
        data = load_example_data()
        attr = 'incorrect_attr'
        filter = {'symbol': '>', 'value': '10'}
        self.assertRaises(KeyError, parse.apply_attr_filters, data, attr, filter)

    def test_empty_data(self):
        attr = 'distance'
        filter = {'symbol': '>', 'value': '10'}
        result = parse.apply_attr_filters([], attr, filter)
        self.assertEqual(len(result), 0)

    def test_filter_distance_attr(self):
        data = load_example_data()
        attr = 'distance'
        filter = {'symbol': '>', 'value': '24'}
        filtered_data = parse.apply_attr_filters(data, attr, filter)
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]['name'], 'Happy Friday')

    def test_filter_pace(self):
        data = load_example_data()
        attr = 'average_pace'
        value = datetime.timedelta(minutes=3, seconds=30)
        filter = {'symbol': '<', 'value': value}
        filtered_data = parse.apply_attr_filters(data, attr, filter)
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]['name'], 'Happy Friday')

    def test_filter_hour_pace(self):
        data = load_example_data()
        attr = 'average_pace'
        value = datetime.timedelta(hours=1, minutes=3, seconds=30)
        filter = {'symbol': '<', 'value': value}
        filtered_data = parse.apply_attr_filters(data, attr, filter)
        self.assertEqual(len(filtered_data), 2)


class TestSortByAttr(unittest.TestCase):
    def test_empty_data(self):
        sort_arg = 'distance:desc'
        result = parse.sort_by_attr([], sort_arg)
        self.assertEqual(result, [])

    def test_incorrect_sort_arg(self):
        data = load_example_data()
        sort_arg = 'randomstring'
        self.assertRaises(ValueError, parse.sort_by_attr, data, sort_arg)

    def test_incorrect_order(self):
        data = load_example_data()
        sort_arg = 'distance:badorder'
        self.assertRaises(ValueError, parse.sort_by_attr, data, sort_arg)

    def test_incorrect_attr_name(self):
        data = load_example_data()
        sort_arg = 'badattr:asc'
        self.assertRaises(KeyError, parse.sort_by_attr, data, sort_arg)

    def test_sort_distance_asc(self):
        data = load_example_data()
        sort_arg = 'distance:asc'
        sorted_data = parse.sort_by_attr(data, sort_arg)
        self.assertGreaterEqual(sorted_data[1]['distance'], sorted_data[0]['distance'])

    def test_sort_distance_desc(self):
        data = load_example_data()
        sort_arg = 'distance:desc'
        sorted_data = parse.sort_by_attr(data, sort_arg)
        self.assertGreaterEqual(sorted_data[0]['distance'], sorted_data[1]['distance'])

    def test_sort_moving_time_desc(self):
        data = load_example_data()
        sort_arg = 'moving_time:desc'
        sorted_data = parse.sort_by_attr(data, sort_arg)
        self.assertGreaterEqual(sorted_data[0]['moving_time'], sorted_data[1]['moving_time'])

    def test_sort_average_speed_desc(self):
        data = load_example_data()
        sort_arg = 'average_speed:desc'
        sorted_data = parse.sort_by_attr(data, sort_arg)
        self.assertGreaterEqual(sorted_data[0]['average_speed'], sorted_data[1]['average_speed'])

    def test_sort_pace_desc(self):
        data = load_example_data()
        data = parse.apply_attr_filters(data, 'average_pace',
                                        {'symbol': '<', 'value': datetime.timedelta(minutes=10)})
        sort_arg = 'average_pace:desc'
        sorted_data = parse.sort_by_attr(data, sort_arg)
        self.assertGreaterEqual(sorted_data[0]['average_pace'], sorted_data[1]['average_pace'])


if __name__ == '__main__':
    unittest.main()
