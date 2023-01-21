from datetime import datetime, timedelta


def time_from_utc_to_moscow_timezone(current_time: str) -> str:
    current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    moscow_time = str(current_time + timedelta(hours=3))
    return moscow_time


def valid_date(datestring):
    datestring = datestring.strip()
    try:
        datetime.strptime(datestring, '%Y-%m-%d')
        return datestring
    except ValueError:
        return False


def compare_dates(db_timestamp: str, filter_timestamp: str) -> bool:
    """Compares dates. If first arg > second arg returns true"""
    db_timestamp = datetime.strptime(db_timestamp, '%Y-%m-%d %H:%M:%S')
    filter_timestamp = datetime.strptime(filter_timestamp, '%Y-%m-%d %H:%M:%S')
    if db_timestamp >= filter_timestamp:
        return True
    else:
        return False
