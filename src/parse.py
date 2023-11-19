import load_activities
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

    def __str__(self):
        return self.value


def pretty_print(data):
    print(f"Total acitivities: {len(data)}")
    for activity in data:
        console.print(f"[bold][red]{activity['name']}: \
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
        console.print(attributes, highlight=False)
    
    
def validate_attr_filters(filters):
    filters = filters.split(' ')
    if len(filters) % 2 != 0:
        raise Exception("Filters are expected to come in pairs of symbols and values.")
    
    parsed_filters = []
    for symbol, value in list(zip(filters[::2], filters[1::2])):
        if symbol not in ['>', '<', '=', '>=', '<=']:
            raise Exception(f'Incorrect equality symbol: {symbol}.')
        try:
            value = float(value)
        except ValueError:
            raise Exception(f'Specified value: {value} is not correct distance.')
        parsed_filters.append({'symbol': symbol, 'value': value})
    return parsed_filters


def apply_attr_filters(data, attribute, filters):
    filtered_data = []
    for filter in filters:
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


if __name__ == '__main__':
    argparser = ArgumentParser(description=f"""Filter strava activities by your parameters.
Available attributes to filter by: {list(Attribute.__members__)}""",
                               formatter_class=RawTextHelpFormatter)
    argparser.add_argument('--type', type=ActivityType, choices=list(ActivityType), 
                           help='filter by specific activity type', nargs='*', action='extend')
    argparser.add_argument('-d', '--distance', type=str, help='set the distance filters[m]')
    argparser.add_argument('-eg', '--elevation_gain', type=str, 
                           help='set the elevation gain filter[m]')
    argparser.add_argument('-hr', '--avg_heartrate', type=str, 
                           help='set the average heartrate filter[bpm]')
    argparser.add_argument('--sortby', type=str, 
                           help="Sort by specific attribute and order: 'attribute_name:[desc/asc]'")

    args = argparser.parse_args()

    data = load_activities.load()

    if args.type:
        data = filter_activity_types(data, args.type)

    for attribute, filters in vars(args).items():
        # skip if filter not specified or not attribute filter [dist, elev, hr]
        if filters is None or attribute not in Attribute.__members__:
            continue
        attribute = Attribute[attribute].value
        filters = validate_attr_filters(filters)
        data = apply_attr_filters(data, attribute, filters)
    
    if args.sortby:
        data = sort_by_attr(data, args.sortby)
        
    
    pretty_print(data)
