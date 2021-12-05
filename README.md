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

During the whole formal and empirical analysis the **basic operation** considered in these analysis will be the **retrieval of a vertice**.

## Formal Analysis

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

We can find the dominating set by ordering the vertices with $ O(n log(n)) $ and following the block of pseudo-code with $ O(n) $ complexity resulting in $ O(2n log(n)) $ which simplifies to
$$ O(n log(n)) $$
```python
covered = set()
for vertice in cardinality_invert_sorted_vertices:
    if vertice in covered: continue

    covered.update(graph.edges[vertice] + vertice)

    domination_set.add(vertice)

    if is_domination_set(graph, domination_set):
        break
```
And finally remove redundant nodes by ordering the resulting dominating set with $ O(dominating\_set\times{log(dominating\_set)}) $ complexity and $ O(dominating\_set) $ complexity to remove the vertices
which simplifies to
$$ O(dominating\_set\times{log(dominating\_set)}) $$
```python
for vertice in cardinality_sorted_domination_vertices:
    domination_set.remove(vertice)
    if not is_domination_set(graph, domination_set):
        domination_set.add(vertice)
```

Therefore, the sum of each component complexity of this algorithm is $ O(n + n\times{log(n)} + dominating\_set\times{log(dominating\_set)}) $ which simplifies to
$$ O(n\times{log(n)}) $$


## Experimental Results

All results are calculated using ``seed = 100``.

### Exhaustive Search

The exhaustive algorithm does not allow us to test the algorithm much further than the number of vertices being more than 22. This is explained by the formal analysis of the exhaustive search.
The table with the inputs and outputs can be seen bellow

|   Vertices |    Edges   |      Exhaustive      |       Greedy      |     Networkx      |
|------------|------------|----------------------|-------------------|-------------------|
| 4          | 2          |      2 vertices      |     2 vertices    |     3 vertices    |
|            |            |       0.04 ms        |       0.03 ms     |       0.02 ms     |
| 8 + 100.0% | 6 + 200.0% |      4 vertices      |     4 vertices    |     5 vertices    |
|            |            |  0.76 ms + 1961.2%   |  0.04 ms + 34.2%  |  0.02 ms - 18.2%  |
| 12 + 50.0% | 11 + 83.3% |      5 vertices      |     5 vertices    |     7 vertices    |
|            |            |  12.59 ms + 1565.8%  |   0.04 ms + 0.2%  |  0.03 ms + 36.4%  |
| 16 + 33.3% | 11 + 0.0%  |      9 vertices      |    9 vertices     |    10 vertices    |
|            |            | 235.21 ms + 1767.9%  |  0.07 ms + 88.1%  |  0.03 ms + 15.5%  |
| 20 + 25.0% | 17 + 54.5% |      9 vertices      |    9 vertices     |    12 vertices    |
|            |            | 4962.32 ms + 2009.8% |  0.09 ms + 23.1%  |  0.03 ms + 13.5%  |
| 22 + 10.0% | 19 + 11.8% |     11 vertices      |    11 vertices    |    14 vertices    |
|            |            | 21415.71 ms + 331.6% |   0.12 ms + 37.8% |   0.04 ms + 4.5%  |

We can see as expected that the number of vertices returned by the exhaustive search is smaller than the Networkx version, however the elapsed time is much larger even for small increases in the size of the graph, for example in the last row, the increase in vertices was 10% and edges 11.8%, however, the elapsed time increased by 331.6%.

The exhaustive algorithm is therefore experimentally comproved to be exponential while both the Greedy and Networkx can only be concluded that they are not exponential.

### Greedy Heuristics

The greedy algorithm has a much better ratio between being computationally fast and having a good solution, remaining always better than the Networkx however, being slower as seen bellow.
When not applying the pós-processing we get worse but faster results as expected.

|    Vertices    |     Edges      | Greedy w pós-processing | Greedy w/out pós-processing |      Networkx     |
|----------------|----------------|-------------------------|-----------------------------|-------------------|
|  125           | 289            |     38 vertices         |     45 vertices             |    49 vertices    |
|                |                |       1.41 ms           |       0.57 ms               |      0.11 ms      |
|  250 + 100.0%  | 622 + 115.2%   |     74 vertices         |     84 vertices             |    95 vertices    |
|                |                |   5.66 ms + 299.9%      |   1.92 ms + 236.8%          |  0.17 ms + 58.5%  |
|  500 + 100.0%  | 1274 + 104.8%  |     139 vertices        |     167 vertices            |    188 vertices   |
|                |                |  22.35 ms + 295.2%      |   7.67 ms + 299.6%          |  0.35 ms + 98.3%  |
| 1000 + 100.0%  | 2562 + 101.1%  |     290 vertices        |     328 vertices            |    353 vertices   |
|                |                |  90.96 ms + 306.9%      |   32.63 ms + 325.4%         |  0.64 ms + 84.1%  |
| 2000 + 100.0%  | 5063 + 97.6%   |     570 vertices        |     647 vertices            |    744 vertices   |
|                |                |  345.44 ms + 279.8%     | 130.22 ms + 299.0%          |  1.32 ms + 108.1% |
| 4000 + 100.0%  | 10020 + 97.9%  |    1147 vertices        |    1303 vertices            |   1482 vertices   |
|                |                |  1428.48 ms + 313.5%    | 513.64 ms + 294.4%          | 2.88 ms + 117.3%  |
| 8000 + 100.0%  | 20063 + 100.2% |    2319 vertices        |    2671 vertices            |  2958 vertices    |
|                |                | 6024.52 ms + 321.7%     | 2164.56 ms + 321.4%         | 5.84 ms + 102.8%  |


A table with the basic operations is presented as follows

|    Vertices    |     Edges      |   Greedy w pós-processing    | Greedy w/out pós-processing |
|----------------|----------------|------------------------------|-----------------------------|
|  125           | 289            |     38 vertices              |     45 vertices             |
|                |                |        1410 b/o              |        1118 b/o             |
|  250 + 100.0%  | 622 + 113.5%   |     74 vertices              |     84 vertices             |
|                |                |        3104 b/o + 120.1%     |        2484 b/o + 122.2%    |
|  500 + 100.0%  | 2551 + 104.6%  |     139 vertices             |     167 vertices            |
|                |                |       6873 b/o + 121.4%      |        5473 b/o + 120.3%    |
| 1000 + 100.0%  | 1274 + 100.9%  |     290 vertices             |     328 vertices            |
|                |                |       15019 b/o + 118.5%     |       11950 b/o + 118.3%    |
| 2000 + 100.0%  | 5063 + 97.6%   |     570 vertices             |     647 vertices            |
|                |                |       32628 b/o + 117.2%     |       25905 b/o + 116.8%    |
| 4000 + 100.0%  | 10020 + 97.9%  |    1147 vertices             |    1303 vertices            |
|                |                |       70594 b/o + 116.4%     |       55809 b/o + 115.44%   |
| 8000 + 100.0%  | 20063 + 100.2% |    2319 vertices             |    2671 vertices            |
|                |                |       152698 b/o + 116.3%    |       119623 b/o + 114.34%  |



# Conclusion

In conclusion the minimum dominating set implemented in this project while it is not as fast as the dominating set function of the Networkx library, it is still very fast and provides much better results while still providing $ n log{n} $ complexity.
