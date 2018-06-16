'''
The file contains the edges of a directed graph. Vertices are labeled as positive integers from
1 to 875714. Every row indicates an edge, the vertex label in first column is the tail and
the vertex label in second column is the head (recall the graph is directed, and the edges
are directed from the first column vertex to the second column vertex). So for example, the
11th row looks liks : "2 47646". This just means that the vertex with label 2 has an outgoing
edge to the vertex with label 47646.

Your task is to code up the algorithm from the video lectures for computing strongly
connected components (SCCs), and to run this algorithm on the given graph.

Output Format: You should output the sizes of the 5 largest SCCs in the given graph, in
decreasing order of sizes, separated by commas (avoid any spaces). So if your algorithm
computes the sizes of the five largest SCCs to be 500, 400, 300, 200 and 100, then your
answer should be "500,400,300,200,100" (without the quotes). If your algorithm finds less
than 5 SCCs, then write 0 for the remaining terms.

General Approach:
Here's how to do the vector f(t). Using Tim's example of the reversed 9 node graph (Grev) from
the lectures:
Initialize global variable t = 0. Initialize a stack data structure to empty. S = [ ].
Start at vertex 9. Add to stack, S = [ 9 ]. Mark 9 visited.
Always examine vertex at top of stack. 9 has outgoing edge to 6. So S.push(9). S = [ 9 6 ].
Mark 6 visited.
6 has outgoing edge 3. So, S.push(3). S = [ 9 6 3 ]. Mark 3 visited.
3 has no outgoing edge that has not yet been visited. So pop 3, increment t, and assign
f(3) = 1. Now t = 1 and S = [ 9 6 ].
6 has an outgoing edge that has not yet been visited. So push 8. S = [ 9 6 8 ]. Mark 8 visited.
Similarly, push 2 and 5. S = [ 9 6 8 2 5 ]. Mark 2 and 5 visited.
Now, examine top of stack as always. 5 has nothing outgoing that has not yet been visited, so
pop 5, increment t, assign f(5) = 2. Now t = 2 and S = [ 9 6 8 2 ].
Examine top of stack. 2 has nothing outgoing that has not yet been visited, so pop 2,
increment t, and assign f(2) = 3. Now t = 3.

And so on ...


Random Notes:
1) Iterative > recursive approach.
2) For running times, use stack to store the vertices. Dictionary for times.
3) Python list to represent graph and stacks. Thread stack size and recursion limit are important.
4) Don't forget to count vertices with no outgoing arcs. If building a dictionary,
with v -> e, e, e, such a dictionary should also contain vertices with no outgoing arcs.
5) import sys sys.setrecursionlimit(1000000)
6) Make sure to use iterative (for-loop) DFS implementation (BFS with stack instead of queue).
The non-trivial trick here is to get the finishing times in iterative algorithm (something
that you get for free with recursion).
7) if __name__ == '__main__':
sys.setrecursionlimit(2 ** 20)
threading.stack_size(2 ** 26)
thread = threading.Thread(target=DFS)
thread.start()
"When I moved on to the iterative version, I ran into the problem of counting finishing time
(not as simple as it is in case of recursion). Any Python-ers here have any suggestions on
how to either fix the global variable issues or correctly computing finishing time with
an iterative DFS?"
'''
import pprint


# input: file name
# output: object with vertex keys as keys and their neighbors as values
def preprocess_adj_list(filename):
    graph_object = {}
    with open(filename) as f_handle:
        for line in f_handle:
            u, v = line.split()
            u = int(u)
            v = int(v)
            graph_object.setdefault(u, []).append(v)
    return graph_object


# input: object with vertex keys as keys and their neighbors as values
# output: Graph object instantiated with input graph object
def create_graph(graph_obj):
    graph = Graph()
    for vertex_key in graph_obj:
        vertex = Vertex(vertex_key)
        for neighbor_key in graph_obj[vertex_key]:
            vertex.add_neighbor(neighbor_key)
        graph.add_vertex(vertex)
    return graph


# Vertex class (vertices are objects with 'key' and 'neighbors' keys)
# Modifying these Vertex objects can make the graph more robust
class Vertex(object):
    def __init__(self, key):
        self.key = key
        self.neighbors = {}

    def __str__(self):
        return '{' + "'key': '{}', 'neighbors': {}".format(
            self.key,
            self.neighbors
        ) + '}'

    def add_neighbor(self, neighbor_key, weight=1):
        if (neighbor_key):
            self.neighbors[neighbor_key] = weight

    def has_neighbor(self, neighbor_key):
        return neighbor_key in self.neighbors

    def get_neighbor_keys(self):
        return list(self.neighbors.keys())

    def remove_neighbor(self, neighbor_key):
        if neighbor_key in self.neighbors:
            del self.neighbors[neighbor_key]

    def get_weight(self, neighbor_key):
        if neighbor_key in self.neighbors:
            return self.neighbors[neighbor_key]


# Graph class
# Note: to maximize applications, add_edge, increase_edge, and remove_edge only add or remove an
# edge for the 'from' vertex, and 'has_edge' only checks the 'from' vertex.
class Graph(object):
    def __init__(self):
        self.vertices = {}

    # 'x in graph' will use this containment logic
    def __contains__(self, key):
        return key in self.vertices

    # 'for x in graph' will use this iter() definition, where x is a vertex in an array
    def __iter__(self):
        return iter(self.vertices.values())

    def __str__(self):
        output = '\n{\n'
        vertices = self.vertices.values()
        for vertex in vertices:
            graph_key = "'{}'".format(vertex.key)
            vertex_str = "\n   'key': '{}', \n   'neighbors': {}".format(
                vertex.key,
                vertex.neighbors
            )
            output += ' ' + graph_key + ': {' + vertex_str + '\n },\n'
        return output + '}'

    def add_vertex(self, vertex):
        if vertex:
            self.vertices[vertex.key] = vertex
        # temporary logic
        return self

    def get_vertex(self, key):
        try:
            return self.vertices[key]
        except KeyError:
            return None

    def get_vertices_keys(self):
        return list(self.vertices.keys())

    # removes vertex as neighbor from all its neighbors, then deletes vertex
    def remove_vertex(self, key):
        if key in self.vertices:
            neighbor_keys = self.vertices[key].get_neighbor_keys()
            for neighbor_key in neighbor_keys:
                self.remove_edge(neighbor_key, key)
            del self.vertices[key]
        # temporary logic
        return self

    # overwrites the weight for an edge if it exists already, with a default of 1
    def add_edge(self, from_key, to_key, weight=1):
        if from_key not in self.vertices:
            self.add_vertex(Vertex(from_key))
        if to_key not in self.vertices:
            self.add_vertex(Vertex(to_key))

        self.vertices[from_key].add_neighbor(to_key, weight)

    # adds the weight for an edge if it exists already, with a default of 1
    def increase_edge(self, from_key, to_key, weight=1):
        if from_key not in self.vertices:
            self.add_vertex(Vertex(from_key))
        if to_key not in self.vertices:
            self.add_vertex(Vertex(to_key))

        weight_v1_v2 = self.get_vertex(from_key).get_weight(to_key)
        new_weight_v1_v2 = weight_v1_v2 + weight if weight_v1_v2 else weight

        self.vertices[from_key].add_neighbor(to_key, new_weight_v1_v2)
        # temporary logic
        return self

    def has_edge(self, from_key, to_key):
        if from_key in self.vertices:
            return self.vertices[from_key].has_neighbor(to_key)

    def remove_edge(self, from_key, to_key):
        if from_key in self.vertices:
            self.vertices[from_key].remove_neighbor(to_key)

    def for_each_vertex(self, cb):
        for vertex in self.vertices:
            cb(vertex)


# Global variables for strongly connected components algorithm
explored = {}


# input: a Graph and vertex
def DFS(G, v):
    explored[v] = 1


# input: a Graph
def DFS_loop(G):
    # Compute t, number of nodes so far processed, for finishing times during first DFS on Grev
    t = 0

    # Compute s, most recent "leader" vertex from which DFS was called, during second DFS on G
    # Topologically order nodes in decreasing order of finishing times
    s = None

    G_rev_keys = list(reversed(G.vertices.keys()))
    for v in G_rev_keys:
        if v not in explored:
            s = v  # tracks current source vertex for DFS call
            DFS(G, v)


# input: a Graph
# output: size of the 5 largest SCCs (e.g. [500,400,300,200,100])
def strongly_connected_components(G):
    # 1) Run DFS loop on G in reverse
    Grev = {}  # to do
    DFS_loop(Grev)

    # 2) Run DFS loop again on original graph G
    DFS_loop(G)

    return []  # return 5 largest SCCs


graph_object = preprocess_adj_list('scc_test_1.txt')
pprint.pprint(graph_object, width=260)

graph = create_graph(graph_object)







