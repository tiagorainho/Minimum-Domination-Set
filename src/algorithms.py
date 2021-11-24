
from typing import List, Set
from models.graph import Graph
import itertools
from models.vertice import Vertice


def min_domination_set(graph: Graph, verbose:bool=False):
    return min_domination_set_greedy_complex(graph, verbose)

def is_domination_set(graph:Graph, vertices: List[Vertice]):
    connected_vertices = set(vertices)
    for vertice in vertices:
        vertices_list = graph.edges.get(vertice)
        if vertices_list == None: continue
        for vertice_to_connect in vertices_list:
            connected_vertices.add(vertice_to_connect)
    return len(connected_vertices) == len(graph.vertices)

def min_domination_set_greedy_complex(graph: Graph, verbose:bool=False) -> Set[Vertice]:
    domination_set = set()

    # preprocessing
    for vertice in graph.vertices:
        vertice_list = graph.edges.get(vertice)
        # add vertices with no edges to domination set
        if vertice_list == None:
            domination_set.add(vertice)
        # add vertices connected with vertices with only one edge
        elif len(vertice_list) == 1:
            domination_set.add(vertice_list[0])

    if verbose: print(f"preprocessing: {len(domination_set)}")

    # sort vertices by inverted cardinality
    cardinality_invert_sorted_vertices = sorted([(vertice,len(graph.edges.get(vertice, list()))) for vertice in graph.vertices], key=lambda tuple: tuple[1], reverse=True)
    #cardinality_invert_sorted_vertices = sorted([(vertice,len(vertice_list)) for vertice, vertice_list in graph.edges.items()], key=lambda tuple: tuple[1], reverse=True)

    # add vertices to dominating set by cardinality order until reaches the goal
    covered = set(list(domination_set))
    for vertice, cardinality in cardinality_invert_sorted_vertices:
        if vertice in covered: continue

        for connected_vertice in graph.edges[vertice]:
            covered.add(connected_vertice)

        domination_set.add(vertice)
        covered.add(vertice)

        if is_domination_set(graph, domination_set):
            break

    if verbose: print(f"processing: {len(domination_set)}")

    
    # sort domination set vertices by cardinality
    cardinality_sorted_domination_vertices = sorted([(vertice,len(graph.edges.get(vertice, list()))) for vertice in domination_set], key=lambda tuple: tuple[1])

    for vertice, cardinality in cardinality_sorted_domination_vertices:
        # remove redundant nodes
        if is_domination_set(graph, domination_set-set([vertice])):
            domination_set.remove(vertice)

    if verbose: print(f"posprocessing: {len(domination_set)}")

    return domination_set

def min_domination_set_greedy_simple(graph: Graph, verbose:bool=False):
    # sort vertices by cardinality
    cardinality_sorted_vertices = sorted([(vertice,len(vertice_list)) for vertice, vertice_list in graph.edges.items()], key=lambda tuple: tuple[1], reverse=True)

    # add vertices to dominating set until reaches the goal
    domination_set = set()
    for vertice, cardinality in cardinality_sorted_vertices:
        domination_set.add(vertice)
        if is_domination_set(graph, domination_set):
            break
    return domination_set


def min_domination_set_exaustive(graph: Graph, verbose:bool=False):
    # generate all possible combinations
    all_combinations = list()
    for i in range(1, len(graph.vertices)+1):
        all_combinations.extend(itertools.combinations(graph.vertices, i))

    # try every combination from smaller to larger to check if it is domination set and return the one with the smallest length
    while all_combinations:
        current_combination = all_combinations.pop(0)
        if is_domination_set(graph, current_combination):
            break
    return set(current_combination)
