from __future__ import absolute_import

import unittest2
import datetime

from kochavareports import response, constant, exception


class TestResponse(unittest2.TestCase):

    def test_response(self):
        with self.assertRaises(ValueError):
            response.Response('invalid data format')
        with self.assertRaises(ValueError):
            response.Response({})
        with self.assertRaises(exception.ApiResponseException):
            response.Response({'status': 'error'})
        with self.assertRaises(exception.ApiCredentialsException):
            response.Response({
                'status': 'error',
                'error': 'API key is missing'
            })
        r = response.Response({'status': 'ok'})
        self.assertFalse(r.is_error())

    def test_valid_fields_response(self):
        with self.assertRaises(ValueError):
            response.GetValidFieldsResponse({'status': 'ok'})

    def test_valid_templates_response(self):
        with self.assertRaises(ValueError):
            response.GetTemplatesResponse({'status': 'ok'})

    def test_create_report_response(self):
        with self.assertRaises(ValueError):
            response.CreateReportResponse({'status': 'ok'})

    def test_progress_report_response(self):
        with self.assertRaises(ValueError):
            response.GetReportProgressResponse({'status': 'completed'})
        report_url = 'http://test.com/whatever'
        r = response.GetReportProgressResponse({
            'status': 'completed',
            'report': report_url
        })
        self.assertTrue(r.is_completed())
        self.assertEqual(r.get_report_url(), report_url)
