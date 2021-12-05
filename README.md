# Minimum-Domination-Set


# Methods

## Graph Representation

A Graph is represented by:
- vertices: Set of Vertices
- edges: Dictionary of a Vertice as Key and a Set of Vertices as Value

The **vertices** are represented by a Set of Vertices (``Set[Vertice]``), this is optimal because we can not have the same vertice twice inside this Set and also provides us with $ O(1) $ search complexity.

The **edges** are represented by a Dictionary containing a Vertice as a key and a Set of Vertices as the value (``Dict[Vertice, Set[Vertice]]``). This structure also provides $ O(1) $ search complexity for both the values and the keys.


## Generating the graphs

We need to test the algorithms proposed by this project, to fulfill that, graphs need to be generated in order to check results.
To generate graphs we first need to initialize a Graph object
```python
graph = Graph()
```
Then we can use the ``generate()`` method which generates the graph based on some user input such as:

| Argument                           | Type      |       Function                                        |
|------------------------------------|-----------|------------------------------------------------------ |
| number_of_vertices                 | Integer   | Number of vertices inside the graph                   |
| medium_number_of_edges             | Integer   | Medium number of edges connecting each vertice        |
| width                              | Integer   | Width of the canvas where the graph is represented    |
| height                             | Integer   | Height of the canvas where the graph is represented   |
| minimum_distance_between_vertices  | Integer   | Mininum distance between each vertice                 |
| connect_with_closest               | Boolean   | Connect each vertice with the *n* closest vertices  |
| verbose                            | Boolean   | Prints information about the operation                |


The graph is constructed in **two main steps** by the ``generate()`` method:
1) First we need to generate the vertices
2) Then we can generate the edges

### Vertices Generation

The vertice generation is of complexity $ O(n) $ because iterates though the number of vertices to generate
```python
for i in range(number_of_vertices):
    new_vertice = Vertice(name = str(i))
    vertices.add(new_vertice)
```
There is small differentes in this function based on if it is needed to generate also the ``width``, ``height`` and also based on ``minimum_distance_between_vertices``. However these are negligable, for example, when both the ``width`` and ``height`` are different than ``None``, then
```python
new_vertice = Vertice(
    name = str(len(vertices)),
    x = random.randint(0, width),
    y = random.randint(0, height)
)
```

### Edges Generation

The edges are more complex to generate than the vertices based on the argument ``connect_with_closest`` because if ``True``, it means we need to look to the closest vertices from all the others vertices to discover which are closer. This is very helpful when debuging the complex algorithms because even for graphs with just 100 vertices it is almost impossible to figure out what vertices the edges are connecting. The implementation of the generation is done by the following pseudo-code

```python
for vertice in vertices:
    if connect_with_closest:
        closest_vertices = get_closest_vertices(vertice = vertice, n = remaining_number_of_edges)
        for vertice_to_connect in closest_vertices:
            add_edge(vertice, vertice_to_connect)
    else:
        vertices_to_connect = random.sample(self.vertices, remaining_number_of_edges)
        for vertice_to_connect in vertices_to_connect:
            add_edge(vertice, vertice_to_connect)
```

The ``get_closest_vertices()`` method is implemented with a *priority queue* in order to achieve aproximatly $ O(log(n)) $ complexity instead of the python ``sorted()`` which runs in $ O(n log(n)) $. When generating large graphs, this difference is very noticiable because this function runs for every vertice.


## Auxiliary Features

Some features were implemented in order to improve graph visualization (``visualizer.py``) and results (``results.py``).

### Visualization

This class is used to provide a visualization method named ``show()`` which takes in a Graph or a list of graphs and plots them in a new window. The vertices are represented by a white circle with the name of the vertice but for easier distinction, the dominating set vertices are represented at a different color.

### Results Extraction

In order to improve results extraction and to facilitate the comparison between multiple algorithms, 2 defined functions compare both the Custom and the Networkx implementation of the mininum dominating set:
1) ``show_both_algorithms()``: given the inputs (*number of vertices*, *medium number of edges* and *seed*), returns the plots of both the implementations.
2) ``compare_both_algorithms_with_table()``: given a list of inputs (list of the input of the previous function), returns a table with statistics.

# Results and discussion



## Formal Analysis

For declarative reasons, the operation considered in these analysis will be the search of a vertice.

### Exhaustive Search

In order to compute this problem in an exhaustive way, we need to run all possible combinations, check if that specific combination is a dominating set and then check if the new dominating set is smaller than the last one.
The pseudo-code would be
```python
for current_combination in all_combinations:
    if is_domination_set(graph, current_combination) and len(current_combination) < len(min_domination_set):
        min_domination_set = current_combination
```

Since we need to check every combination, the complexity of this algorithm will be
$$ O(2^{n}) $$
However, if we count the ``is_domination_set()`` method, because it is of complexity $ O(n*medium\_number\_of\_edges) $, we end up with a larger complexity $ O(2^{n}\times{n\times{medium\_number\_of\_edges}}) $ but the smaller order terms are not taken into account, for that reason, from now on these will not appear again.

### Greedy Heuristics

The greedy approache consists in 3 main steps:
1) starting the min dominating set with the vertices that contain 0 edges and if only contains 1 edge, then add the vertice which is connected
2) sort vertices from the number of edges it contains and start adding them to the dominating set until finds a dominating set
3) remove excess vertices from the dominating set by sorting them in decreasing order of number of edges and trying to check if the dominating set remains a dominating set without that vertice


The preprocessing complexity is $ O(n) $ and can be seen as
```python
for vertice in graph.vertices:
    vertice_list = graph.edges.get(vertice, list())
    if len(vertice_list) == 0:
        domination_set.add(vertice)
    elif len(vertice_list) == 1:
        domination_set.add(vertice_list[0])
```

We can find the dominating set by the following block of pseudo-code with $ O(n) $ complexity
```python
covered = set()
for vertice in cardinality_invert_sorted_vertices:
    if vertice in covered: continue

    covered.update(graph.edges[vertice] + vertice)

    domination_set.add(vertice)

    if is_domination_set(graph, domination_set):
        break
```
And finally remove redundant nodes with also $ O(n) $ complexity
```python
for vertice in cardinality_sorted_domination_vertices:
    domination_set.remove(vertice)
    if not is_domination_set(graph, domination_set):
        domination_set.add(vertice)
```

Therefore, the final complexity of this algorithm is $ O(3n) $ which converts to
$$ O(n) $$


## Experimental Results



### Exhaustive Search


### Greedy Heuristics


# Conclusion

In conclusion 































| Vertices | Edges |       Custom                           |      Networkx                             |
|----------|-------|----------------------------------------|-------------------------------------------|
|   125    |   5   |    40 vertices<br>3.48 ms + -99.7%     |    46 vertices<br>0.18 ms + -100.0%       |
|   250    |   5   |    77 vertices     |    94 vertices    |
|          |       | 14.05 ms + 303.6%  |   0.3 ms + 60.4%  |
|   500    |   5   |    148 vertices    |    167 vertices   |
|          |       | 75.65 ms + 438.4%  |  0.52 ms + 76.5%  |
|   1000   |   5   |    298 vertices    |    358 vertices   |
|          |       | 219.91 ms + 190.7% |  1.04 ms + 99.2%  |
|   2000   |   5   |    610 vertices    |    722 vertices   |
|          |       | 992.13 ms + 351.2% |  2.01 ms + 93.8%  |