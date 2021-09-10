import unittest

import app_create


class ApplicationTest(unittest.TestCase):
    def test_app_create(self):
        app_create.app_create(gml_file_name="../data/madrid.gml",
                              pm_dict_file_name="../data/traffic_measurement_points.csv",
                              model_params_file_name="../test/model_params")

