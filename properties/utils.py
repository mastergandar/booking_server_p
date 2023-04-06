from datetime import timedelta


def list_of_days_from_data_range(start_date, end_date, days: list):
    """Return a list of days between two dates."""
    days.append(start_date)
    days.append(end_date)
    for n in range(int((end_date - start_date).days)):
        days.append(start_date + timedelta(n))
    return days
