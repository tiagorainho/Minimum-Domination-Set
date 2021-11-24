
from models.graph import Graph
import algorithms
import networkx as nx
import networkx.algorithms.dominating as dominating
import random
import time
import visualizer


number_of_vertices: int = 100
max_number_of_edges:int = 5


def convert_to_nx(graph:Graph):
    nx_graph = nx.Graph()
    for vertice, list_of_vertices in graph.edges.items():
        for vertice2 in list_of_vertices:
            nx_graph.add_edge(vertice.name, vertice2.name)
            nx_graph.add_edge(vertice2.name, vertice.name)
    return nx_graph


def convert_nx_vertice_set_to_graph_vertices(min_domination_set, graph):
    return {v for vertice in min_domination_set for v in graph.vertices if v.name == vertice}


def compare_algorithms():

    # test the custom algorithm
    random.seed(92984)
    graph = Graph(name='Custom Min Domination Set')
    graph.generate(number_of_vertices, max_number_of_edges)
    t1 = time.perf_counter()
    min_domination_set = algorithms.min_domination_set(graph)
    graph.min_domination_set = min_domination_set
    t2 = time.perf_counter()
    print(f'Custom min domination set: {len(min_domination_set)} nodes and took {t2-t1} seconds')

    # test the networkx algorithm
    random.seed(92984)
    graph2 = Graph(name='Networkx Min Domination Set')
    graph2.generate(number_of_vertices, max_number_of_edges)
    nx_graph = convert_to_nx(graph2)
    t1 = time.perf_counter()
    min_domination_set = dominating.dominating_set(nx_graph)
    t2 = time.perf_counter()
    print(f'Networkx min domination set: {len(min_domination_set)} nodes and took {t2-t1} seconds')
    graph2.min_domination_set = convert_nx_vertice_set_to_graph_vertices(min_domination_set, graph2)

    # show both the graphs
    visualizer.show([graph, graph2])


if __name__ == '__main__':
    compare_algorithms()