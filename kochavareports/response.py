import util
from .exception import ApiResponseException, ApiCredentialsException


class Response(object):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        return self.data.get(name, None)

    def __str__(self):
        return str(self.data)

    def __unicode__(self):
        return unicode(self.data)

    def is_error(self):
        return self.status is None or self.status.lower() == u'error'

    def validate(self):
        if(self.is_error()):
            if self.error and 'API KEY' in self.error.upper():
                raise ApiCredentialsException(self.error)
            raise ApiResponseException(self.error, self)


class GetValidFieldsResponse(Response):
    def get_valid_fields(self):
        self.validate()
        return self.valid_fields or []


class GetTemplatesResponse(Response):
    def get_template_values(self):
        self.validate()
        return self.template_values or []


class CreateReportResponse(Response):
    def get_report_token(self):
        self.validate()
        return self.report_token


class GetReportProgressResponse(Response):
    def is_completed(self):
        return self.status is None or self.status.lower() == u'completed'

    def get_report_url(self):
        self.validate()
        if self.is_completed():
            return self.report or None
        return None

    @property
    def status_date(self):
        date = self.data.get('status_date', None)
        if date:
            return util.parse_str_datetime(date)
        return None
