
from typing import Dict, List
import random
from models.vertice import Vertice


class Graph:
    vertices: List[Vertice]
    edges: Dict[Vertice, List[Vertice]]
    width: int
    height: int
    name: str

    def __init__(self, vertices:List[Vertice]=None, edges:Dict[Vertice, Vertice]=None, name:str='graph'):
        self.name = name
        self.vertices = vertices if vertices != None else list()
        self.edges = edges if edges != None else dict()
    
    def add_edge(self, vertice1:Vertice, vertice2:Vertice):
        edges = self.edges.get(vertice1)
        if edges == None: self.edges[vertice1] = [vertice2]
        else: edges.append(vertice2)

        edges = self.edges.get(vertice2)
        if edges == None: self.edges[vertice2] = [vertice1]
        else: edges.append(vertice1)

    def generate(self, number_of_vertices:int, max_edges:int,  width:int=1000, height:int=1000, min_distance_between_vertices:int=5):
        self.width = width
        self.height = height

        # generate vertices
        while(len(self.vertices) <= number_of_vertices):
            new_vertice = Vertice(str(len(self.vertices)), random.randint(0, width), random.randint(0, height))
            # recalculate if there is already this vertice
            if all([vertice.distance(new_vertice) >= min_distance_between_vertices for vertice in self.vertices]):
                self.vertices.append(new_vertice)

        # generate edges
        for vertice in self.vertices:
            remaining_number_of_edges = random.randint(0, max_edges - len(self.edges.get(vertice, list())))
            closest_vertices = sorted([(v, vertice.distance(v)) for v in self.vertices if vertice != v], key=lambda tuple: tuple[1])
            i = 0
            while remaining_number_of_edges > 0:
                vertice_to_connect = closest_vertices[i][0]
                edges = self.edges.get(vertice_to_connect, list())
                if len(edges) < max_edges:
                    self.add_edge(vertice, vertice_to_connect)
                    remaining_number_of_edges -= 1
                i += 1

    def __repr__(self):
        return '\n'.join([str(vertice) for vertice in self.vertices])
