import osmnx as ox
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

with open('analysis.csv', 'w', buffering=1) as f:
    for n in range(NUM_SAMPLES):
        node_src = choice(nodes)
        node_dst = choice(nodes)

        origin_point = (graph.nodes[node_src]['x'], graph.nodes[node_src]['y'])
        destination_point = (graph.nodes[node_dst]['x'], graph.nodes[node_dst]['y'])

        try:
            distance_actual_shortest = nx.algorithms.shortest_paths.generic.shortest_path_length(graph, node_src, node_dst,
                                                                                                 weight='weight',
                                                                                                 method='dijkstra')

            route_predicted, valid = app.get_route(origin_point, destination_point)

            distance_predicted = nx.classes.function.path_weight(graph, route_predicted, weight='weight')

            print("%d, %f, %f, %d, %f, %f,  %f, %f\n" % (node_src, origin_point[0], origin_point[1],
                                                         node_dst, destination_point[0], destination_point[1],
                                                         distance_actual_shortest, distance_predicted))
            f.write("%d, %f, %f, %d, %f, %f,  %f, %f\n" % (node_src, origin_point[0], origin_point[1],
                                                           node_dst, destination_point[0], destination_point[1],
                                                           distance_actual_shortest, distance_predicted))
        except nx.exception.NetworkXNoPath:
            print("%d, %f, %f, %d, %f, %f,  %f, %f\n" % (node_src, origin_point[0], origin_point[1],
                                                         node_dst, destination_point[0], destination_point[1],
                                                         -1, -1))
            f.write("%d, %f, %f, %d, %f, %f,  %f, %f\n" % (node_src, origin_point[0], origin_point[1],
                                                           node_dst, destination_point[0], destination_point[1],
                                                           -1, -1))

