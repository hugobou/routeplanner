import unittest
import GraphCreator as gc
import RoutePlanner as rp


class ModelStubAlwaysConstant:
    def __init__(self, constant):
        self._constant = constant

    def predict(self, ignored):
        return self._constant


class ModelStubAlwaysZero:
    def predict(self, ignored):
        return 0


class ModelStubAlwaysError:
    def predict(self, ignored):
        raise RuntimeError("ModelStubAlwaysError.predict always throws error")


# TODO: error handling. src/dst Nodes not in graph.

class RoutePlannerTest(unittest.TestCase):
    def test_infer_node_happy_flow(self):
        model = ModelStubAlwaysZero()

        graph = gc.generate_path(5)
        out_edges = list(graph.out_edges(0))
        next_node = rp.infer_next_node(model, graph, out_edges, 0, 1)
        self.assertEqual(1, next_node)

    def test_infer_node_invalid_prediction_random_choice(self):
        model = ModelStubAlwaysConstant(5)

        graph = gc.generate_hardcoded_graph()
        out_edges = [(1, 2), (1, 4)]
        next_node = rp.infer_next_node(model, graph, out_edges, 1, 2)
        self.assertTrue(next_node == 2 or next_node == 4)

    def test_infer_node_route_not_possible(self):
        model = ModelStubAlwaysError()

        graph = gc.generate_path(5)
        out_edges = []
        self.assertRaises(RuntimeError, rp.infer_next_node, model, graph, out_edges, 0, 1)

    def test_only_one_next_dont_call_model(self):
        model = ModelStubAlwaysError()

        graph = gc.generate_path(5)
        route, valid = rp.get_route(model, graph, 0, 4)
        self.assertEqual([0, 1, 2, 3, 4], route)
        self.assertTrue(valid)

    def test_straight_path(self):
        model = ModelStubAlwaysZero()
        # 1st edge: use model
        # 2nd edge: deterministic

        graph = gc.generate_hardcoded_graph()
        route, valid = rp.get_route(model, graph, 1, 3)
        self.assertEqual([1, 2, 3], route)
        self.assertTrue(valid)

    def test_ensure_exclude_nodes_in_route(self):
        model = ModelStubAlwaysZero()

        graph = gc.generate_hardcoded_graph()
        route, valid = rp.get_route(model, graph, 1, 5)
        self.assertEqual([1, 2, 3, 6, 5], route)
        self.assertTrue(valid)


if __name__ == '__main__':
    unittest.main()
