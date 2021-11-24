

from typing import Set
from models.graph import Graph
import networkx as nx

from models.vertice import Vertice

def convert_to_nx(graph:Graph):
    nx_graph = nx.Graph()
    for vertice in graph.vertices:
        vertice_list = graph.edges.get(vertice)
        if vertice_list == None:
            # add edge from and to the same vertice
            nx_graph.add_edge(vertice.name, vertice.name)
        else:
            # add vertice from vertice1 to vertice2
            for vertice2 in vertice_list:
                nx_graph.add_edge(vertice.name, vertice2.name)
                nx_graph.add_edge(vertice2.name, vertice.name)
    return nx_graph

def convert_nx_vertice_set_to_graph_vertices(min_domination_set:Set[any], graph:Graph) -> Set[Vertice]:
    return {v for vertice in min_domination_set for v in graph.vertices if v.name == vertice}