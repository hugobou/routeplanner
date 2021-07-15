import unittest

import osmnx as ox

import GraphCreator as gc
import TrainingData as td


class TrainingDataCase(unittest.TestCase):
    def test_generate_training_set(self):
        graph = gc.generate_random_graph(10)
        features, labels = td.generate_training_set(graph, 20)

        self.assertGreaterEqual(len(features), 20)
        self.assertGreaterEqual(len(labels), 20)

        self.assertEqual(len(features[0]), 25)

    def test_generate_training_set_osm_data(self):
        ox.config(use_cache=True, log_console=True)

        graph = ox.graph_from_xml("../data/map.osm")

        features, labels = td.generate_training_set(graph, 20)

        self.assertGreaterEqual(len(features), 20)
        self.assertGreaterEqual(len(labels), 20)

        self.assertEqual(len(features[0]), 25)


if __name__ == '__main__':
    unittest.main()
