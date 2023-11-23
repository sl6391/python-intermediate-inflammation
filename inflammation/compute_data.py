"""Module containing mechanism for calculating standard deviation between datasets.
"""

import glob
import os
import numpy as np

from inflammation import models, views
from unittest.mock import Mock
import numpy.testing as npt


class CSVDataSource:
    def __init__(self,dir_path):
        self.dir_path = dir_path

    def load_inflammation_data(self):
        files_of_interest = 'inflammation*.csv'
        data_file_paths = glob.glob(os.path.join(self.dir_path, files_of_interest))

        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation csv's found in path {self.dir_path}")

        data = map(models.load_csv, data_file_paths)
        return data


class JSONDataSource:
  """
  Loads all the inflammation JSON's within a specified folder.
  """
  def __init__(self, dir_path):
    self.dir_path = dir_path

  def load_inflammation_data(self):
    data_file_paths = glob.glob(os.path.join(self.dir_path, 'inflammation*.json'))
    if len(data_file_paths) == 0:
      raise ValueError(f"No inflammation JSON's found in path {self.dir_path}")
    data = map(models.load_json, data_file_paths)
    return list(data)


def compute_standard_deviation_by_day(data):
    means_by_day = map(models.daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))
    
    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)
    return daily_standard_deviation


def analyse_data(data_source):
    """Calculate the standard deviation by day between datasets

    Gets all the inflammation csvs within a directory, works out the mean
    inflammation value for each day across all datasets, then graphs the
    standard deviation of these means."""

    data = data_source.load_inflammation_data()

    daily_standard_deviation = compute_standard_deviation_by_day(data)

    graph_data = {
        'standard deviation by day': daily_standard_deviation,
    }

    return daily_standard_deviation
    #views.visualize(graph_data)


def test_compute_data_mock_source():
    from inflammation.compute_data import analyse_data
    data_source = Mock()
    data_source.load_inflammation_data.return_value = [[[0, 2, 0]], [[0, 1, 0]]]

    result = analyse_data(data_source)
    npt.assert_array_almost_equal(result, [0, math.sqrt(0.25) ,0])
    