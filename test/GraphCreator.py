import networkx as nx
import random
import numpy as np


def generate_low_degree_g(num_nodes=20, min_out_degree=2, max_out_degree=4, weight_min=0.0, weight_max=1.0):
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))

    for node in G.nodes:
        tmp_nodes = list(G.nodes)
        tmp_nodes.remove(node)
        random.shuffle(tmp_nodes)

        out_neighbors = tmp_nodes[:random.randint(min_out_degree, max_out_degree)]

        for out_neighbor in out_neighbors:
            G.add_edge(node, out_neighbor, weight=random.uniform(weight_min, weight_max))

    add_xy_to_nodes(G)

    return G


def generate_path(num_nodes, x=None, y=None, w=None):
    G = nx.path_graph(num_nodes, create_using=nx.DiGraph())
    add_xy_to_nodes(G, x, y)

    add_edge_weights(G, w)

    return G


def add_edge_weights(G, w):
    weight_dict = {}
    for idx, edge in enumerate(G.edges):
        if w != None:
            weight_dict[edge] = w[idx]
        else:
            weight_dict[edge] = np.random.uniform(0, 1)
    nx.set_edge_attributes(G, weight_dict, 'weight')


def add_xy_to_nodes(G, x=None, y=None):
    n = G.number_of_nodes()
    xx = x if x != None else np.random.uniform(0, 10, size=n)
    yy = y if y != None else np.random.uniform(0, 10, size=n)
    lat_dict = dict(zip(range(n), xx))
    lon_dict = dict(zip(range(n), yy))
    nx.set_node_attributes(G, values=lat_dict, name="y")
    nx.set_node_attributes(G, values=lon_dict, name="x")
