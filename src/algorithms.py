
from typing import Set
from models.graph import Graph
import itertools
from models.vertice import Vertice


def min_domination_set(graph: Graph):
    return min_domination_set_greedy_complex(graph)

def min_domination_set_greedy_complex(graph: Graph) -> Set[Vertice]:
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


    print(f"preprocessing: {len(domination_set)}")
    # sort vertices by inverted cardinality
    #cardinality_invert_sorted_vertices = sorted([(vertice,len(graph.edges.get(vertice, list()))) for vertice in graph.vertices], key=lambda tuple: tuple[1], reverse=True)
    cardinality_invert_sorted_vertices = sorted([(vertice,len(vertice_list)) for vertice, vertice_list in graph.edges.items()], key=lambda tuple: tuple[1], reverse=True)

    # add vertices to dominating set by cardinality order until reaches the goal
    covered = set(list(domination_set))
    for vertice, cardinality in cardinality_invert_sorted_vertices:
        if vertice in covered: continue

        for connected_vertice in graph.edges[vertice]:
            covered.add(connected_vertice)

        domination_set.add(vertice)
        covered.add(vertice)

        if graph.is_domination_set(domination_set):
            break

    print(f"processing: {len(domination_set)}")


    # sort domination set vertices by cardinality
    cardinality_sorted_domination_vertices = sorted([(vertice,len(graph.edges.get(vertice, list()))) for vertice in domination_set], key=lambda tuple: tuple[1])
    # remove extra nodes
    for vertice, cardinality in cardinality_sorted_domination_vertices:
        if graph.is_domination_set(domination_set-set([vertice])):
            domination_set.remove(vertice)

    print(f"posprocessing: {len(domination_set)}")

    
    return domination_set

def min_domination_set_greedy_simple(graph: Graph):
    # sort vertices by cardinality
    cardinality_sorted_vertices = sorted([(vertice,len(vertice_list)) for vertice, vertice_list in graph.edges.items()], key=lambda tuple: tuple[1], reverse=True)

    # add vertices to dominating set until reaches the goal
    domination_set = set()
    for vertice, cardinality in cardinality_sorted_vertices:
        domination_set.add(vertice)
        if graph.is_domination_set(domination_set):
            break
    return domination_set


def min_domination_set_exaustive(graph: Graph):
    # generate all possible combinations
    all_combinations = list()
    for i in range(1, len(graph.vertices)+1):
        all_combinations.extend(itertools.combinations(graph.vertices, i))

    # try every combination from smaller to larger to check if it is domination set and return the one with the smallest length
    while all_combinations:
        current_combination = all_combinations.pop(0)
        if graph.is_domination_set(current_combination):
            break
    return set(current_combination)
