import datetime
import re
import unicodedata


def parse_datetime(date):
    """Load datetime by format used in the API."""
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')


def strip_accents(string):
    """Remove local nonunicode chars(č -> c) for better name matching."""
    return ''.join(c for c in unicodedata.normalize('NFD', string)
                   if unicodedata.category(c) != 'Mn')


def speed_to_pace(speed):
    """Calculate running pace from speed [m/s -> min/km]."""
    if speed == 0:
        return speed
    pace = 60 / (speed * 3.6)
    pace_timedelta = datetime.timedelta(minutes=pace)
    return pace_timedelta - datetime.timedelta(microseconds=pace_timedelta.microseconds)


def format_value(attr, value):
    """Predefined formatters for undesired values in strava data."""
    if attr == 'distance':
        return value / 1000
    elif attr == 'average_speed':
        return value * 3.6
    elif attr == 'average_pace':
        return speed_to_pace(value)
    elif attr == 'start_date_local':
        return parse_datetime(value).date()
    else:
        return value


def pace_from_string(filter_val):
    """Load pace as timedelta from string specified as cli argument by user."""
    if not re.match(r"[0-5]?\d:[0-5]\d", filter_val):
        raise ValueError(f"Incorrect pace specified: {filter_val}")
    dt = datetime.datetime.strptime(filter_val, "%M:%S")
    delta = datetime.timedelta(minutes=dt.minute, seconds=dt.second)
    return delta
