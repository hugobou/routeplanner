import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import numpy as np
import graphcreator as gc
import features as feat

from features import NUM_FEATURES, FEATURE_LENGTH


class FeaturesTest(unittest.TestCase):
    def test_encode_features(self):
        l = list(range(5))
        graph = gc.generate_path(5, x=l, y=l, w=l)
        out_edges = graph.out_edges(0)
        features = feat.FeaturesEncoder().encode(graph, out_edges, 0, 1)
        self.assertEqual(FEATURE_LENGTH, len(features))
        np.testing.assert_array_almost_equal([0.0, 1.0, 1.0, 0.0, 1.0, 0.0], features[0:NUM_FEATURES], 0.0000001)
        np.testing.assert_array_almost_equal(np.ones(4*NUM_FEATURES), features[NUM_FEATURES:FEATURE_LENGTH], 0.0000001)

    def test_encode_features_empty_out_edges_exception(self):
        graph = gc.generate_path(5)
        out_edges = []
        self.assertRaises(RuntimeError, feat.FeaturesEncoder().encode, graph, out_edges, 0, 1)

    def test_encode_features_more_edges_than_allowed_last_edge_ignored(self):
        graph = gc.generate_hardcoded_graph_too_many_connections()
        out_edges = graph.out_edges(1)
        features = feat.FeaturesEncoder().encode(graph, out_edges, 1, 10)
        self.assertEqual(FEATURE_LENGTH, len(features))

