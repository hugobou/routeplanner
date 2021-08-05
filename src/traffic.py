import networkx as nx
import osmnx as ox
import utm
import csv

SERVICE_DEFAULT = 0


def utm2latlon(x, y):
    return utm.to_latlon(x, y, 30, 'T')


class TrafficMeasurement:
    def __init__(self, id, description, x, y, serv_level):
        self.id = int(id)
        self.description = description
        self.x = float(x.replace(",", "."))
        self.y = float(y.replace(",", "."))
        self.lat, self.lon = utm2latlon(self.x, self.y)
        self.serv_level = int(serv_level) if serv_level is not None and serv_level != "Error" else SERVICE_DEFAULT

    def __str__(self):
        return "%s (%f, %f): %d" % (self.description, self.x, self.y, self.serv_level)

    def isvalid(self):
        if self.id is None or self.description is None or self.x is None or self.y is None or self.serv_level is None:
            return False
        else:
            return True


def read_tm_dict(filename):
    tm_dict = {}
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            tm_dict[int(row['pm'])] = (int(row['src']), int(row['dst']))
    return tm_dict


def reset_traffic_info(graph):
    nx.set_edge_attributes(graph, SERVICE_DEFAULT, "traffic")


def update_traffic_info(graph, tm_list, tm_edge_dict):
    reset_traffic_info(graph)
    for tm in tm_list:
        try:
            edge = tm_edge_dict[tm.id]
            src = edge[0]
            dst = edge[1]
        except KeyError:
            continue

        graph.get_edge_data(src, dst, 0)['traffic'] = tm.serv_level
