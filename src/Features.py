import networkx as nx
import numpy as np

def dist_eucl(x1, y1, x2, y2):
    return np.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)

def dist_cos(x0, y0, x1, y1, x2, y2):
    v1 = [x1 - x0, y1 - y0]
    v2 = [x2 - x0, y2 - y0]
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def encode_features(graph, node_cur, node_dst):
    max_out_degree = max(graph.out_degree, key=lambda d: d[1])[1]
    num_features = 5

    longitudes = nx.get_node_attributes(graph, 'x')
    latitudes = nx.get_node_attributes(graph, 'y')

    features_vec = np.ones(max_out_degree * num_features)

    for idx, out_edge in enumerate(graph.out_edges(node_cur)):
        out_edge_dst = out_edge[1]

        features_vec[idx * num_features] = graph.get_edge_data(node_cur, out_edge_dst)['weight']
        features_vec[idx * num_features + 1] = latitudes[out_edge_dst]
        features_vec[idx * num_features + 2] = longitudes[out_edge_dst]
        features_vec[idx * num_features + 3] = dist_eucl(longitudes[out_edge_dst], latitudes[out_edge_dst],
                                                         longitudes[node_dst], latitudes[node_dst])
        features_vec[idx * num_features + 4] = dist_cos(longitudes[node_cur], latitudes[node_cur],
                                                        longitudes[out_edge_dst], latitudes[out_edge_dst],
                                                        longitudes[node_dst], latitudes[node_dst])
    return features_vec