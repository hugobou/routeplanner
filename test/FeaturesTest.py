import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import numpy as np

import GraphCreator as gc
import Features as feat

class FeaturesTest(unittest.TestCase):
    def test_encode_features(self):
        l = list(range(5))
        graph = gc.generate_path(5, x=l, y=l, w=l)
        features = feat.encode_features(graph, 0, 1)
        self.assertEqual(5, len(features))
        np.testing.assert_array_almost_equal([0.0, 1.0, 1.0, 0.0, 1.0], features, 0.0000001)

    # TODO More tests, more complicated