from __future__ import absolute_import

import unittest2

import requests
import json
import mock

from kochavareports import client, constant, exception, response

from kochavareports import KochavaCredentials, KochavaClient


class TestClient(unittest2.TestCase):

    TEST_URL = 'http://whatever.url'
    TEST_DATA = {
        'dummy': 'whatever'
    }

    def _make_credentials(self):
        return KochavaCredentials(api_key='api key',
                                  app_guid='app guid')

    def _make_client(self):
        return KochavaClient(self._make_credentials())

    @mock.patch('kochavareports.client.requests.get')
    def test_get_http_error(self, mock_get):
        mock_response = mock.Mock()
        http_error = requests.exceptions.RequestException()
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response
        with self.assertRaises(exception.HttpException):
            self._make_client()._get_data(self.TEST_URL)

        mock_get.assert_called_once_with(self.TEST_URL)
        self.assertEqual(1, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_response.json.call_count)

    @mock.patch('kochavareports.client.requests.post')
    def test_post_http_error(self, mock_post):
        mock_response = mock.Mock()
        http_error = requests.exceptions.RequestException()
        mock_response.raise_for_status.side_effect = http_error
        mock_post.return_value = mock_response
        with self.assertRaises(exception.HttpException):
            self._make_client()._post_data(self.TEST_URL, self.TEST_DATA)

        mock_post.assert_called_once_with(self.TEST_URL,
                                          data=json.dumps(self.TEST_DATA))
        self.assertEqual(1, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_response.json.call_count)

    @mock.patch('kochavareports.client.requests.get')
    def test_get_json_error(self, mock_get):
        mock_response = mock.Mock()
        mock_response.return_value = ''
        mock_response.json.side_effect = ValueError()
        mock_get.return_value = mock_response
        with self.assertRaises(exception.ApiException):
            self._make_client()._get_data(self.TEST_URL)
        self.assertEqual(1, mock_response.json.call_count)

    @mock.patch('kochavareports.client.requests.post')
    def test_post_json_error(self, mock_post):
        mock_response = mock.Mock()
        mock_response.return_value = ''
        mock_response.json.side_effect = ValueError()
        mock_post.return_value = mock_response
        with self.assertRaises(exception.ApiException):
            self._make_client()._post_data(self.TEST_URL, self.TEST_DATA)
        self.assertEqual(1, mock_response.json.call_count)

    @mock.patch('kochavareports.client.time.sleep')
    @mock.patch('kochavareports.client.requests.post')
    @mock.patch('kochavareports.client.Client.get_report_progress')
    def test_poll_report_max_retries_exceeded(self, mock_progress, mock_post,
                                              mock_sleep):
        response_data = {
            'status': 'queued'
        }
        mock_response = mock.Mock()
        mock_response.json.return_value = response_data
        mock_post.return_value = mock_response
        mock_progress.return_value = response.GetReportProgressResponse(
                                                response_data)
        token = '12345667'
        retry_interval_seconds = 3
        start_delay_seconds = 15
        max_retries = 60

        with self.assertRaises(exception.PollMaxRetryException):
            self._make_client().poll_report(
                token,
                retry_interval_seconds=retry_interval_seconds,
                start_delay_seconds=start_delay_seconds,
                max_retries=max_retries)

        # checking time.sleep() calls would verify that all input parameters
        # are used correctly:
        sleep_calls = [mock.call(start_delay_seconds)] + \
                      [mock.call(retry_interval_seconds)] * max_retries
        self.assertEqual(sleep_calls, mock_sleep.call_args_list)

        # finally, check that get_report_progress() is called
        # `max_retries` times with the token parameter:
        progress_calls = [mock.call(token)] * max_retries
        self.assertEqual(progress_calls, mock_progress.call_args_list)

    @mock.patch('kochavareports.client.time.sleep')
    @mock.patch('kochavareports.client.Client.read_report')
    @mock.patch('kochavareports.client.Client.get_report_progress')
    def test_poll_report_success(self, mock_progress, mock_read, mock_sleep):
        token = '1234456765'
        response_queued = {
            'status': 'queued'
        }
        response_completed = {
            'status': 'completed',
            'report': 'http://some.url/whatever'
        }
        response_result = {
            'click_count': 10,
            'install_count': 2,
        }

        ping_times = 3  # for testing purposes it should be lower than
        # `max_retries`, which defaults 60 in this test

        mock_progress.side_effect = \
            [response.GetReportProgressResponse(response_queued)] * ping_times + \
            [response.GetReportProgressResponse(response_completed)]
        mock_read.return_value = response_result

        result = self._make_client().poll_report(token)

        # read_report() result should be the same as poll_report result:
        self.assertEqual(result, response_result)

        # read_report() should be called exactly once with the returned url:
        mock_read.assert_called_once_with(response_completed['report'])

        # get_report_progress() should be called internally exactly like
        # specified here: just the token, (ping_times + 1) times in total,
        # in the specified order
        progress_calls = [mock.call(token)] * (ping_times + 1)
        self.assertEqual(progress_calls, mock_progress.call_args_list)
