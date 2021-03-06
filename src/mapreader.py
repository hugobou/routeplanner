import networkx as nx
import osmnx as ox

highway_include = {'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential',
                   'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link', 'living_street',
                   'service', 'road'}
highway_exclude = {'footway', 'cycleway', 'pedestrian'}


def ReadMap(filename):

    ox.config(use_cache=True, log_console=True)

    G = ox.io.load_graphml(filename)

    remove_edges_without_highway(G)
    remove_edges_with_invalid_highway(G)
    remove_edges_without_valid_highway_list(G)
    remove_edges_without_valid_highway(G)
    simplify_highway(G)

    # Useful info:
    # https://geoffboeing.com/2020/06/whats-new-with-osmnx/
    # https://geoffboeing.com/2016/11/osmnx-python-street-networks/
    G = ox.add_edge_speeds(G)
    # add_maxspeed(G)

    # G2 = ox.project_graph(G)
    # G3 = ox.consolidate_intersections(G2, tolerance=10, rebuild_graph=True, dead_ends=True)

    # Generate connected components and select the largest:
    # https://stackoverflow.com/q/20012579
    largest_component = max(nx.weakly_connected_components(G), key=len)

    G4 = G.subgraph(largest_component)

    return G4


def remove_edges_without_valid_highway(G):
    edges_to_remove = [(s, d) for s, d, meta in G.edges.data() if
                       not isinstance(meta['highway'], list) and meta['highway'] not in highway_include]
    remove_edges(G, edges_to_remove)


def remove_edges_with_invalid_highway(G):
    edges_to_remove = [(s, d) for s, d, meta in G.edges.data() if
                       isinstance(meta['highway'], list) and any(hwy in highway_exclude for hwy in meta['highway'])]
    remove_edges(G, edges_to_remove)


def remove_edges_without_valid_highway_list(G):
    edges_to_remove = [(s, d) for s, d, meta in G.edges.data() if
                       isinstance(meta['highway'], list) and all(hwy not in highway_include for hwy in meta['highway'])]
    remove_edges(G, edges_to_remove)


def remove_edges_without_highway(G):
    edges_to_remove = [(s, d) for s, d, meta in G.edges.data() if 'highway' not in meta]
    remove_edges(G, edges_to_remove)


def remove_edges(G, edges_to_remove):
    for (s, d) in edges_to_remove:
        while G.has_edge(s, d):
            G.remove_edge(s, d)


def simplify_highway(G):
    for s, d, meta in G.edges.data():
        if isinstance(meta['highway'], list):
            first = next(filter(lambda hwy: hwy in highway_include, meta['highway']), None)
            G[s][d][0]['highway'] = first


def add_maxspeed(G):
    highway_maxspeed = {'motorway': 120, 'trunk': 80, 'primary': 80, 'secondary': 70, 'tertiary':50, 'unclassified':50, 'residential':30,
        'motorway_link':80, 'trunk_link':80, 'primary_link':80, 'secondary_link':70, 'tertiary_link':50, 'living_street':30, 'service':30, 'road':50}

    edges_without_speed = [(s, d) for s, d, meta in G.edges.data() if 'maxspeed' not in meta]
    for s, d in edges_without_speed:
        for i in range(len(G[s][d])):
            G[s][d][i]['maxspeed'] = highway_maxspeed[G[s][d][i]['highway']]

    edges_with_multiple_speed = [(s, d) for s, d, meta in G.edges.data() if isinstance(meta['maxspeed'], list)]
    for s, d in edges_with_multiple_speed:
        for i in range(len(G[s][d])):
            G[s][d][i]['maxspeed'] = min([float(speed) for speed in G[s][d][i]['maxspeed']])
