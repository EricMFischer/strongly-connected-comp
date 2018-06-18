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
# output: object with vertex keys and their head vertices
def preprocess_adj_list(filename):
    graph_obj = {}
    with open(filename) as f_handle:
        for line in f_handle:
            u, v = line.split()
            u = int(u)
            v = int(v)
            graph_obj.setdefault(u, []).append(v)

            # dont forget nodes with no outgoing arcs
            if v not in graph_obj:
                graph_obj.setdefault(v, [])

    return graph_obj


# input: object with vertex keys and their head vertices
# output: Graph instantiated with input graph object
def create_graph(graph_obj):
    G = Graph()
    for v_key in graph_obj:
        v = Vertex(v_key) if v_key not in G else G.get_v(v_key)
        for head_key in graph_obj[v_key]:
            # v gets a tail_of value of head_key (useful for normal graph traversal)
            v.add_head(head_key)

            # v_head gets a head_of value of v_key (useful for traversing graph backwards)
            v_head = Vertex(head_key) if head_key not in G else G.get_v(head_key)
            v_head.add_tail(v_key)
            G.add_v(v_head)

        G.add_v(v)
    return G


# Vertex class for directed graphs (object with 'key', 'tail_of', and 'head_of' keys)
class Vertex(object):
    def __init__(self, key):
        self.key = key
        self.tail_of = {}
        self.head_of = {}

    def __str__(self):
        return '{' + "'key': '{}', 'tail_of': {}, 'head_of': {}".format(
            self.key,
            self.tail_of,
            self.head_of
        ) + '}'

    def add_head(self, head_key, weight=1):
        if (head_key):
            self.tail_of[head_key] = weight

    def add_tail(self, tail_key, weight=1):
        if (tail_key):
            self.head_of[tail_key] = weight

    def tail_of(self, head_key):
        return head_key in self.tail_of

    def head_of(self, tail_key):
        return tail_key in self.head_of

    def get_tail_of_keys(self):
        return list(self.tail_of.keys())

    def get_head_of_keys(self):
        return list(self.head_of.keys())

    def remove_tail(self, tail_key):
        if tail_key in self.head_of:
            del self.head_of[tail_key]

    def remove_head(self, head_key):
        if head_key in self.tail_of:
            del self.tail_of[head_key]

    def get_tail_weight(self, tail_key):
        if tail_key in self.head_of:
            return self.head_of[tail_key]

    def get_head_weight(self, head_key):
        if head_key in self.tail_of:
            return self.tail_of[head_key]


# Graph class for directed graphs
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
        for v in vertices:
            graph_key = "'{}'".format(v.key)
            v_str = "\n   'key': '{}', \n   'tail_of': {}, \n   'head_of': {}".format(
                v.key,
                v.tail_of,
                v.head_of
            )
            output += ' ' + graph_key + ': {' + v_str + '\n },\n'
        return output + '}'

    def add_v(self, v):
        if v:
            self.vertices[v.key] = v
        return self

    def get_v(self, key):
        try:
            return self.vertices[key]
        except KeyError:
            return None

    def get_v_keys(self):
        return list(self.vertices.keys())

    # removes vertex as head and tail from all its neighbors, then deletes vertex
    def remove_v(self, key):
        if key in self.vertices:
            head_of_keys = self.vertices[key].get_head_of_keys()
            tail_of_keys = self.vertices[key].get_tail_of_keys()
            for tail_key in head_of_keys:
                self.remove_head(tail_key, key)
            for head_key in tail_of_keys:
                self.remove_tail(key, head_key)
            del self.vertices[key]
        return self

    def add_edge(self, tail_key, head_key, weight=1):
        if tail_key not in self.vertices:
            self.add_v(Vertex(tail_key))
        if head_key not in self.vertices:
            self.add_v(Vertex(head_key))

        self.vertices[tail_key].add_head(head_key, weight)
        self.vertices[head_key].add_tail(tail_key, weight)

    # adds the weight for an edge if it exists already, with a default of 1
    def increase_edge(self, tail_key, head_key, weight=1):
        if tail_key not in self.vertices:
            self.add_v(Vertex(tail_key))
        if head_key not in self.vertices:
            self.add_v(Vertex(head_key))

        weight_v1_v2 = self.get_v(tail_key).get_head_weight(head_key)
        new_weight_v1_v2 = weight_v1_v2 + weight if weight_v1_v2 else weight

        weight_v2_v1 = self.get_v(head_key).get_tail_weight(tail_key)
        new_weight_v2_v1 = weight_v2_v1 + weight if weight_v2_v1 else weight

        self.vertices[tail_key].add_head(head_key, new_weight_v1_v2)
        self.vertices[head_key].add_tail(tail_key, new_weight_v2_v1)
        return self

    def has_forward_edge(self, tail_key, head_key):
        if tail_key in self.vertices:
            return self.vertices[tail_key].tail_of(head_key)

    def remove_edge(self, tail_key, head_key):
        if tail_key in self.vertices:
            self.vertices[tail_key].remove_head(head_key)
        if head_key in self.vertices:
            self.vertices[head_key].remove_tail(tail_key)

    def remove_tail(self, tail_key, head_key):
        if head_key in self.vertices:
            self.vertices[head_key].remove_tail(tail_key)

    def remove_head(self, tail_key, head_key):
        if tail_key in self.vertices:
            self.vertices[tail_key].remove_head(head_key)

    def for_each_v(self, cb):
        for v in self.vertices:
            cb(v)


# Global variables
EXPLORED = {}
# 1st DFS loop
t = 0  # increment when a node and its children have been fully explored
F = []  # tracks node finishing times (e.g. [x,y,z] for 3 nodes labeled 1, 2, and 3)

# 2nd DFS loop
S = []  # append a node before DFS_G subroutine is called from it
LEADERS = {}  # tracks node "leaders", i.e. node DFS_G was called from to discover them


# input: Graph, vertex key, iteration of DFS loop (1st or 2nd)
def DFS_G(G, v_key, loop):
    global t, EXPLORED
    EXPLORED[v_key] = 1

    # Leader of a vertex is its DFS_G subroutine source vertex
    if loop is 2:
        LEADERS[v_key] = S[-1]

    v = G.get_v(v_key)
    v_heads = v.get_tail_of_keys() if loop is 2 else v.get_head_of_keys()  # hmm
    for v_head in v_heads:
        if v_head not in EXPLORED:
            DFS_G(G, v_head, loop)

    # When v_key has no more outoing arcs, t++ and record t as its finishing time
    if loop is 1:
        t += 1
        F[v_key - 1] = t  # vector opt. of F assumes node labels are integers and 1-indexed


# input: Graph, iteration of DFS loop (1 or 2)
def DFS_loop(G, loop):
    global F, S, EXPLORED
    EXPLORED = {}

    if loop is 1:
        keys = G.get_v_keys()
        F = [None] * len(keys)
        sorted_keys = list(reversed(keys))
    else:
        # Sorts nodes in reverse topological order, i.e. descending order of finishing times
        i = [b[0] for b in sorted(enumerate(F), key=lambda i:i[1], reverse=True)]
        sorted_keys = [x + 1 for x in i]
        print('reverse toplogical order: ', sorted_keys)

    for v_key in sorted_keys:
        if v_key not in EXPLORED:
            if loop is 2:
                S.append(v_key)
            DFS_G(G, v_key, loop)


# input: Graph and number of SCC sizes to return
# output: size of 5 largest SCCs
def strongly_connected_components(G, num):
    # 1) Run DFS loop on G with reversed arcs to gather the searched finishing times of nodes in F
    DFS_loop(G, 1)
    print('F: ', F)
    print('t: ', t)

    # 1b) Now that we have the searched order finishing times of the first DFS, replace vertex keys
    # (i.e. node labels) with these rankings, so that when we now traverse the graph in the forward
    # direction, but again in the order of n to 1 (which will thus be in decreasing order of
    # finishing times), we'll start at the right nodes to find only 1 strongly connected component
    # at a time (marking as 'explored' nodes that are part of 1 SCC so we don't ever call DFS from
    # them in DFS_loop), potentially even starting with sink vertices which have no outgoing arcs
    # and are thus their own SCC.

    # 2) Run DFS loop on G such that keys of vertices are replaced by their finishing times
    DFS_loop(G, 2)
    print('S: ', S)
    print('LEADERS: ', LEADERS)
    return find_largest(num)


# Uses global 'leaders' object with vertex keys and their leader
# input: number of SCC sizes to return
# output: SCC sizes
def find_largest(num):
    SCCs = {}  # leader keys and their SCC size
    for v in LEADERS:
        leader = LEADERS[v]
        SCCs[leader] = SCCs.get(leader, 0) + 1
    print('SCCs: ', SCCs)

    sizes = sorted(SCCs.values(), reverse=True)[:num]
    result = sizes + ([0] * (num - len(sizes)))
    return result


graph_obj = preprocess_adj_list('scc_test_1.txt')
pprint.pprint(graph_obj, width=40)

graph = create_graph(graph_obj)
print(graph)

result = strongly_connected_components(graph, 5)
print(result)
