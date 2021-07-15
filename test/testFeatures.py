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
        out_edges = graph.out_edges(0)
        features = feat.encode_features(graph, out_edges, 0, 1)
        self.assertEqual(25, len(features))
        np.testing.assert_array_almost_equal([0.0, 1.0, 1.0, 0.0, 1.0], features[0:5], 0.0000001)
        np.testing.assert_array_almost_equal(np.ones(20), features[5:25], 0.0000001)

    def test_encode_features_empty_out_edges_exception(self):
        graph = gc.generate_path(5)
        out_edges = []
        self.assertRaises(RuntimeError, feat.encode_features, graph, out_edges, 0, 1)

    def test_encode_features_more_edges_than_allowed_last_edge_ignored(self):
        graph = gc.generate_hardcoded_graph_too_many_connections()
        out_edges = graph.out_edges(1)
        features = feat.encode_features(graph, out_edges, 1, 10)
        self.assertEqual(25, len(features))


    # TODO More tests, more complicated
