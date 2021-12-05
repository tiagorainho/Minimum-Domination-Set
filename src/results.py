
from typing import List, Tuple
from models.graph import Graph
import algorithms
import networkx.algorithms.dominating as dominating
from networkx.algorithms.approximation.dominating_set import min_weighted_dominating_set
import random
import time
import visualizer
from prettytable import PrettyTable
import utils
import networkx as nx


number_of_vertices:int = 100
max_number_of_edges:int = 5
seed:int = 100

WIDTH:int = 1000
HEIGHT:int = 1000
MIN_DISTANCE_BETWEEN_VERTICES:int = 2


def show_both_algorithms(number_of_vertices:int, max_number_of_edges:int, seed:int):

    # create the custom algorithm
    random.seed(seed)
    graph = Graph(name='Custom Min Domination Set')
    graph.generate(number_of_vertices, max_number_of_edges, WIDTH, HEIGHT, MIN_DISTANCE_BETWEEN_VERTICES, True)

    # test the custom algorithm
    t1 = time.perf_counter()
    min_domination_set = algorithms.min_domination_set(graph)
    t2 = time.perf_counter()
    graph.min_domination_set = min_domination_set
    print(f'Custom min domination set: {len(min_domination_set)} nodes and took {t2-t1} seconds')

    # create the networkx algorithm
    random.seed(seed)
    graph2 = graph.clone()
    graph2.name = 'Networkx Min Domination Set'
    nx_graph: nx.Graph = utils.convert_to_nx(graph2)

    # test the networkx algorithm
    t1 = time.perf_counter()
    min_domination_set = dominating.dominating_set(nx_graph) # min_weighted_dominating_set(nx_graph)
    t2 = time.perf_counter()
    graph2.min_domination_set = utils.convert_nx_vertice_set_to_graph_vertices(min_domination_set, graph2)
    print(f'Networkx min domination set: {len(min_domination_set)} nodes and took {t2-t1} seconds')

    # show both the graphs
    visualizer.show([graph, graph2])


def compare_both_algorithms_with_table(inputs:List[Tuple[int, int, int]]):
    table = PrettyTable(["Vertices", "Edges", "Greedy", "Networkx"])
    last_times = [1, 1]
    last_edges = 1
    last_vertices = 1
    get_percentage_increase = lambda new, last: (new-last)/last*100
    for i, (number_of_vertices, max_number_of_edges, seed) in enumerate(inputs):
        print(f'{round(i/len(inputs)*100, 2)}\t%')

        # create the custom algorithm
        random.seed(seed)
        graph = Graph(name='Custom Min Domination Set')
        graph.generate(number_of_vertices, max_number_of_edges, min_distance_between_vertices=0, connect_with_closest=False, verbose=False)

        # test the custom algorithm
        t1 = time.perf_counter()
        min_domination_set = algorithms.min_domination_set(graph)
        t2 = time.perf_counter()

        # save retrieved information about the custom algorithm
        number_of_edges = graph.number_of_edges
        row1 = [
            f'{len(graph.vertices)} + {round(get_percentage_increase(len(graph.vertices), last_vertices),1)}%',
            f'{number_of_edges} + {round(get_percentage_increase(number_of_edges, last_edges),1)}%'
        ]
        row2 = ['', '']

        row1.append(f'{len(min_domination_set)} vertices')
        row2.append(f'{round((t2-t1)*1000, 2)} ms + {round(get_percentage_increase((t2-t1), last_times[0]),1)}%')
        
        last_times[0] = t2-t1
        last_edges = number_of_edges
        last_vertices = len(graph.vertices)

        
        # create the networkx graph
        random.seed(seed)
        graph2 = graph.clone()
        graph2.name = 'Networkx Min Domination Set'
        nx_graph:nx.Graph = utils.convert_to_nx(graph2)

        # test the networkx dominating set algorithm
        t1 = time.perf_counter()
        min_domination_set = dominating.dominating_set(nx_graph) # min_weighted_dominating_set(nx_graph)
        t2 = time.perf_counter()

        # save retrieved information about the networkx algorithm
        row1.append(f'{len(min_domination_set)} vertices')
        row2.append(f'{round((t2-t1)*1000, 2)} ms + {round(((t2-t1)-last_times[1])/(last_times[1])*100,1)}%')
        last_times[1] = t2-t1

        table.add_rows([row1, row2])

    print(table)
    
    

if __name__ == '__main__':
    # show_both_algorithms(number_of_vertices, max_number_of_edges, seed)
    # exit(0)
    compare_both_algorithms_with_table([
        # (number_of_vertices, max_number_of_edges, seed),
        # (4, 2, 100),
        # (8, 2, 100),
        # (12, 2,100),
        # (16, 2, 100),
        # (20, 2, 100),
        # (22, 2, 100),

        (125, 20, 100),
        (250, 20, 100),
        (500, 20, 100),
        (1000, 20, 100),
        (2000, 20, 100),
        (4000, 20, 100),
        (8000, 20, 100)
    ])