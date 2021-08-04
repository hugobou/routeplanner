import unittest
from unittest import TestCase
import csv

import osmnx as ox
import mapreader as mr
import pmparser as pm
import traffic as tr


class Test(TestCase):
    # TODO anotar cuanto tiempo es necesario para esto
    @unittest.skip("Run manually only")
    def generate_offline_tm_dict(self):
        graph = mr.ReadMap("/home/hugo/PycharmProjects/routeplanner/proto/madrid.gml")
        # Project to UTM
        graph = ox.projection.project_graph(graph)

        with open('traffic_measurement_points.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            header = ['pm', 'src', 'dst']
            writer.writerow(header)

            with open('pm.xml') as xmlfile:
                tmlist = pm.parse_traffic_data(xmlfile.read(), debug=False)
                for tm in tmlist:
                    print(tm)
                    s, d, i = ox.distance.nearest_edges(graph, tm.x, tm.y)
                    writer.writerow([tm.id, s, d])

    def test_create_tm_dict(self):
        filename = 'traffic_measurement_points_test.csv'

        tm_dict = tr.read_tm_dict(filename)
        self.assertEqual(len(tm_dict), 4)
        self.assertEqual(tm_dict[1], (21, 31))
        self.assertEqual(tm_dict[2], (22, 32))
        self.assertEqual(tm_dict[11], (211, 311))
        self.assertEqual(tm_dict[12], (212, 312))

