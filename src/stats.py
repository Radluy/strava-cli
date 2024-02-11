import datetime

from src.utils import format_value


def calculate_stats(data):
    """TODO"""
    stats = {}
    stats["covered_distance"] = round(
        sum([format_value("distance", activity["distance"]) for activity in data]), 2
    )
    stats["moving_time"] = sum(
        [format_value("moving_time", activity["moving_time"]) for activity in data],
        datetime.timedelta(),
    )
    stats["covered_elevation"] = round(
        sum([activity["total_elevation_gain"] for activity in data]), 2
    )

    return stats


def generate_weekly_ranges(num_weeks=4):
    ranges = []
    day = datetime.datetime.today().date()
    for _ in range(num_weeks):
        start = day - datetime.timedelta(days=day.weekday())
        end = start + datetime.timedelta(days=6)
        ranges.append({"start": start, "end": end})
        day = day - datetime.timedelta(days=7)

    return ranges


def data_by_weeks(data, num_weeks):
    ranges = generate_weekly_ranges(num_weeks)
    weekly_collections = [[] for _ in range(len(ranges))]
    for activity in data:
        date = format_value("start_date_local", activity["start_date_local"])
        for idx, week in enumerate(ranges):
            if date >= week["start"] and date <= week["end"]:
                weekly_collections[idx].append(activity)

    return weekly_collections


def weekly_stats(data, num_weeks=4):
    weekly_data = data_by_weeks(data, num_weeks)
    return [calculate_stats(week) for week in weekly_data]
