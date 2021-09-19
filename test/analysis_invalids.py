import csv
import networkx as nx
from random import choice

import app_create
import traffic as tr
import logging

from train import add_weights

NUM_SAMPLES = 10000

logging.basicConfig(filename='routeplanner.log', level=logging.DEBUG)

app = app_create.app_create()
graph = app.graph

with open('pm.xml') as xmlfile:
    tm_list = tr.parse_traffic_data(xmlfile.read(), debug=False)
app.update_traffic_info_offline(tm_list)
add_weights(graph)

nodes = list(graph.nodes())


with open('analysis.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    with open('analysis_invalids.csv', 'w', buffering=1) as f:
        for row in reader:
            print(', '.join(row))
            node_src = int(row[0])
            node_dst = int(row[3])
            valid = float(row[6]) >= 0

            if valid:
                continue

            origin_point = (graph.nodes[node_src]['x'], graph.nodes[node_src]['y'])
            destination_point = (graph.nodes[node_dst]['x'], graph.nodes[node_dst]['y'])

            try:
                distance_actual_shortest = nx.algorithms.shortest_paths.generic.shortest_path_length(graph, node_src, node_dst,
                                                                                                     weight='weight',
                                                                                                     method='dijkstra')

                print("%d, %f, %f, %d, %f, %f,  %f\n" % (node_src, origin_point[0], origin_point[1],
                                                         node_dst, destination_point[0], destination_point[1],
                                                         distance_actual_shortest))
                f.write("%d, %f, %f, %d, %f, %f,  %f\n" % (node_src, origin_point[0], origin_point[1],
                                                           node_dst, destination_point[0], destination_point[1],
                                                           distance_actual_shortest))
            except nx.exception.NetworkXNoPath:
                print("%d, %f, %f, %d, %f, %f,  %f\n" % (node_src, origin_point[0], origin_point[1],
                                                         node_dst, destination_point[0], destination_point[1],
                                                         -1))
                f.write("%d, %f, %f, %d, %f, %f,  %f\n" % (node_src, origin_point[0], origin_point[1],
                                                           node_dst, destination_point[0], destination_point[1],
                                                           -1))

