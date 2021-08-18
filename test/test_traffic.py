import unittest
from unittest import TestCase
import csv

import osmnx as ox
import mapreader as mr
import traffic
import traffic as tr
import graphcreator as gc


class Test(TestCase):
    # TODO anotar cuanto tiempo es necesario para esto
    @unittest.skip("Run manually only")
    def generate_offline_tm_dict(self):
        graph = mr.ReadMap("../data/madrid.gml")
        # Project to UTM
        graph = ox.projection.project_graph(graph)

        with open('traffic_measurement_points.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            header = ['pm', 'src', 'dst']
            writer.writerow(header)

            with open('pm.xml') as xmlfile:
                tmlist = traffic.parse_traffic_data(xmlfile.read(), debug=False)
                for tm in tmlist:
                    print(tm)
                    s, d, i = ox.distance.nearest_edges(graph, tm.x, tm.y)
                    writer.writerow([tm.id, s, d])

    def test_read_tm_dict(self):
        filename = 'traffic_measurement_points_test.csv'

        tm_dict = tr.read_tm_dict(filename)
        self.assertEqual(len(tm_dict), 4)
        self.assertEqual(tm_dict[1], (21, 31))
        self.assertEqual(tm_dict[2], (22, 32))
        self.assertEqual(tm_dict[11], (211, 311))
        self.assertEqual(tm_dict[12], (212, 312))

    def test_reset_traffic_status(self):
        graph = gc.generate_hardcoded_graph()

        tr.reset_traffic_info(graph)

        for s, d, meta in graph.edges.data():
            self.assertIn('traffic', meta)
            self.assertEqual(meta['traffic'], 0)

    def test_update_traffic_status(self):
        DESC = ""
        X = "100000"
        Y = "100000"
        graph = gc.generate_hardcoded_graph()

        tr.reset_traffic_info(graph)

        tm_dict = {101: (1, 2), 102: (2, 3), 103: (1, 4), 104: (3, 6)}
        tm_list = [
            tr.TrafficMeasurement(101, DESC, X, Y, 1),
            tr.TrafficMeasurement(102, DESC, X, Y, 2),
            tr.TrafficMeasurement(103, DESC, X, Y, 3),
            tr.TrafficMeasurement(104, DESC, X, Y, 4),
        ]
        tr.update_traffic_info(graph, tm_list, tm_dict)

        self.assertEqual(graph.get_edge_data(1, 2)[0]['traffic'], 1)
        self.assertEqual(graph.get_edge_data(2, 3)[0]['traffic'], 2)
        self.assertEqual(graph.get_edge_data(1, 4)[0]['traffic'], 3)
        self.assertEqual(graph.get_edge_data(3, 6)[0]['traffic'], 4)

        self.assertEqual(graph.get_edge_data(1, 5)[0]['traffic'], 0)
        self.assertEqual(graph.get_edge_data(5, 1)[0]['traffic'], 0)

        self.assertEqual(graph.get_edge_data(5, 8)[0]['traffic'], 0)
        self.assertEqual(graph.get_edge_data(8, 5)[0]['traffic'], 0)

    def test_parse_traffic_data(self):
        with open('pm.xml') as xmlfile:
            tmlist = traffic.parse_traffic_data(xmlfile.read(), debug=True)
            self.assertGreater(len(tmlist), 0)
