
from typing import List, Set
from models.graph import Graph
import itertools
from models.vertice import Vertice

def is_domination_set(graph:Graph, vertices: List[Vertice]):
    if len(vertices) < (len(graph.vertices) - len(graph.edges)):
        return False

    connected_vertices = set(vertices)
    for vertice in vertices:
        vertices_list = graph.edges.get(vertice)
        if vertices_list == None: continue
        connected_vertices.update(vertices_list)
        if len(connected_vertices) == len(graph.vertices):
            return True
    return len(connected_vertices) == len(graph.vertices)
    

def min_domination_set(graph: Graph, verbose:bool=False):
    return min_domination_set_greedy_complex(graph, verbose=verbose)


def min_domination_set_greedy_complex(graph: Graph, pos_processing:bool = True, verbose:bool=False) -> Set[Vertice]:
    domination_set = set()

    count = 0

    # preprocessing
    for vertice in graph.vertices:
        count += 1
        vertice_list = graph.edges.get(vertice)
        # add vertices with no edges to domination set
        if vertice_list == None:
            domination_set.add(vertice)
        # add vertices connected with vertices with only one edge
        elif len(vertice_list) == 1:
            count += 1
            domination_set.add(list(vertice_list)[0])

    if verbose: print(f"preprocessing: {len(domination_set)}")

    # sort vertices by inverted cardinality
    cardinality_invert_sorted_vertices = sorted([(vertice,len(graph.edges.get(vertice, list()))) for vertice in graph.vertices], key=lambda tuple: tuple[1], reverse=True)
    #cardinality_invert_sorted_vertices = sorted([(vertice,len(vertice_list)) for vertice, vertice_list in graph.edges.items()], key=lambda tuple: tuple[1], reverse=True)
    import math
    count += int(len(graph.vertices)*math.log2(len(graph.vertices)))

    # add vertices to dominating set by cardinality order until reaches the goal
    covered = domination_set.copy()
    found = False
    for vertice, _ in cardinality_invert_sorted_vertices:
        count += 1
        if vertice in covered: continue

        # add connected vertices and vertice to covered
        covered.update(graph.edges[vertice])
        covered.add(vertice)

        domination_set.add(vertice)

        if is_domination_set(graph, domination_set):
            found = True
            break
    
    if not found:
        return None

    if verbose: print(f"processing: {len(domination_set)}")
    
    if pos_processing:
        # sort domination set vertices by cardinality
        cardinality_sorted_domination_vertices = sorted([(vertice,len(graph.edges.get(vertice, list()))) for vertice in domination_set], key=lambda tuple: tuple[1])
        count += int(len(domination_set)*math.log2(len(domination_set)))

        for vertice, _ in cardinality_sorted_domination_vertices:
            
            # remove redundant nodes
            domination_set.remove(vertice)
            if not is_domination_set(graph, domination_set):
                domination_set.add(vertice)

        count += len(cardinality_sorted_domination_vertices)
        print(len(cardinality_sorted_domination_vertices))
        
        if verbose: print(f"posprocessing: {len(domination_set)}")
    print(f'contagem: {count}')
    return domination_set


def min_domination_set_greedy_simple(graph: Graph, verbose:bool=False):
    # sort vertices by cardinality
    cardinality_sorted_vertices = sorted([(vertice,len(vertice_list)) for vertice, vertice_list in graph.edges.items()], key=lambda tuple: tuple[1], reverse=True)

    # add vertices to dominating set until reaches the goal
    domination_set = set()
    for vertice, _ in cardinality_sorted_vertices:
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
        if is_domination_set(graph, current_combination) :
            break
    return set(current_combination)

def min_domination_set_exaustive_long(graph: Graph, verbose:bool=False):
    # generate all possible combinations
    all_combinations = [combination for i in range(1, len(graph.vertices)+1) for combination in itertools.combinations(graph.vertices, i)]

    # try every combination from smaller to larger to check if it is domination set and return the one with the smallest length
    min_domination_set = None
    print(len(all_combinations))
    for current_combination in all_combinations:
        if is_domination_set(graph, current_combination) and (min_domination_set == None or len(current_combination) < len(min_domination_set)):
            min_domination_set = current_combination
    return set(min_domination_set)
