import application as app
import osmnx as ox
import networkx as nx

app = app.application_creator("/home/hugo/PycharmProjects/routeplanner/data/madrid.gml",
                              "/home/hugo/PycharmProjects/routeplanner/test/model_params")

origin_point = (-3.6121729, 40.4224813)
destination_point = (-3.7090030, 40.4538682)

route, valid = app.get_route(origin_point, destination_point)

print(route)
print(valid)

G = app.graph
node_src = ox.distance.nearest_nodes(G, origin_point[0], origin_point[1])
node_dst = ox.distance.nearest_nodes(G, destination_point[0], destination_point[1])
route2 = nx.shortest_path(G, node_src, node_dst, weight='length')

print(node_dst)
print(route2)


