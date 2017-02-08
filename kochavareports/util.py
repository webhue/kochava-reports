import datetime
import time


DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def parse_str_datetime(strdate):
    return datetime.datetime.strptime(strdate, DATETIME_FORMAT)


def get_timestamp(d, date_format=DATE_FORMAT):
    if isinstance(d, basestring):
        if d.isdigit():
            date = datetime.datetime.fromtimestamp(int(d, 10))
        else:
            date = datetime.datetime.strptime(d, date_format)
    elif isinstance(d, datetime.datetime):
        date = d
    elif isinstance(d, datetime.date):
        date = datetime.datetime(year=d.year, month=d.month, day=d.day)
    elif isinstance(d, int):
        date = datetime.datetime.fromtimestamp(d)
    else:
        raise ValueError('Invalid date argument: %r' % d)
    # date = datetime.datetime(*date.timetuple()[:4])
    t = time.mktime(date.timetuple())
    return int(t)
