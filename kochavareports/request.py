import copy

from . import util


class Request(object):
    data = {}

    def __init__(self, **kwargs):
        self.data.update(kwargs)


class AuthRequest(Request):
    def __init__(self, credentials, **kwargs):
        Request.__init__(self, **kwargs)
        if credentials:
            self.data.update(credentials.__dict__)


class GetReportColumnsRequest(AuthRequest):
    def __init__(self, credentials=None, report=None):
        AuthRequest.__init__(self, credentials, report=report)


class CreateReportRequest(AuthRequest):
    def __init__(self, credentials=None, reportCategory=None, **kwargs):
        time_start = util.get_timestamp(kwargs.get('time_start'))
        time_end = util.get_timestamp(kwargs.get('time_end'))
        if time_end < time_start:
            time_start, time_end = time_end, time_start

        # reportCategory is ignored

        data = copy.deepcopy(kwargs)
        data.update({
            'time_start': str(time_start),
            'time_end': str(time_end),
            'delivery_method': [
                "S3link"
            ],
            "delivery_format": "json",
        })

        AuthRequest.__init__(self, credentials, **data)


class GetReportProgressRequest(AuthRequest):
    def __init__(self, credentials=None, token=None):
        AuthRequest.__init__(self, credentials, token=token)
