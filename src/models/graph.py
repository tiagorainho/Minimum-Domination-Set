
from typing import Dict, List, Set
import random
from models.vertice import Vertice
import time
import heapq
from copy import deepcopy


class Graph:
    vertices: Set[Vertice]
    edges: Dict[Vertice, Set[Vertice]]
    width: int
    height: int
    name: str

    def clone(self):
        return deepcopy(self)

    def __init__(self, vertices:List[Vertice]=None, edges:Dict[Vertice, Vertice]=None, name:str='graph'):
        self.name = name
        self.vertices = vertices if vertices != None else set()
        self.edges = edges if edges != None else dict()
    
    @property
    def number_of_edges(self):
        return sum(len(vertices) for vertices in self.edges.values())

    
    def add_edge(self, vertice1:Vertice, vertice2:Vertice):
        edges = self.edges.get(vertice1)
        if edges == None: self.edges[vertice1] = set([vertice2])
        else: edges.add(vertice2)

        edges = self.edges.get(vertice2)
        if edges == None: self.edges[vertice2] = set([vertice1])
        else: edges.add(vertice1)

    def generate(self, number_of_vertices:int, medium_number_of_edges:int,  width:int=None, height:int=None, min_distance_between_vertices:int=None, connect_with_closest:bool=False, verbose:bool=False):

        assert (0 if width == None else 1) == (0 if height == None else 1)

        self.width = width
        self.height = height

        # generate vertices
        t1 = time.perf_counter()
        """
        if width == None and height == None:
            for i in range(number_of_vertices):
                self.vertices.add(Vertice(str(i)))
        else:
            while(len(self.vertices) < number_of_vertices):
                remaining_number_of_vertices = number_of_vertices - len(self.vertices)
                vertice_x_coords = set(range(width))
                vertice_y_coords = set(range(height))
                x_values = random.sample(vertice_x_coords, remaining_number_of_vertices)
                y_values = random.sample(vertice_y_coords, remaining_number_of_vertices)

                for 

                new_vertice = Vertice(str(len(self.vertices)), random.randint(0, width), random.randint(0, height))
                # recalculate if there is already this vertice
                if new_vertice not in vertices_coords:
                    self.vertices.add(new_vertice)
                    vertices_coords.add((new_vertice.x, new_vertice.y))
                #if all([vertice.distance(new_vertice) >= min_distance_between_vertices for vertice in self.vertices]):
                #    self.vertices.append(new_vertice)
        """
        if width == None and height == None:
            for i in range(number_of_vertices):
                self.vertices.add(Vertice(str(i)))
        else:
            while(len(self.vertices) < number_of_vertices):
                new_vertice = Vertice(str(len(self.vertices)), random.randint(0, width), random.randint(0, height))
                # recalculate if there is already this vertice
                #if all([vertice.distance(new_vertice) >= min_distance_between_vertices for vertice in self.vertices]):
                self.vertices.add(new_vertice)
        
        t2 = time.perf_counter()

        # generate edges
        for vertice in self.vertices:
            remaining_number_of_edges = random.randint(0, medium_number_of_edges)
            if remaining_number_of_edges == 0: continue
            if connect_with_closest:
                closest_vertices = heapq.nsmallest(remaining_number_of_edges, [(v, vertice.distance(v)) for v in self.vertices if vertice != v], key=lambda t: t[1])
                for vertice_to_connect, _ in closest_vertices:
                    self.add_edge(vertice, vertice_to_connect)
            else:
                vertices_to_connect = random.sample(self.vertices, remaining_number_of_edges)
                for vertice_to_connect in vertices_to_connect:
                    self.add_edge(vertice, vertice_to_connect)
        if verbose:
            print(f"generation of: VERTICES -> {t2-t1} seconds, EDGES -> {time.perf_counter()-t2} seconds")

    def __repr__(self):
        return '\n'.join([str(vertice) for vertice in self.vertices])
