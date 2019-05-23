from __future__ import absolute_import
import copy

from . import util
from .constant import DateTimeGranularity


class Request(object):
    data = {}

    def __init__(self, **kwargs):
        self.data.update(kwargs)


class AuthRequest(Request):
    def __init__(self, credentials, **kwargs):
        Request.__init__(self, **kwargs)
        if credentials:
            self.data.update(credentials.to_dict())


class GetReportColumnsRequest(AuthRequest):
    def __init__(self, credentials=None, report=None):
        AuthRequest.__init__(self, credentials, report=report)


class CreateReportRequest(AuthRequest):
    reportCategory = None

    def __init__(self, credentials=None, reportCategory=None, **kwargs):
        if not reportCategory:
            raise ValueError("Missing report category parameter (summary or detail)")

        self.reportCategory = reportCategory

        time_start = kwargs.get('time_start')
        time_end = kwargs.get('time_end')
        time_zone = kwargs.get('time_zone')
        if not time_start and not time_end:
            raise ValueError("Missing time_start and/or time_end parameters")

        time_start = util.get_timestamp(time_start, time_zone)
        time_end = util.get_timestamp(time_end, time_zone)

        if time_end < time_start:
            time_start, time_end = time_end, time_start

        if not kwargs.get('traffic'):
            raise ValueError("Missing traffic parameters")

        data = copy.deepcopy(kwargs)
        data.update({
            'time_start': str(time_start),
            'time_end': str(time_end),
            'time_series': kwargs.get('time_series', DateTimeGranularity.HOURLY),
            'delivery_method': [
                "S3link",
            ],
            "delivery_format": "json",
        })

        AuthRequest.__init__(self, credentials, **data)


class GetReportProgressRequest(AuthRequest):
    def __init__(self, credentials=None, token=None):
        AuthRequest.__init__(self, credentials, token=token)
