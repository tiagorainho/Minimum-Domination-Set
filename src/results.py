
from typing import List, Set, Tuple
from models.graph import Graph
import algorithms
import networkx as nx
import networkx.algorithms.dominating as dominating
import random
import time
from models.vertice import Vertice
import visualizer
from prettytable import PrettyTable


number_of_vertices:int = 200
max_number_of_edges:int = 5
seed:int = 100


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


def show_both_algorithms(number_of_vertices:int, max_number_of_edges:int, seed:int):

    # test the custom algorithm
    random.seed(seed)
    graph = Graph(name='Custom Min Domination Set')
    graph.generate(number_of_vertices, max_number_of_edges)
    t1 = time.perf_counter()
    min_domination_set = algorithms.min_domination_set(graph)
    graph.min_domination_set = min_domination_set
    t2 = time.perf_counter()
    print(f'Custom min domination set: {len(min_domination_set)} nodes and took {t2-t1} seconds')

    # test the networkx algorithm
    random.seed(seed)
    graph2 = Graph(name='Networkx Min Domination Set')
    graph2.generate(number_of_vertices, max_number_of_edges)
    nx_graph = convert_to_nx(graph2)
    t1 = time.perf_counter()
    min_domination_set = dominating.dominating_set(nx_graph)
    t2 = time.perf_counter()
    graph2.min_domination_set = convert_nx_vertice_set_to_graph_vertices(min_domination_set, graph2)
    print(f'Networkx min domination set: {len(min_domination_set)} nodes and took {t2-t1} seconds')

    # show both the graphs
    visualizer.show([graph, graph2])


def get_result():
    pass

def compare_table(inputs:List[Tuple[int, int, int]]):
    table = PrettyTable(["Vertices", "Edges", "Custom", "Networkx"])
    for i, (number_of_vertices, max_number_of_edges, seed) in enumerate(inputs):

        print(f'{round(i/len(inputs)*100, 2)}\t%')

        row1 = [number_of_vertices, max_number_of_edges]
        row2 = ['', '']

        random.seed(seed)
        graph = Graph(name='Custom Min Domination Set')
        graph.generate(number_of_vertices, max_number_of_edges)
        t1 = time.perf_counter()
        min_domination_set = algorithms.min_domination_set(graph)
        t2 = time.perf_counter()

        row1.append(f'{len(min_domination_set)} vertices')
        row2.append(f'{round((t2-t1)*1000, 2)} ms')

        random.seed(seed)
        graph2 = Graph(name='Networkx Min Domination Set')
        graph2.generate(number_of_vertices, max_number_of_edges)
        nx_graph = convert_to_nx(graph2)
        t1 = time.perf_counter()
        min_domination_set = dominating.dominating_set(nx_graph)
        t2 = time.perf_counter()

        row1.append(f'{len(min_domination_set)} vertices')
        row2.append(f'{round((t2-t1)*1000, 2)} ms')


        table.add_rows([row1, row2])


    print(table)
    
    

if __name__ == '__main__':
    # show_both_algorithms(number_of_vertices, max_number_of_edges, seed)
    compare_table([
        (100, 5, 100),
        #(150, 5, 100),
        (200, 5, 100),
        #(250, 5, 100),
        (300, 5, 100),
        #(350, 5, 100),
        (400, 5, 100),
        #(450, 5, 100),
        (500, 5, 100),
        #(550, 5, 100),
        (600, 5, 100)
    ])


