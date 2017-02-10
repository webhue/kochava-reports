import datetime
import calendar


DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def parse_str_datetime(strdate):
    return datetime.datetime.strptime(strdate, DATETIME_FORMAT)


def get_timestamp(d, timezone=None):
    # tz = pytz.timezone(timezone) if timezone else None
    # timezone is not used atm
    if isinstance(d, basestring):
        if d.isdigit():
            return int(d, 10)
        else:
            date_format = DATETIME_FORMAT if(len(d) > 10) else DATE_FORMAT
            date = datetime.datetime.strptime(d, date_format)
    elif isinstance(d, datetime.datetime):
        date = d
    elif isinstance(d, datetime.date):
        date = datetime.datetime(year=d.year, month=d.month, day=d.day)
    elif isinstance(d, int):
        return d
    else:
        raise ValueError('Invalid date argument: %r' % d)
    date = datetime.datetime(*date.timetuple()[:4])
    t = calendar.timegm(date.timetuple())
    return int(t)
