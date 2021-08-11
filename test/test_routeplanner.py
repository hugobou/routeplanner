import unittest
import graphcreator as gc
import routeplanner as rp


class FeatureEncoderStub:
    def encode_features(self, graph, out_edges, node_cur, node_dst):
        return None


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


class ModelStubPresetList:
    def __init__(self, values):
        self._values = values
        self._index = 0

    def predict(self, ignored):
        value = self._values[self._index]
        self._index += 1
        return value

# TODO: error handling. src/dst Nodes not in graph.


class RoutePlannerTest(unittest.TestCase):
    def test_infer_node_happy_flow(self):
        model = ModelStubAlwaysZero()

        graph = gc.generate_path(5)
        out_edges = list(graph.out_edges(0))

        sut = rp.RoutePlanner(model, FeatureEncoderStub())
        next_node = sut.infer_next_node(graph, out_edges, 0, 1)
        self.assertEqual(1, next_node)

    def test_infer_node_invalid_prediction_random_choice(self):
        model = ModelStubAlwaysConstant(5)

        graph = gc.generate_hardcoded_graph()
        out_edges = [(1, 2), (1, 4)]

        sut = rp.RoutePlanner(model, FeatureEncoderStub())
        next_node = sut.infer_next_node(graph, out_edges, 1, 2)
        self.assertTrue(next_node == 2 or next_node == 4)

    def test_infer_node_route_not_possible(self):
        model = ModelStubAlwaysError()

        graph = gc.generate_path(5)
        out_edges = []

        sut = rp.RoutePlanner(model, FeatureEncoderStub())
        self.assertRaises(RuntimeError, sut.infer_next_node, graph, out_edges, 0, 1)

    def test_only_one_next_dont_call_model(self):
        model = ModelStubAlwaysError()

        graph = gc.generate_path(5)

        sut = rp.RoutePlanner(model, FeatureEncoderStub())
        route, valid = sut.get_route(graph, 0, 4)
        self.assertEqual([0, 1, 2, 3, 4], route)
        self.assertTrue(valid)

    def test_straight_path(self):
        model = ModelStubAlwaysZero()
        # 1st edge: use model
        # 2nd edge: deterministic

        graph = gc.generate_hardcoded_graph()

        sut = rp.RoutePlanner(model, FeatureEncoderStub())
        route, valid = sut.get_route(graph, 1, 3)
        self.assertEqual([1, 2, 3], route)
        self.assertTrue(valid)

    def test_ensure_exclude_nodes_in_route(self):
        model = ModelStubAlwaysZero()

        graph = gc.generate_hardcoded_graph()

        sut = rp.RoutePlanner(model, FeatureEncoderStub())
        route, valid = sut.get_route(graph, 1, 5)
        self.assertEqual([1, 2, 3, 6, 5], route)
        self.assertTrue(valid)

    def test_walk_back(self):
        model = ModelStubPresetList([0, 1, 1])

        graph = gc.generate_hardcoded_graph()

        sut = rp.RoutePlanner(model, FeatureEncoderStub())
        route, valid = sut.get_route(graph, 1, 9)
        self.assertEqual([1, 2, 3, 6, 9], route)
        self.assertTrue(valid)


if __name__ == '__main__':
    unittest.main()
