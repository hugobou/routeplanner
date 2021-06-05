import unittest
import GraphCreator as gc
import networkx as nx


class GraphCreatorTest(unittest.TestCase):
    def test_generate_low_degree_g(self):
        G = gc.generate_low_degree_g(num_nodes=100)
        self.assertEqual(100, G.number_of_nodes())
        # Ensure no key errors
        nx.get_node_attributes(G, 'x')[0]
        nx.get_node_attributes(G, 'y')[0]

    def test_generate_path_g(self):
        G = gc.generate_path(num_nodes=100)
        self.assertEqual(100, G.number_of_nodes())
        nx.get_node_attributes(G, 'x')[0]
        nx.get_node_attributes(G, 'y')[0]

if __name__ == '__main__':
    unittest.main()
