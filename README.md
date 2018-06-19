## Synopsis
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

## Motivation
Kosaraju's strongly connected components algorithm for directed acyclic graphs has *O(m+n)* time complexity and demonstrates the utility of sink vertices for finding the maximal number of strongly connected components in a directed graph. Note that this algorithm is one the 4 free primitive operations for computing useful information about a graph in linear time.

## Acknowledgements

This algorithm is part of the Stanford University Algorithms 4-Course Specialization on Coursera, instructed by Tim Roughgarden.
