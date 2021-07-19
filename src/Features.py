import networkx as nx
import numpy as np

MAX_OUT_DEGREE = 5
NUM_FEATURES = 5

def dist_eucl(x1, y1, x2, y2):
    return np.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)

def dist_cos(x0, y0, x1, y1, x2, y2):
    v1 = [x1 - x0, y1 - y0]
    v2 = [x2 - x0, y2 - y0]
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def encode_features(graph, out_edges, node_cur, node_dst):
    if len(out_edges) == 0:
        # TODO define proper exception
        raise RuntimeError("Woops")

    longitudes = nx.get_node_attributes(graph, 'x')
    latitudes = nx.get_node_attributes(graph, 'y')

    features_vec = np.ones(MAX_OUT_DEGREE * NUM_FEATURES)

    for idx, out_edge in enumerate(out_edges):
        if idx >= MAX_OUT_DEGREE:
            break
        out_edge_dst = out_edge[1]

        # TODO: update features with OSM and traffic data
        # - Length
        # - Serv level
        # - Max speed
        try:
            features_vec[idx * NUM_FEATURES] = graph.get_edge_data(node_cur, out_edge_dst, 0)['maxspeed']
            features_vec[idx * NUM_FEATURES + 1] = latitudes[out_edge_dst]
            features_vec[idx * NUM_FEATURES + 2] = longitudes[out_edge_dst]
            features_vec[idx * NUM_FEATURES + 3] = dist_eucl(longitudes[out_edge_dst], latitudes[out_edge_dst],
                                                             longitudes[node_dst], latitudes[node_dst])
            features_vec[idx * NUM_FEATURES + 4] = dist_cos(longitudes[node_cur], latitudes[node_cur],
                                                            longitudes[out_edge_dst], latitudes[out_edge_dst],
                                                            longitudes[node_dst], latitudes[node_dst])
        except KeyError:
            print("Error with: ", graph.get_edge_data(node_cur, out_edge_dst))
            raise

    return features_vec