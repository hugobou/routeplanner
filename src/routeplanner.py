import logging
import random
import osmnx as ox

MAX_ITERATIONS = 1000
INVALID_NODE = -1


class RoutePlanner:
    def __init__(self, model, feature_encoder):
        self.model = model
        self.feature_encoder = feature_encoder

    def get_route_gps(self, graph, origin_point, destination_point):
        node_src = ox.distance.nearest_nodes(graph, origin_point[0], origin_point[1])
        node_dst = ox.distance.nearest_nodes(graph, destination_point[0], destination_point[1])
        route, valid = self.get_route(graph, node_src, node_dst)

        return route, valid

    def get_route(self, graph, node_src, node_dst):
        route = [node_src]
        visited = [node_src]
        node_cur = node_src

        while node_cur != node_dst:
            if len(visited) > MAX_ITERATIONS:
                logging.error("get_route reached iter limit: node_src=%d, node_dst=%d" % (node_src, node_dst))
                return route, False

            logging.debug("get_route: node_cur=%d" % node_cur)
            node_next = self.select_next_node(graph, visited, node_cur, node_dst)
            if node_next != INVALID_NODE:
                route.append(node_next)
                visited.append(node_next)
                node_cur = node_next
            else:
                logging.debug("get_route: walk back")
                del route[-1]
                node_cur = route[-1]

        return route, True

    def select_next_node(self, graph, visited, node_cur, node_dst):
        out_edges = list(filter(lambda edge: edge[1] not in visited, graph.out_edges(node_cur)))
        logging.debug("select_next_node: out_edges=%s" % out_edges)

        if len(out_edges) == 0:
            # TODO test
            return INVALID_NODE
        elif len(out_edges) == 1:
            node_next = out_edges[0][1]
        else:
            node_next = self.infer_next_node(graph, out_edges, node_cur, node_dst)
        return node_next

    def infer_next_node(self, graph, out_edges, node_cur, node_dst):
        if len(out_edges) == 0:
            raise RuntimeError("error in infer_next_node: len(out_edges) == 0")

        features_vector = self.feature_encoder.encode(graph, out_edges, node_cur, node_dst)
        index = self.model.predict(features_vector)

        if index < len(out_edges):
            next_node = out_edges[index][1]
        else:
            next_node = random.choice(out_edges)[1]
            logging.debug("infer_next_node: random choice next_node=%d" % next_node)

        return next_node
