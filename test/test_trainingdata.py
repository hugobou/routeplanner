import unittest

import osmnx as ox

import graphcreator as gc
from model import trainingdata as td
import mapreader as mr
import traffic as tf
from model.features import FEATURE_LENGTH, FeaturesEncoder


class TrainingDataCase(unittest.TestCase):
    def test_generate_training_set(self):
        graph = gc.generate_random_graph(10)
        features, labels = td.generate_training_set(FeaturesEncoder(), graph, 20)

        self.assertGreaterEqual(len(features), 20)
        self.assertGreaterEqual(len(labels), 20)

        self.assertEqual(len(features[0]), FEATURE_LENGTH)

    def test_generate_training_set_osm_data(self):
        ox.config(use_cache=True, log_console=True)

        graph = mr.ReadMap("../data/madrid.gml")
        tf.reset_traffic_info(graph)

        features, labels = td.generate_training_set(FeaturesEncoder(), graph, 20)

        self.assertGreaterEqual(len(features), 20)
        self.assertGreaterEqual(len(labels), 20)

        self.assertEqual(len(features[0]), FEATURE_LENGTH)


if __name__ == '__main__':
    unittest.main()
