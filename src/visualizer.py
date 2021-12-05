
from tkinter import *
from typing import List
from models.graph import Graph
from models.vertice import Vertice
import random
import algorithms


canvas_width:int = 1000
canvas_height:int = 1000
margin:int = 20
window: Canvas
number_of_vertices: int = 100
max_number_of_edges:int = 5
min_distance_between_vertices: int = 50#(canvas_height*canvas_width/(number_of_vertices*500)) #math.log(number_of_vertices, 2) * 100
NORMAL_VERTICE_COLOR:str = "#ffffff"
DOMINATION_SET_VERTICE_COLOR:str = "#3aead3"
EDGES_COLOR: str = "#000000"
CONNECT_WITH_CLOSEST:bool = False



def add_point(window:Canvas, graph:Graph, x, y, r, **kwargs):
    window.create_oval(x-r, (graph.height-y)-r, x+r, (graph.height-y)+r, **kwargs)

def add_line(window:Canvas, graph:Graph, vertice1:Vertice, vertice2:Vertice):
    window.create_line(vertice1.x, (graph.height-vertice1.y), vertice2.x, (graph.height-vertice2.y), fill=EDGES_COLOR)

def add_text(window:Canvas, graph:Graph, x:int, y:int, text:str):
    window.create_text(x, (graph.height-y), text=text)

def draw_graph(window:Canvas, graph:Graph, **kwargs):
    # add edges
    for vertice, vertices_list in graph.edges.items():
        for vertice2 in vertices_list:
            add_line(window, graph, vertice, vertice2)

    # add vertices
    for vertice in graph.vertices:
        vertice_color = NORMAL_VERTICE_COLOR
        if graph.__dict__.get('min_domination_set') != None:
            vertice_color = DOMINATION_SET_VERTICE_COLOR if vertice in graph.min_domination_set else NORMAL_VERTICE_COLOR

        add_point(window, graph, vertice.x, vertice.y, 10, fill=vertice_color)
        add_text(window, graph, vertice.x, vertice.y, vertice.name)


def show(graph_list:List[Graph] or Graph):
    if isinstance(graph_list, Graph):
        graph_list = [graph_list]
    for graph in graph_list:
        master = Tk()
        master.resizable(height = None, width = None)
        master.title(graph.name)
        window = Canvas(master,
                width=graph.width,
                height=graph.height,
                bg="white")
        window.pack(expand=YES, fill=BOTH)
        draw_graph(window, graph)
    mainloop()


if __name__ == '__main__':
    random.seed(92984)
    graph = Graph()
    graph.generate(number_of_vertices, max_number_of_edges, canvas_width, canvas_height, min_distance_between_vertices, CONNECT_WITH_CLOSEST)
    graph.min_domination_set = algorithms.min_domination_set(graph, True)
    show(graph)

