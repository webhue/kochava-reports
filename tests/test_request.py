from __future__ import absolute_import

import unittest2
import datetime

from mock import patch

from kochavareports import request


class TestRequest(unittest2.TestCase):

    def test_(self):
        pass
        # TODO

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
