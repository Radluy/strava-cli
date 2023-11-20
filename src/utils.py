import datetime
import unicodedata


def format_time(date):
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
    if attr == 'distance':
        return value / 1000
    elif attr == 'average_speed':
        return value * 3.6
    elif attr == 'average_pace':
        return speed_to_pace(value)


def pace_from_string(filter_val):
    dt = datetime.datetime.strptime(filter_val, "%M:%S")
    delta = datetime.timedelta(minutes=dt.minute, seconds=dt.second)
    return delta
