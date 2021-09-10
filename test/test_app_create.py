import unittest

import app_create


class ApplicationTest(unittest.TestCase):
    def test_app_create(self):
        app_create.app_create("../config/routeplanner.cfg")

    def test_read_config(self):
        (gml, pm, model) = app_create.read_config("test.cfg")

        self.assertEqual("foo.txt", gml)
        self.assertEqual("bar.txt", pm)
        self.assertEqual("baz.txt", model)