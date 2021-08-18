import networkx as nx

class RouteFormatter:
    def format(self, graph, route):
        formatted = []
        x = nx.get_node_attributes(graph, 'x')
        y = nx.get_node_attributes(graph, 'y')
        for pair in zip(route[0:-1], route[1:]):
            elem = {}
            elem['next'] = pair[1]
            elem['name'] = "" if "name" not in graph[pair[0]][pair[1]][0] else graph[pair[0]][pair[1]][0]["name"]
            elem['x'] = x[pair[1]]
            elem['y'] = y[pair[1]]
            formatted.append(elem)
        return formatted