from src.utils import parse_datetime, format_value
from src.stats import weekly_stats, generate_weekly_ranges
from src import Attribute, Units

from rich.console import Console
from rich.table import Table

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


def weekly_table(data, num_weeks=4):
    ranges = generate_weekly_ranges(num_weeks)
    stats = weekly_stats(data, num_weeks)

    table = Table(show_header=True, header_style=f"bold {SECOND_COLOR}",
                  show_lines=True, row_styles=["dim", ""])
    table.add_column("Week")
    table.add_column("Moving time")
    table.add_column("Distance")
    table.add_column("Elevation")
    for week, stat in zip(ranges, stats):
        table.add_row(f"{week['start'].strftime('%d %b %Y')} - {week['end'].strftime('%d %b %Y')}",
                      f"{stat['moving_time']} h",
                      f"{stat['covered_distance']} km",
                      f"{stat['covered_elevation']} m")

    console.print(table)


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


def print_gears(bikes, shoes):
    table = Table(show_header=True, header_style=f"bold {SECOND_COLOR}",
                  show_lines=True, row_styles=["dim", ""])
    table.add_column("Bike")
    table.add_column("Covered distance")
    for bike in bikes:
        table.add_row(bike['name'], f"{bike['converted_distance']} km")
    console.print(table)

    table = Table(show_header=True, header_style=f"bold {SECOND_COLOR}",
                  show_lines=True, row_styles=["dim", ""])
    table.add_column("Shoes")
    table.add_column("Covered distance")
    for shoe in shoes:
        table.add_row(shoe['name'], f"{shoe['converted_distance']} km")
    console.print(table)
