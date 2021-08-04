import unittest

import application as app


class ApplicationTest(unittest.TestCase):
    def test_constructor(self):
        app.application_creator(gml_file_name="/data/madrid.gml",
                                model_params_file_name="/home/hugo/PycharmProjects/routeplanner/test/model_params")

