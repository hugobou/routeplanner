import unittest

import networkx as nx
import routeformatter as rf
import graphcreator as gc


class RouteFormatterTest(unittest.TestCase):
    def test_one_name_next(self):
        formatter = rf.RouteFormatter()

        graph = gc.generate_hardcoded_graph()

        result = formatter.format(graph, [1, 2])
        self.assertEqual(1, len(result))
        self.assertEqual(graph[1][2][0]["name"], result[0]["name"])
        self.assertEqual(2, result[0]["next"])

    def test_two_name_next(self):
        formatter = rf.RouteFormatter()

        graph = gc.generate_hardcoded_graph()

        result = formatter.format(graph, [1, 2, 3])
        self.assertEqual(2, len(result))

        self.assertEqual(graph[1][2][0]["name"], result[0]["name"])
        self.assertEqual(2, result[0]["next"])

        self.assertEqual(graph[2][3][0]["name"], result[1]["name"])
        self.assertEqual(3, result[1]["next"])

    def test_coordinates(self):
        formatter = rf.RouteFormatter()

        graph = gc.generate_hardcoded_graph()

        result = formatter.format(graph, [1, 2, 3])

        x = nx.get_node_attributes(graph, 'x')
        y = nx.get_node_attributes(graph, 'y')

        self.assertEqual(x[2], result[0]["lon"])
        self.assertEqual(x[3], result[1]["lon"])

        self.assertEqual(y[2], result[0]["lat"])
        self.assertEqual(y[3], result[1]["lat"])

if __name__ == '__main__':
    unittest.main()
