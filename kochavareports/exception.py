import requests


class HttpException(Exception):
    def __init__(self, httpException):
        self.httpException = httpException
        Exception.__init__(self, str(httpException))

    def is_connection_error(self):
        return isinstance(self.httpException, (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.SSLError))

    def _is_http_error(self):
        return isinstance(self.httpException, requests.exceptions.HTTPError)

    def is_client_error(self):
        return self._is_http_error() and (
            400 <= self.httpException.response.status_code < 500)

    def is_server_error(self):
        return self._is_http_error() and (
            self.httpException.response.status_code >= 500)


class ApiException(Exception):
    pass


class ApiCredentialsException(ApiException):
    pass


class ApiResponseException(ApiException):
    def __init__(self, message, response=None):
        ApiException.__init__(self, message)
        self.response = response


class PollMaxRetryException(ApiException):
    pass
