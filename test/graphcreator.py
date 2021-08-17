import networkx as nx
import random
import numpy as np

import traffic as tr


def generate_random_graph(num_nodes=20, min_out_degree=2, max_out_degree=4, weight_min=0.0, weight_max=1.0):
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))

    for node in G.nodes:
        tmp_nodes = list(G.nodes)
        tmp_nodes.remove(node)
        random.shuffle(tmp_nodes)

        out_neighbors = tmp_nodes[:random.randint(min_out_degree, max_out_degree)]

        for out_neighbor in out_neighbors:
            G.add_edge(node, out_neighbor, key=0, speed_kph=random.uniform(weight_min, weight_max))

    add_xy_to_nodes(G)
    add_edge_traffic_zero(G)

    return G


def generate_path(num_nodes, x=None, y=None, w=None):
    G = nx.path_graph(num_nodes, create_using=nx.DiGraph())
    add_xy_to_nodes(G, x, y)

    add_edge_speed_kph(G, w)
    add_edge_traffic_zero(G)

    return G

def generate_hardcoded_graph():
    G = nx.DiGraph()
    G.add_nodes_from(range(1, 11))
    add_xy_to_nodes(G)

    add_bidir_edge(G, 1, 2)
    add_bidir_edge(G, 1, 4)
    add_bidir_edge(G, 1, 5)
    add_bidir_edge(G, 2, 3)
    add_bidir_edge(G, 3, 6)
    add_bidir_edge(G, 3, 7)
    add_bidir_edge(G, 4, 8)
    add_bidir_edge(G, 5, 6)
    add_bidir_edge(G, 5, 8)
    add_bidir_edge(G, 6, 9)
    add_bidir_edge(G, 7, 10)

    add_description_to_nodes(G)
    return G


def generate_hardcoded_graph_too_many_connections():
    G = generate_hardcoded_graph()

    add_bidir_edge(G, 1, 6)
    add_bidir_edge(G, 1, 7)
    add_bidir_edge(G, 1, 8)


    return G


def add_bidir_edge(G, n1, n2, w=1):
    G.add_edge(n1, n2, key=0, speed_kph=w, traffic=0)
    G.add_edge(n2, n1, key=0, speed_kph=w, traffic=0)


def add_edge_speed_kph(G, w):
    weight_dict = {}
    for idx, edge in enumerate(G.edges):
        if w != None:
            weight_dict[edge] = w[idx]
        else:
            weight_dict[edge] = np.random.uniform(30, 100)
    nx.set_edge_attributes(G, weight_dict, 'speed_kph')


def add_edge_traffic_zero(G):
    tr.reset_traffic_info(G)


def add_xy_to_nodes(G, x=None, y=None):
    n = G.number_of_nodes()
    xx = x if x != None else np.random.uniform(0, 10, size=n)
    yy = y if y != None else np.random.uniform(0, 10, size=n)
    lat_dict = dict(zip(G.nodes(), xx))
    lon_dict = dict(zip(G.nodes(), yy))
    nx.set_node_attributes(G, values=lat_dict, name="y")
    nx.set_node_attributes(G, values=lon_dict, name="x")


def add_description_to_nodes(G):
    names = [str(edge) for edge in G.edges()]
    names_dict = dict(zip(G.edges(), names))
    nx.set_edge_attributes(G, values=names_dict, name="name")