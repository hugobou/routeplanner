from unittest import TestCase
import csv

import osmnx as ox
import mapreader as mr
import pmparser as pm
import traffic as tr


class Test(TestCase):
    # TODO anotar cuanto tiempo es necesario para esto
    def test_update_traffic_info(self):
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


