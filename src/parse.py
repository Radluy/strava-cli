import load_activities

import datetime
import re
import unicodedata
from argparse import ArgumentParser, RawTextHelpFormatter
from enum import Enum

from rich.console import Console

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

    def __str__(self):
        return self.value


def strip_accents(string):
   """Remove local nonunicode chars(č -> c) for better name matching."""
   return ''.join(c for c in unicodedata.normalize('NFD', string)
                  if unicodedata.category(c) != 'Mn')


def pretty_print(data):
    print(f"Total acitivities: {len(data)}")
    for activity in data:
        console.print(f"[bold][red]{activity['name']} [{activity['type']}] \
[blue]https://strava.com/activities/{activity['id']}")
        attributes = f"  -  [bold]distance[/bold]: "
        attributes += f"[green]{round(float(activity['distance'])/1000, 2)}km[/green], "
        attributes += f"[bold]elevation gain[/bold]: "
        attributes += f"[green]{activity['total_elevation_gain']}m[/green], "
        attributes += f"[bold]average heartrate[/bold]: "
        try:
            attributes += f"[green]{activity['average_heartrate']}bpm[/green] "
        except:
            attributes += "None"
        attributes += f"\n  -  [bold]moving time[/bold]: "
        attributes += f"[green]{datetime.timedelta(seconds=activity['moving_time'])}[/green], "
        attributes += f"[bold]average speed[/bold]: "
        attributes += f"[green]{round(activity['average_speed']*3.6, 2)}km/h[/green], "
        console.print(attributes, highlight=False)
    
    
def validate_attr_filters(filters):
    parsed_filters = []
    for filter in filters:
        symbol, value = filter.split(' ')
        if symbol not in ['>', '<', '==', '>=', '<=']:
            raise Exception(f'Incorrect equality symbol: {symbol}.')
        try:
            value = float(value)
        except ValueError:
            raise Exception(f'Specified value: {value} is not correct distance.')
        parsed_filters.append({'symbol': symbol, 'value': value})
    return parsed_filters


def apply_attr_filters(data, attribute, filter):
    filtered_data = []
    for activity in data:
        try:
            if eval(f'{activity[attribute]} {filter['symbol']} {filter['value']}'):
                filtered_data.append(activity)
        except KeyError:
            continue
    return filtered_data


def filter_activity_types(data, types):
    type_filters = [f.value for f in types]
    data = [activity for activity in data if activity['type'] in type_filters]
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


if __name__ == '__main__':
    argparser = ArgumentParser(description=f"""Filter strava activities by your parameters.
All attribute filters are specified as \"symbol value\" string where symbol is one of [>, <, ==, >=, <=]
Available attributes to filter by: {list(Attribute.__members__)}
Available activity types: {list(ActivityType.__members__)}""",
                               formatter_class=RawTextHelpFormatter)
    argparser.add_argument('--name', type=str, 
                           help='filter by keywords present in activity name')
    argparser.add_argument('--type', type=ActivityType, choices=list(ActivityType), 
                           help='filter by specific activity type', nargs='*', action='extend')
    argparser.add_argument('--sortby', type=str, 
                           help="Sort by specific attribute and order: 'attribute_name:[desc/asc]'")
    argparser.add_argument('-l', '--limit', type=int, 
                           help='limit output to number of results')
    attr_group = argparser.add_argument_group('Attribute filters')
    attr_group.add_argument('-d', '--distance', type=str, nargs='*', action='extend',
                           help='set the distance filters[m]')
    attr_group.add_argument('-eg', '--elevation_gain', type=str, nargs='*', action='extend',
                           help='set the elevation gain filter[m]')
    attr_group.add_argument('-hr', '--avg_heartrate', type=str, nargs='*', action='extend',
                           help='set the average heartrate filter[bpm]')
    attr_group.add_argument('-sp', '--average_speed', type=str, nargs='*', action='extend',
                           help='set the average speed filter[m/s]')
    attr_group.add_argument('-t', '--moving_time', type=str, nargs='*', action='extend',
                           help='set the moving time filter[s]')
    #TODO: add pace

    args = argparser.parse_args()

    data = load_activities.load()

    if args.name:
        data = match_name(data, args.name)

    if args.type:
        data = filter_activity_types(data, args.type)

    for attribute, filters in vars(args).items():
        # skip if filter not specified or not attribute filter [dist, elev, hr]
        if filters is None or attribute not in Attribute.__members__:
            continue
        attribute = Attribute[attribute].value
        filters = validate_attr_filters(filters)
        for filter in filters:
            data = apply_attr_filters(data, attribute, filter)
    
    if args.sortby:
        data = sort_by_attr(data, args.sortby)
        
    if args.limit:
        data = data[0:args.limit]
    
    pretty_print(data)
