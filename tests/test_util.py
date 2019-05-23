from __future__ import absolute_import

import unittest
import datetime

from kochavareports import util


class TestUtil(unittest.TestCase):

    def test_timezone_timestamp(self):
        timezone = 'US/Pacific'
        result = util.get_timestamp('2016-11-07', timezone)
        self.assertEqual(result, 1478476800)
        result = util.get_timestamp('2016-11-07 00:00:00', timezone)
        self.assertEqual(result, 1478476800)
        result = util.get_timestamp(datetime.datetime(2016, 11, 7), timezone)
        self.assertEqual(result, 1478476800)
        result = util.get_timestamp(datetime.date(2016, 11, 7), timezone)
        self.assertEqual(result, 1478476800)
        result = util.get_timestamp('1478476800', timezone)
        self.assertEqual(result, 1478476800)
        result = util.get_timestamp(1478476800, timezone)
        self.assertEqual(result, 1478476800)
