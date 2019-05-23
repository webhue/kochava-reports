from __future__ import absolute_import
from . import util
from .exception import ApiResponseException, ApiCredentialsException


class Response(object):
    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError(
                "Invalid data returned, it must be a dictionary: " + str(data))
        if not len(data.keys()):
            raise ValueError(
                "Empty data returned: " + str(data))
        self.data = data

        self.validate()

    def __getattr__(self, name):
        return self.data.get(name, None)

    def __str__(self):
        return str(self.data)

    def __unicode__(self):
        # Note: this method is only called in Python 2
        return unicode(self.data)

    def is_error(self):
        return self.status is None or self.status.lower() == u'error'

    def validate(self):
        if(self.is_error()):
            if self.error and 'API KEY' in self.error.upper():
                raise ApiCredentialsException(self.error)
            raise ApiResponseException(self.error, self)


class GetValidFieldsResponse(Response):
    def validate(self):
        super(GetValidFieldsResponse, self).validate()
        if not self.valid_fields:
            raise ValueError("Fields list is missing or empty")


class GetTemplatesResponse(Response):
    def validate(self):
        super(GetTemplatesResponse, self).validate()
        if not self.template_values:
            raise ValueError("Template values are missing")


class CreateReportResponse(Response):
    def validate(self):
        super(CreateReportResponse, self).validate()
        if not self.report_token:
            raise ValueError("Report token is missing")


class GetReportProgressResponse(Response):
    def validate(self):
        super(GetReportProgressResponse, self).validate()
        if self.is_completed() and not self.report:
            raise ValueError("Report URL of completed report is missing")

    def is_completed(self):
        return self.status and self.status.lower() == u'completed'

    def get_report_url(self):
        if self.is_completed():
            return self.report or None
        return None

    @property
    def status_date(self):
        date = self.data.get('status_date', None)
        if date:
            return util.parse_str_datetime(date)
        return None
