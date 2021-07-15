import Features as feat


def get_route(model, graph, node_src, node_dst):
    route = [node_src]
    node_cur = node_src
    node_prev = None

    while node_cur != node_dst:
        node_next = select_next_node(graph, model, route, node_cur, node_dst)
        route.append(node_next)
        node_cur = node_next

    return route


def select_next_node(graph, model, route, node_cur, node_dst):

    out_edges = list(filter(lambda edge: edge[1] not in route, graph.out_edges(node_cur)))

    if len(out_edges) == 1:
        node_next = out_edges[0][1]
    else:
        node_next = infer_next_node(model, graph, out_edges, node_cur, node_dst)
    return node_next


def infer_next_node(model, graph, out_edges, node_cur, node_dst):
    if len(out_edges) == 0:
        # TODO define proper exception
        raise RuntimeError("Woops")

    features_vector = feat.encode_features(graph, out_edges, node_cur, node_dst)
    index = model.predict(features_vector)
    next_node = out_edges[index][1]

    # TODO deal with no prediction
    return next_node