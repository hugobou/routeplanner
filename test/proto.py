import osmnx as ox
import networkx as nx

import application as app
import pmparser as pm
import traffic as tr

app = app.application_creator("/home/hugo/PycharmProjects/routeplanner/data/madrid.gml",
                              "/home/hugo/PycharmProjects/routeplanner/test/model_params")

origin_point = (-3.6121729, 40.4224813)
destination_point = (-3.7090030, 40.5538682)

tm_dict = tr.read_tm_dict('/home/hugo/PycharmProjects/routeplanner/data/traffic_measurement_points.csv')

with open('pm.xml') as xmlfile:
    tm_list = pm.parse_traffic_data(xmlfile.read(), debug=False)

tr.update_traffic_info(app.graph, tm_list, tm_dict)

route, valid = app.get_route(origin_point, destination_point)

print(route)
print(valid)

G = app.graph
node_src = ox.distance.nearest_nodes(G, origin_point[0], origin_point[1])
node_dst = ox.distance.nearest_nodes(G, destination_point[0], destination_point[1])
route2 = nx.shortest_path(G, node_src, node_dst, weight='length')

print(node_dst)
print(route2)


