from unittest import TestCase, main

import overdoses

import pandas as pd
from pandas.util.testing import assert_series_equal


class OverdosesTestCase(TestCase):
    @staticmethod
    def test_get_database_data():
        actual_result = overdoses.OverdoseDatabase().query(2013, 'Alcohol')
        actual_result = pd.DataFrame(actual_result).iloc[0]

        expected_result = pd.Series([115, 'Alcohol', 'Allegany', 2013, 2])
        actual_result.rename_axis(None)

        assert_series_equal(actual_result, expected_result, check_names=False)

    def test_get_database_data_count(self):
        actual_result = overdoses.OverdoseDatabase().query(2015, 'Cocaine')
        actual_result = len(pd.DataFrame(actual_result).index)
        self.assertTrue(actual_result, 24)


if __name__ == '__main__':
    main()
