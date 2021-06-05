import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import GraphCreator as gc
import RoutePlanner as rp



class RoutePlannerTest(unittest.TestCase):
    def test_infer_node(self):
        class ModelStub:
            def predict(self, ignored):
                return 0
        model = ModelStub()

        path = gc.generate_path(5)
        next = rp.infer_next_node(model, path, 1, 0)
        self.assertEqual(1, next)

    def test_plan_route(self):
        class ModelStub:
            def predict(self, ignored):
                return 0
        model = ModelStub()

        path = gc.generate_path(5)
        route = rp.get_route(model, path, 0, 4)
        self.assertEqual([0, 1, 2, 3, 4], route)

if __name__ == '__main__':
    unittest.main()
