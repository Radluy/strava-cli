from src.utils import parse_datetime, format_value
from src import Attribute, Units

from rich.console import Console


MAIN_COLOR = "#C45016"
SECOND_COLOR = "#C47C16"
THIRD_COLOR = "#F5F2C1"

console = Console()


def bold(text):
    return f"[bold]{text}[/bold]"


def third_color(text):
    return color(text, THIRD_COLOR)


def second_color(text):
    return color(text, SECOND_COLOR)


def main_color(text):
    return color(text, MAIN_COLOR)


def color(text, color):
    return f"[{color}]{text}[/{color}]"


def pprint(data):
    print(f"Total activities: {len(data)}")
    for activity in data:
        header = [
            bold(main_color(activity['name'])),
            bold(second_color(f"[{activity['type']}]")),
            parse_datetime(activity['start_date_local'])
        ]

        stats = []
        for attr in Attribute.__members__:
            if attr == "date":
                continue
            activity['average_pace'] = activity['average_speed']
            try:
                value = format_value(attr, activity[Attribute[attr].value])
            except KeyError:
                value = None
            unit = Units[attr]
            stats.append(f"  - {second_color(attr)}: {value} {unit}")  # noqa: E221

        url = third_color(f"https://strava.com/activities/{activity['id']}")  # noqa: E231

        console.print(*header, highlight=False)
        console.print(url)
        console.print(*stats, highlight=False, sep='\n')
        console.print('\n')
