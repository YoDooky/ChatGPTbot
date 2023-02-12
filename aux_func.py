from datetime import datetime, timedelta


def compare_dates(first_date: str, second_date: str) -> bool:
    """Compares dates. If first arg > second arg returns true"""
    first_date = datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S')
    second_date = datetime.strptime(second_date, '%Y-%m-%d %H:%M:%S')
    if first_date >= second_date:
        return True
    else:
        return False
