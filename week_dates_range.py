from datetime import date, timedelta


def get_week_dates():
    date_range = []

    dt = date.today()
    # start = dt - timedelta(days=(dt.weekday())+1)
    start = dt - timedelta(days=4)
    end = dt + timedelta(days=3)
    # end = start + timedelta(days=6)
    while start < end:
        start += timedelta(days=1)
        str_start = str(start)
        day_name = get_day_name(str_start)
        date_range.append({day_name: str_start})

    return date_range


def get_day_name(str_start):
    year, month, day = str_start.split('-')
    day_name = (date(int(year), int(month), int(day)).strftime("%a"))
    return day_name


get_week_dates()
