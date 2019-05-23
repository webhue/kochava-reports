from __future__ import absolute_import

import unittest

from kochavareports import request, constant
from kochavareports import KochavaCredentials
import six


class TestRequest(unittest.TestCase):

    def _make_credentials(self):
        return KochavaCredentials(api_key='api key',
                                  app_guid='app guid')

    def _make_data(self):
        return dict(key1='value1', key2='value2')

    def test_auth_request(self):
        credentials = self._make_credentials()
        data = self._make_data()
        r = request.AuthRequest(credentials, **data)
        for key, value in data.iteritems():
            self.assertEqual(r.data.get(key), value)
        for key, value in credentials.to_dict().iteritems():
            self.assertEqual(r.data.get(key), value)

    def test_report_columns_request(self):
        credentials = self._make_credentials()
        report = 'install'
        r = request.GetReportColumnsRequest(credentials, report=report)
        self.assertEqual(r.data.get('report'), report)
        for key, value in credentials.to_dict().iteritems():
            self.assertEqual(r.data.get(key), value)

    def test_create_report_request(self):
        credentials = self._make_credentials()
        reportCategory = constant.ReportCategory.SUMMARY
        empty_data = {}
        missing_traffic_data = {
            'time_start': '2017-01-01',
            'time_end': '2017-02-01'
        }
        required_data = missing_traffic_data.copy()
        required_data.update({
            'traffic': [
                'install'
            ]
        })
        with self.assertRaises(ValueError):
            request.CreateReportRequest(credentials, reportCategory=None,
                                        **required_data)
        with self.assertRaises(ValueError):
            request.CreateReportRequest(credentials,
                                        reportCategory=reportCategory,
                                        **empty_data)
        with self.assertRaises(ValueError):
            request.CreateReportRequest(credentials,
                                        reportCategory=reportCategory,
                                        **missing_traffic_data)
        r = request.CreateReportRequest(credentials,
                                        reportCategory=reportCategory,
                                        **required_data)
        for key, value in credentials.to_dict().iteritems():
            self.assertEqual(r.data.get(key), value)
        self.assertTrue(isinstance(r.data.get('time_start'), six.string_types))
        self.assertTrue(isinstance(r.data.get('time_end'), six.string_types))
        self.assertGreater(r.data.get('time_end'), r.data.get('time_start'))
        self.assertTrue(r.data.get('time_series'))
        self.assertTrue(r.data.get('delivery_method'))
        self.assertTrue(r.data.get('delivery_format'))

    def test_report_progress_request(self):
        credentials = self._make_credentials()
        token = '1234567890'
        r = request.GetReportProgressRequest(credentials, token=token)
        self.assertEqual(r.data.get('token'), token)
        for key, value in credentials.to_dict().iteritems():
            self.assertEqual(r.data.get(key), value)
