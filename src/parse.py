from src import ActivityType, Attribute
from src.authorize import authorize
from src.get_data import download
from src.load_activities import load
from src.printer import pprint, weekly_table
from src.utils import pace_from_string, strip_accents, \
    format_value, timedelta_from_string, add_pace_attribute

import datetime
import re
from argparse import ArgumentParser, RawTextHelpFormatter


def validate_attr_filter(filtr, attribute):
    """Make sure that attribute based filter specified by user is in correct format.
    (symbol:value) where symbol is from [>, <, ==, <=, >=] and value is float or pace[mm:ss]."""
    try:
        symbol, value = filtr.split(' ')
    except ValueError:
        raise ValueError(f"Incorrect attribute filter specified: {filtr}, "
                         f"maybe a missing space between symbol and value")
    if symbol not in ['>', '<', '==', '>=', '<=']:
        raise ValueError(f'Incorrect equality symbol: {symbol}.')
    try:
        if attribute == "start_date_local":
            value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        elif attribute == "average_pace":
            value = pace_from_string(value)
        elif attribute == "moving_time":
            value = timedelta_from_string(value)
        else:
            value = float(value)
    except ValueError:
        raise ValueError(f'Specified value: {value} is not correct.')
    return {'symbol': symbol, 'value': value}


def generate_condition(value, filtr):
    """"""
    if filtr['symbol'] == '>':
        return value > filtr['value']
    elif filtr['symbol'] == '>=':
        return value >= filtr['value']
    elif filtr['symbol'] == '==':
        return value == filtr['value']
    elif filtr['symbol'] == '<=':
        return value <= filtr['value']
    elif filtr['symbol'] == '<':
        return value < filtr['value']


def apply_attr_filters(data, attribute, filtr):
    """Filter activities by specified attribute filters.
    E.g.: attribute 'distance', filter: '> 10'."""
    filtered_data = []
    for activity in data:
        if attribute not in Attribute.list():
            raise KeyError("Incorrect attribute specified.")
        try:
            value = format_value(attribute, activity[attribute])
        except KeyError:
            continue
        if generate_condition(value, filtr):
            filtered_data.append(activity)
    return filtered_data


def filter_activity_types(data, types):
    """Filter list of activities by specific activity types, one or more."""
    data = [activity for activity in data if activity['type'].lower() in types]
    return data


def sort_by_attr(data, sort_arg):
    """Sort activities by specified attribute and order in format 'attribute:[asc/desc]'."""
    if ':' not in sort_arg:
        raise ValueError("Sorting argument should be in format 'attribute:[asc/desc]'")
    attribute, order = sort_arg.split(':')
    if order not in ['asc', 'desc']:
        raise ValueError("Sorting order should be either asc:desc")
    try:
        attribute = Attribute[attribute].value
    except KeyError as e:
        raise KeyError(f"Incorrect attribute specified in sortby: {attribute}") from e
    reverse_order = (order.lower() == 'desc')
    # remove data with missing attribute
    data = [activity for activity in data if activity.get(attribute)]
    data = sorted(data, key=lambda x: x[attribute], reverse=reverse_order)
    return data


def match_name(data, pattern):
    """Filter list of activities by matching a part or the whole name of activity."""
    filtered_data = []
    for activity in data:
        stripped_name = strip_accents(activity['name'])
        if re.search(pattern, stripped_name, flags=re.IGNORECASE):
            filtered_data.append(activity)
    return filtered_data


def parse_cli_args():
    argparser = ArgumentParser(description=f"""Filter strava activities by your parameters.
All attribute filters are specified as \"symbol value\" \
string where symbol is one of [>, <, ==, >=, <=]
Available attributes to filter by: {list(Attribute.__members__)}
Available activity types: {[act.value for act in ActivityType]}""",
                               formatter_class=RawTextHelpFormatter)
    subparser = argparser.add_subparsers(title="Subcommands", dest="subcommand",
                                         help="Available subcommands")
    subparser.add_parser("authorize", help="Authorize app to access data")
    subparser.add_parser("download", help="Download activity data")
    basic_group = argparser.add_argument_group('Basic filters')
    basic_group.add_argument('--name', type=str,
                             help='filter by keywords present in activity name')
    basic_group.add_argument('--type', type=str.lower,
                             choices=[t.value.lower() for t in ActivityType],
                             help='filter by specific activity type', nargs='*', action='extend')
    basic_group.add_argument('-l', '--limit', type=int,
                             help='limit output to number of results')
    basic_group.add_argument('--sortby', type=str,
                             help="Sort by specific attribute and order: "
                                  "'attribute_name:[desc/asc]'")
    basic_group.add_argument('--weekly', type=int,
                             help="Print weekly statistics")
    attr_group = argparser.add_argument_group('Attribute filters')
    attr_group.add_argument('-dis', '--distance', type=str, nargs='*', action='extend',
                            help='set the distance filters[km], e.g.: \'> 90\'')
    attr_group.add_argument('-dat', '--date', type=str, nargs='*', action='extend',
                            help='set the date filters[YYYY-MM-DD], e.g.: \'> 2023-12-06\'')
    attr_group.add_argument('-eg', '--elevation_gain', type=str, nargs='*', action='extend',
                            help='set the elevation gain filter[m], e.g.: \'> 1000\'')
    attr_group.add_argument('-hr', '--average_heartrate', type=str, nargs='*', action='extend',
                            help='set the average heartrate filter[bpm], e.g.: \'== 160\'')
    attr_group.add_argument('-sp', '--average_speed', type=str, nargs='*', action='extend',
                            help='set the average speed filter[km/h], e.g.: \'>= 25\'')
    attr_group.add_argument('-t', '--moving_time', type=str, nargs='*', action='extend',
                            help='set the moving time filter[s], e.g.: \'< 3600\'')
    attr_group.add_argument('-pc', '--average_pace', type=str, nargs='*', action='extend',
                            help='set the average pace filter[mm:ss/km], e.g.: \'< 05:30\'')

    return argparser.parse_args()


def main():
    args = parse_cli_args()
    if args.subcommand == 'authorize':
        authorize()
        return
    elif args.subcommand == 'download':
        download()
        return

    data = load()
    data = add_pace_attribute(data)

    if args.name:
        data = match_name(data, args.name)

    if args.type:
        data = filter_activity_types(data, args.type)

    for attribute, filters in vars(args).items():
        # skip if filter not specified or not attribute filter [dist, elev, hr, ..]
        if filters is None or attribute not in Attribute.__members__:
            continue
        attribute = Attribute[attribute].value
        filters = [validate_attr_filter(filtr, attribute) for filtr in filters]
        for filtr in filters:
            data = apply_attr_filters(data, attribute, filtr)

    if args.sortby:
        data = sort_by_attr(data, args.sortby)

    if args.limit:
        data = data[0:args.limit]

    if args.weekly:
        weekly_table(data, args.weekly)
    else:
        pprint(data)


if __name__ == '__main__':
    main()
