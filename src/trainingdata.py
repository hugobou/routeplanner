import random
import networkx as nx
import numpy as np
import concurrent
import features as feat


def random_node(graph):
    return random.choice(list(graph.nodes))


def get_label(graph, src, dst):
    label = list(map(lambda t:  t[1], graph.out_edges(src))).index(dst)
    return label


def generate_training_set(graph, n_samples):
    features = []
    labels = []
    # TODO pass as argument
    feature_encoder = feat.FeaturesEncoder()

    while len(labels) <= n_samples:
        src = random_node(graph)
        dst = random_node(graph)
        if dst == src:
            continue

        try:
            path = nx.astar_path(graph, src, dst)
        except nx.exception.NetworkXNoPath:
            continue

        node_pairs = get_node_pairs(path)
        for (src, dst) in node_pairs:
            if len(graph.out_edges(src)) < 2:
                continue
            features.append(feature_encoder.encode(graph, list(graph.out_edges(src)), src, dst))
            labels.append(get_label(graph, src, dst))
            if len(labels) % 100 == 0:
                print("Generating training data: %d samples generated" % len(labels))

    return np.array(features), np.array(labels)


def get_node_pairs(path):
    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]