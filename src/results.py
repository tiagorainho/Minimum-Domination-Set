
from typing import List, Tuple
from models.graph import Graph
import algorithms
import networkx.algorithms.dominating as dominating
import random
import time
import visualizer
from prettytable import PrettyTable
import utils


number_of_vertices:int = 200
max_number_of_edges:int = 5
seed:int = 100


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
    nx_graph = utils.convert_to_nx(graph2)
    t1 = time.perf_counter()
    min_domination_set = dominating.dominating_set(nx_graph)
    t2 = time.perf_counter()
    graph2.min_domination_set = utils.convert_nx_vertice_set_to_graph_vertices(min_domination_set, graph2)
    print(f'Networkx min domination set: {len(min_domination_set)} nodes and took {t2-t1} seconds')

    # show both the graphs
    visualizer.show([graph, graph2])


def compare_table(inputs:List[Tuple[int, int, int]]):
    table = PrettyTable(["Vertices", "Edges", "Custom", "Networkx"])
    last_times = [1, 1]
    for i, (number_of_vertices, max_number_of_edges, seed) in enumerate(inputs):

        print(f'{round(i/len(inputs)*100, 2)}\t%')

        row1 = [number_of_vertices, max_number_of_edges]
        row2 = ['', '']

        random.seed(seed)
        graph = Graph(name='Custom Min Domination Set')
        graph.generate(number_of_vertices, max_number_of_edges, min_distance_between_vertices=0)
        t1 = time.perf_counter()
        min_domination_set = algorithms.min_domination_set(graph)
        t2 = time.perf_counter()

        row1.append(f'{len(min_domination_set)} vertices')
        row2.append(f'{round((t2-t1)*1000, 2)} ms + {round(((t2-t1)-last_times[0])/(last_times[0])*100,1)}%')
        last_times[0] = t2-t1

        random.seed(seed)
        graph2 = Graph(name='Networkx Min Domination Set')
        graph2.generate(number_of_vertices, max_number_of_edges)
        nx_graph = utils.convert_to_nx(graph2)
        t1 = time.perf_counter()
        min_domination_set = dominating.dominating_set(nx_graph)
        t2 = time.perf_counter()

        row1.append(f'{len(min_domination_set)} vertices')
        row2.append(f'{round((t2-t1)*1000, 2)} ms + {round(((t2-t1)-last_times[1])/(last_times[1])*100,1)}%')
        last_times[1] = t2-t1


        table.add_rows([row1, row2])


    print(table)
    
    

if __name__ == '__main__':
    # show_both_algorithms(number_of_vertices, max_number_of_edges, seed)
    compare_table([
        (125, 5, 100),
        (250, 5, 100),
        (500, 5, 100),
        (1000, 5, 100),
        (2000, 5, 100)
    ])
    