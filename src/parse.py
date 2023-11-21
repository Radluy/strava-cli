import datetime
import re
from argparse import ArgumentParser, RawTextHelpFormatter
from enum import Enum

from rich.console import Console

from load_activities import load
from utils import pace_from_string, parse_datetime, \
                             speed_to_pace, strip_accents, format_value


console = Console()


class ActivityType(Enum):
    run = 'Run'
    ride = 'Ride'
    hike = 'Hike'
    workout = 'Workout'
    rock_climbing = 'RockClimbing'
    nordic_ski = 'NordicSki'
    alpine_ski = 'AlpineSki'

    def __str__(self):
        return self.value


class Attribute(Enum):
    distance = 'distance'
    elevation_gain = 'total_elevation_gain'
    avg_heartrate = 'average_heartrate'
    moving_time = 'moving_time'
    average_speed = 'average_speed'
    average_pace = 'average_pace'

    def __str__(self):
        return self.value


def pretty_print(data):
    print(f"Total acitivities: {len(data)}")
    for activity in data:
        console.print(f"[bold][red]{activity['name']} [{activity['type']}] \
[blue]https://strava.com/activities/{activity['id']}")
        attributes = "  -  [bold]date[/bold]: "
        attributes += f"[green]{parse_datetime(activity['start_date_local'])}[/green], "
        attributes += "[bold]distance[/bold]: "
        attributes += f"[green]{round(float(activity['distance']) / 1000, 2)}km[/green], "
        attributes += "[bold]moving time[/bold]: "
        attributes += f"[green]{datetime.timedelta(seconds=activity['moving_time'])}[/green], "
        attributes += "\n  -  [bold]elevation gain[/bold]: "
        attributes += f"[green]{activity['total_elevation_gain']}m[/green], "
        attributes += "[bold]avg heartrate[/bold]: "
        try:
            attributes += f"[green]{activity['average_heartrate']}bpm[/green], "
        except KeyError:
            attributes += "None, "
        attributes += "[bold]avg speed[/bold]: "
        attributes += f"[green]{round(activity['average_speed']*3.6, 2)}km/h[/green], "
        attributes += "\n  -  [bold]avg pace[/bold]: "
        attributes += f"[green]{speed_to_pace(activity['average_speed'])}min/km[/green]"
        console.print(attributes, highlight=False)


def validate_attr_filter(filtr):
    """Make sure that attribute based filter specified by user is in correct format.
    (symbol:value) where symbol is from [>, <, ==, <=, >=] and value is float or pace[mm:ss]"""
    try:
        symbol, value = filtr.split(' ')
    except ValueError:
        raise ValueError(f"Incorrect attribute filter specified: {filtr}, "
                         f"maybe a missing space between symbol and value")
    if symbol not in ['>', '<', '==', '>=', '<=']:
        raise ValueError(f'Incorrect equality symbol: {symbol}.')
    try:
        if ':' in value:
            value = pace_from_string(value)
        else:
            value = float(value)
    except ValueError:
        raise ValueError(f'Specified value: {value} is not correct.')
    return {'symbol': symbol, 'value': value}


def apply_attr_filters(data, attribute, filter):
    filtered_data = []
    for activity in data:
        activity['average_pace'] = activity['average_speed']
        value = format_value(attribute, activity[attribute])
        if attribute == 'average_pace':
            condition = f"\"{value}\" {filter['symbol']} \"{filter['value']}\""
        else:
            condition = f"{value} {filter['symbol']} {filter['value']}"
        try:
            if eval(condition):
                filtered_data.append(activity)
        except KeyError:
            continue
    return filtered_data


def filter_activity_types(data, types):
    data = [activity for activity in data if activity['type'].lower() in types]
    return data


def sort_by_attr(data, sort_arg):
    attribute, order = sort_arg.split(':')
    try:
        attribute = Attribute[attribute].value
    except KeyError:
        raise Exception(f"Incorrect attribute specified in sortby: {attribute}")
    reverse_order = (order.lower() == 'desc')
    data = sorted(data, key=lambda x: x[attribute], reverse=reverse_order)
    return data


def match_name(data, pattern):
    filtered_data = []
    for activity in data:
        stripped_name = strip_accents(activity['name'])
        if re.match(pattern, stripped_name, flags=re.IGNORECASE):
            filtered_data.append(activity)
    return filtered_data


def parse_cli_args():
    argparser = ArgumentParser(description=f"""Filter strava activities by your parameters.
All attribute filters are specified as \"symbol value\" \
string where symbol is one of [>, <, ==, >=, <=]
Available attributes to filter by: {list(Attribute.__members__)}
Available activity types: {[act.value for act in ActivityType]}""",
                               formatter_class=RawTextHelpFormatter)
    argparser.add_argument('--name', type=str,
                           help='filter by keywords present in activity name')
    argparser.add_argument('--type', type=str.lower,
                           choices=[t.value.lower() for t in ActivityType],
                           help='filter by specific activity type', nargs='*', action='extend')
    argparser.add_argument('--sortby', type=str,
                           help="Sort by specific attribute and order: 'attribute_name:[desc/asc]'")
    argparser.add_argument('-l', '--limit', type=int,
                           help='limit output to number of results')
    attr_group = argparser.add_argument_group('Attribute filters')
    attr_group.add_argument('-d', '--distance', type=str, nargs='*', action='extend',
                            help='set the distance filters[km], e.g.: \'> 90\'')
    attr_group.add_argument('-eg', '--elevation_gain', type=str, nargs='*', action='extend',
                            help='set the elevation gain filter[m], e.g.: \'> 1000\'')
    attr_group.add_argument('-hr', '--avg_heartrate', type=str, nargs='*', action='extend',
                            help='set the average heartrate filter[bpm], e.g.: \'== 160\'')
    attr_group.add_argument('-sp', '--average_speed', type=str, nargs='*', action='extend',
                            help='set the average speed filter[km/h], e.g.: \'>= 25\'')
    attr_group.add_argument('-t', '--moving_time', type=str, nargs='*', action='extend',
                            help='set the moving time filter[s], e.g.: \'< 3600\'')
    attr_group.add_argument('-pc', '--average_pace', type=str, nargs='*', action='extend',
                            help='set the average pace filter[mm:ss/km], e.g.: \'< 05:30\'')

    return argparser.parse_args()


if __name__ == '__main__':
    args = parse_cli_args()
    data = load()

    if args.name:
        data = match_name(data, args.name)

    if args.type:
        data = filter_activity_types(data, args.type)

    for attribute, filters in vars(args).items():
        # skip if filter not specified or not attribute filter [dist, elev, hr, ..]
        if filters is None or attribute not in Attribute.__members__:
            continue
        attribute = Attribute[attribute].value
        filters = [validate_attr_filter(filtr) for filtr in filters]
        for filtr in filters:
            data = apply_attr_filters(data, attribute, filtr)

    if args.sortby:
        data = sort_by_attr(data, args.sortby)

    if args.limit:
        data = data[0:args.limit]

    pretty_print(data)
