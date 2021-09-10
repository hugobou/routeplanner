import osmnx as ox
import networkx as nx

import app_create
import traffic as tr
import json

app = app_create.app_create()

origin_point = (-3.6121729, 40.4524813)
destination_point = (-3.7090030, 40.4538682)

with open('pm.xml') as xmlfile:
    tm_list = tr.parse_traffic_data(xmlfile.read(), debug=False)

app.update_traffic_info(tm_list)

print('get_formatted_route')
formatted = app.get_formatted_route(origin_point, destination_point)
print(json.dumps(formatted))

G = app.graph
node_src = ox.distance.nearest_nodes(G, origin_point[0], origin_point[1])
node_dst = ox.distance.nearest_nodes(G, destination_point[0], destination_point[1])
route2 = nx.shortest_path(G, node_src, node_dst, weight='length')

print(node_dst)
print(route2)


