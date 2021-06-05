import Features as feat

def get_route(model, graph, node_src, node_dst):
    route = [node_src]
    node_cur = node_src

    while node_cur != node_dst:
        node_next = infer_next_node(model, graph, node_dst, node_cur)

        route.append(node_next)

        node_cur = node_next

    return route


def infer_next_node(model, graph, node_dst, node_cur):
    features_vector = feat.encode_features(graph, node_cur, node_dst)
    index = model.predict(features_vector)
    next_node = list(graph.out_edges(node_cur))[index][1]

    # TODO deal with no prediction
    return next_node