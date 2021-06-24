import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import mxnet as mx
import logging
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
# from greedy import generate_low_degree_g

import cProfile
import pstats
from pstats import SortKey

max_out_degree = 4


def generate_low_degree_g(num_nodes=20, min_out_degree=2, max_out_degree=4, weight_min=0.0, weight_max=1.0):

    G = nx.DiGraph()

    node_range = range(0, num_nodes)
    G.add_nodes_from(node_range)

    latitudes = np.random.uniform(0, 10, size=num_nodes)
    longitudes = np.random.uniform(0, 10, size=num_nodes)
    lat_dict=dict(zip(node_range, latitudes))
    lon_dict=dict(zip(node_range, longitudes))
    nx.set_node_attributes(G, values=lat_dict, name="y")
    nx.set_node_attributes(G, values=lon_dict, name="x")

    for node in G.nodes:
        tmp_nodes = list(G.nodes)
        tmp_nodes.remove(node)
        random.shuffle(tmp_nodes)

        out_neighbors = tmp_nodes[:random.randint(
            min_out_degree, max_out_degree)]

        for out_neighbor in out_neighbors:
            G.add_edge(node, out_neighbor, weight=random.uniform(
                weight_min, weight_max))

    return G, latitudes, longitudes



def generate_dataset_greedy(G):

    X, y = [], []

    for node in G.nodes:

        if G.out_degree(node) == 0:
            print('Node %d has 0 out degree' % node)
            continue

        init_weight_vec = np.ones(max_out_degree)

        for idx, out_edge in enumerate(G.out_edges(node)):
            init_weight_vec[idx] = G.get_edge_data(node, out_edge[1])['weight']

        out_neighbors = map(lambda t: (t[1], G.get_edge_data(
            node, t[1])['weight']),  G.out_edges(node))
    #     print(node, min(out_neighbors, key=lambda d: d[1]), len(out_neighbors), sorted(out_neighbors))

        label = min(out_neighbors, key=lambda d: d[1])[1]
        assert label == init_weight_vec[np.argmin(init_weight_vec)]
        X.append(init_weight_vec)
        y.append(label)

    return np.array(X), np.array(y)


def dist_eucl(x1, y1, x2, y2):
    return np.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)


def dist_cos(x0, y0, x1, y1, x2, y2):
    return np.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)

def encode_features(G, latitudes, longitudes, num_features, node_dst, node_src, features_vec, idx, out_edge_dst):
    features_vec[idx * num_features] = G.get_edge_data(node_src, out_edge_dst)['weight']
    features_vec[idx * num_features + 1] = latitudes[out_edge_dst]
    features_vec[idx * num_features + 2] = longitudes[out_edge_dst]
    features_vec[idx * num_features + 3] = dist_eucl(
                    longitudes[out_edge_dst], latitudes[out_edge_dst], longitudes[node_dst], latitudes[node_dst])
    features_vec[idx * num_features + 3] = dist_cos(longitudes[node_src], latitudes[node_src], 
                    longitudes[out_edge_dst], latitudes[out_edge_dst], longitudes[node_dst], latitudes[node_dst])



def generate_dataset_shortest(G, latitudes, longitudes, max_nodes_to_consider=90):
    # For all nodes in the graph
    # Find shortest path to rest of nodes in the graph
    # Label = first node of the route

    X, y = [], []

    # TODO define
    num_features = 5

    if len(G.nodes) <= max_nodes_to_consider:
        nodes = G.nodes
    else:
        nodes = list(G.nodes)[0:max_nodes_to_consider]

    for node_dst in nodes:
        for node_src in nodes:
            if node_dst == node_src:
                continue

            if G.out_degree(node_src) == 0:
                print('Node %d has 0 out degree' % node_src)
                continue


            try:
                optimal_next_node = nx.astar_path(G, node_src, node_dst)[1]
            except nx.exception.NetworkXNoPath:
                continue

            features_vec = np.ones(max_out_degree * num_features)
            
            label = get_label(G, node_src, optimal_next_node)



            for idx, out_edge in enumerate(G.out_edges(node_src)):
                out_edge_dst = out_edge[1]

                features_vec[idx * num_features] = G.get_edge_data(node_src, out_edge_dst)['weight']
                features_vec[idx * num_features + 1] = latitudes[out_edge_dst]
                features_vec[idx * num_features + 2] = longitudes[out_edge_dst]
                features_vec[idx * num_features + 3] = dist_eucl(
                                longitudes[out_edge_dst], latitudes[out_edge_dst], longitudes[node_dst], latitudes[node_dst])
                features_vec[idx * num_features + 3] = dist_cos(longitudes[node_src], latitudes[node_src], 
                                longitudes[out_edge_dst], latitudes[out_edge_dst], longitudes[node_dst], latitudes[node_dst])

            if label == None:
                continue
            X.append(features_vec)
            y.append(label)

    return np.array(X), np.array(y)

def get_label(G, node_src, optimal_next_node):
    label = None
    for idx, out_edge in enumerate(G.out_edges(node_src)):
        out_edge_dst = out_edge[1]
        if out_edge_dst == optimal_next_node:
            label = idx
    return label


def augment_dataset(X, y=None, augmentation_index=600):

    X_aug, y_aug = [], []
    indices = np.arange(len(X[0]))

    for _, x in enumerate(X):
        for _ in range(augmentation_index):

            X_aug.append(x[indices])
            y_aug.append(np.argmin(x[indices]))

    return np.array(X_aug), np.array(y_aug)


def build_model(context=mx.cpu()):

    data = mx.sym.var('data')
    label = mx.sym.var('softmax_label')

    fc2 = mx.sym.FullyConnected(data=data, num_hidden=32)
    fc2 = mx.sym.Activation(data=fc2, act_type="relu")

    fc3 = mx.sym.FullyConnected(data=fc2, num_hidden=max_out_degree)
    mlp = mx.sym.SoftmaxOutput(data=fc3, label=label)

    return mx.mod.Module(symbol=mlp, context=context)


def infer_next_node(G, cur_node):
    return min(map(lambda t: (t[1], G.get_edge_data(cur_node, t[1])['weight']),  G.out_edges(cur_node)), key=lambda d: d[1])


def nn_infer_next_node(G, latitudes, longitudes, cur_node, node_dst, model):

    num_features = 5

    input_vec = np.ones(4 * num_features)

    for idx, out_edge in enumerate(G.out_edges(cur_node)):
        out_edge_dst = out_edge[1]
        input_vec[idx] = G.get_edge_data(cur_node, out_edge[1])['weight']
        input_vec[idx * num_features] = G.get_edge_data(cur_node, out_edge_dst)['weight']
        input_vec[idx * num_features + 1] = latitudes[out_edge_dst]
        input_vec[idx * num_features + 2] = longitudes[out_edge_dst]
        input_vec[idx * num_features + 3] = dist_eucl(
                        longitudes[out_edge_dst], latitudes[out_edge_dst], longitudes[node_dst], latitudes[node_dst])
        input_vec[idx * num_features + 4] = dist_cos(longitudes[cur_node], latitudes[cur_node], 
                        longitudes[out_edge_dst], latitudes[out_edge_dst], longitudes[node_dst], latitudes[node_dst])

    out_neighbors = list(map(lambda t: (t[1], G.get_edge_data(
        cur_node, t[1])['weight']),  G.out_edges(cur_node)))

    pred_idx = np.argmax(model.predict(mx.io.NDArrayIter(
        np.array([input_vec]), np.array([0]))).asnumpy()[0])
    return out_neighbors[pred_idx]


def greedy_path_finder(G, latitudes, longitudes, src, dst, use_nn=False, model=None):

    path = [src]
    cur_node = src
    total_weights = .0

    while True:
        print(cur_node)
        if len(path) >= G.number_of_nodes():
            return path, total_weights, False

        if use_nn:
            next_node, weight = nn_infer_next_node(
                G, latitudes, longitudes, cur_node, dst, model) if use_nn else infer_next_node(G, cur_node)
        else:
            next_node, weight = infer_next_node(G, cur_node)
        total_weights += weight
        path.append(next_node)

        if next_node == dst:
            return path, total_weights, True

        cur_node = next_node


def check_greedy_path_finder_acc(G, latitudes, longitudes, model):

    identical_cnt = 0
    other_cnt = 0

    for src in G.nodes:
        for dst in G.nodes:

            if src == dst:
                continue

            path, _, found = greedy_path_finder(G, latitudes, longitudes, src, dst)
            nn_path, _, nn_found = greedy_path_finder(
                G, latitudes, longitudes, src, dst, use_nn=True, model=model)

            if path == nn_path:
                identical_cnt += 1
            else:
                other_cnt += 1

    return identical_cnt, other_cnt


def do_stuff():
    G, lats, longs = generate_low_degree_g(num_nodes=100)

    # nx.draw(G, with_labels=True)
    # plt.show()

    # max_out_degree = max(G.out_degree, key=lambda d: d[1])[1]


    X, y = generate_dataset_shortest(G, lats, longs)

    # X, y = augment_dataset(features, labels, augmentation_index=1)

    # indices = np.arange(len(X_aug))
    # np.random.shuffle(indices)
    # X, y =  X_aug[indices], y_aug[indices]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.8, random_state=42)

    batch_size = 20

    train_iter = mx.io.NDArrayIter(X, y, batch_size, shuffle=True)
    val_iter = mx.io.NDArrayIter(X, y, batch_size=batch_size)

    logging.getLogger().setLevel(logging.DEBUG)  # logging to stdout
    model = build_model()
    model.bind(data_shapes=train_iter.provide_data,
               label_shapes=train_iter.provide_label)
    model.init_params()

    model.fit(train_iter,  # train data
              eval_data=val_iter,  # validation data
              optimizer='adam',  # use SGD to train
              #               optimizer_params={'learning_rate':0.01, 'momentum': 0.9},
              eval_metric='acc',  # report accuracy during training
              # output progress for each 100 data batches
              batch_end_callback=mx.callback.Speedometer(batch_size, 10),
              num_epoch=5)  # train for at most 10 dataset passes

    identical_cnt, other_cnt = check_greedy_path_finder_acc(G, lats, longs, model)

    print('identical_cnt=%d, other_cnt=%d' % (identical_cnt, other_cnt))

    # pred_train = np.argmax(model.predict(mx.io.NDArrayIter(
    #     X_train, y_train, batch_size=batch_size)).asnumpy(), axis=1)
    # print('Acc on training set %f' % accuracy_score(y_train, pred_train))

    # pred_test = np.argmax(model.predict(mx.io.NDArrayIter(
    #     X_test, y_test, batch_size=batch_size)).asnumpy(), axis=1)
    # print('Acc on test set %f' % accuracy_score(y_test, pred_test))

    # graph_sizes = [20, 100, 500, 1000]
    # # graph_sizes = [20, 100]
    # stats = [[] for _ in range(len(graph_sizes))]
    # number_of_tests = 10

    # for idx, num_nodes in enumerate(graph_sizes):

    #     print('Working on graphs with %d nodes' % num_nodes)
    #     for i in range(number_of_tests):

    #         if i > 0 and i % 10 == 0:
    #             print("Processed %d graphs" % i)

    #         G_1, lats_1, longs_1 = generate_low_degree_g(num_nodes=num_nodes)
    #         X_test, y_test = generate_dataset_shortest(G_1, lats_1, longs_1)

    #         pred_test = np.argmax(model.predict(
    #             mx.io.NDArrayIter(X_test, y_test)).asnumpy(), axis=1)
    #         acc = accuracy_score(y_test, pred_test)
    #         stats[idx].append(acc)

    # for idx, stat in enumerate(stats):
    #     stat_mean = np.mean(stat)
    #     stat_std = np.std(stat)
    #     label = u'%d nodes, μ=%f, σ=%f' % \
    #             (graph_sizes[idx], stat_mean, stat_std)
    #     plt.scatter(list(range(number_of_tests)), stat, label=label)

    # plt.legend(loc='best')
    # plt.show()


if __name__ == "__main__":
    cProfile.run('do_stuff()', 'learnstats')
    p = pstats.Stats('learnstats')
    p.sort_stats(SortKey.TIME)
    p.print_stats(20)
