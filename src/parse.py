import load_activities
from argparse import ArgumentParser

from rich import print as rprint
from rich.console import Console


console = Console()


def pretty_print(data):
    print(f"Total acitivities: {len(data)}")
    for activity in data:
        console.print(f"[bold][red]{activity['name']}: [blue]https://strava.com/activities/{activity['id']}")
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
    
    
def validate_filters(filters):
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


def apply_filters(data, attribute, filters):
    filtered_data = []
    for filter in filters:
        for activity in data:
            try:
                if eval(f'{activity[attribute]} {filter['symbol']} {filter['value']}'):
                    filtered_data.append(activity)
            except KeyError:
                continue
    return filtered_data


if __name__ == '__main__':
    argparser = ArgumentParser(description="Filter strava activities by your parameters.")
    argparser.add_argument('-d', '--distance', type=str, help='set the distance filters[m]')
    argparser.add_argument('-eg', '--total_elevation_gain', type=str, help='set the elevation gain filter[m]')
    argparser.add_argument('-hr', '--average_heartrate', type=str, help='set the average heartrate filter[bpm]')

    args = argparser.parse_args()

    data = load_activities.load()
    for attribute, filters in vars(args).items():
        if filters is None:
            continue
        filters = validate_filters(filters)
        data = apply_filters(data, attribute, filters)
    
    pretty_print(data)
