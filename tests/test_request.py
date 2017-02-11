from __future__ import absolute_import

import unittest2
import datetime

from mock import patch

from kochavareports import request, constant
from kochavareports import KochavaCredentials


class TestRequest(unittest2.TestCase):

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
            'time_start':'2017-01-01',
            'time_end':'2017-02-01'
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
        self.assertTrue(isinstance(r.data.get('time_start'), basestring))
        self.assertTrue(isinstance(r.data.get('time_end'), basestring))
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

    # @patch('pynsights.tasks.s3_upload._get_file_io')
    # @patch('pynsights.tasks.s3_upload.extract_and_upload')
    # def test_refresh_data_sources_called(self, mock_extract_and_upload,
    #                                      mock_get_file_io):
    #     # It does not matter what mock_get_file_io returns, as long as it's not
    #     # None
    #     data_source_id = 'test_datasource'

    #     mock_get_file_io.return_value = object()
    #     mock_extract_and_upload.return_value = [data_source_id]

    #     self._create_caching_key(PROVIDER, PROVIDER)
    #     self._create_caching_key(PROVIDER, QUERY_COLLECTION)

    #     _import_csv_data_from_s3('bucket', 'users/foo-bar')

    #     query_cache = Caching.get(QUERY_COLLECTION, CACHE_KEY)
    #     provider_cache = Caching.get(PROVIDER, CACHE_KEY)

    #     self.assertEqual(query_cache, None)
    #     self.assertEqual(provider_cache, None)
