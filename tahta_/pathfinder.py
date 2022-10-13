# TODO: TRY DIJKSTRA'S ALGORTIHM
# https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
# undirected graph = x can go to y and y can go to x
# directed graph = the way that each node can travel to is defined, x can go to y but maybe y cant go to x 
# https://www.youtube.com/watch?v=pVfj6mxhdMw

# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph
 
# Library for INT_MAX
import random
import sys
import time
 
class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
 
    def printSolution(self, dist, index):
        print(f"Wanted Vertex:{index} \nVertex \tDistance from Source")
        for node in range(self.V):
            print(node, "\t", dist[node])
 
    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
 
        # Initialize minimum distance for next node
        min = sys.maxsize
 
        # Search not nearest vertex not in the
        # shortest path tree
        for u in range(self.V):
            if dist[u] < min and sptSet[u] == False:
                min = dist[u]
                min_index = u
        
        return min_index
 
    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    # src is either wanted destination or start destination
    def dijkstra(self, src):
 
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V #this list is empty at start 
 
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # x is always equal to src in first iteration
            x = self.minDistance(dist, sptSet)
 
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[x] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for y in range(self.V):
                if self.graph[x][y] > 0 and sptSet[y] == False and \
                        dist[y] > dist[x] + self.graph[x][y]:
                    dist[y] = dist[x] + self.graph[x][y]
 
        self.printSolution(dist,src)
 
 
# Driver's code

# st = time.time()
# g = Graph(9) #when we give 9 this means that there are 9 vertices
# # each list in this list contains the dist to the other vertexes
# g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
#             [4, 0, 8, 0, 0, 0, 0, 11, 0],
#             [0, 8, 0, 7, 0, 4, 0, 0, 2],
#             [0, 0, 7, 0, 9, 14, 0, 0, 0],
#             [0, 0, 0, 9, 0, 10, 0, 0, 0],
#             [0, 0, 4, 14, 10, 0, 2, 0, 0],
#             [0, 0, 0, 0, 0, 2, 0, 1, 6],
#             [8, 11, 0, 0, 0, 0, 1, 0, 7],
#             [0, 0, 2, 0, 0, 0, 6, 7, 0]]
# g.dijkstra(2)


def a(vertex_count:int):
    g = Graph(vertex_count) #when we give 9 this means that there are 9 vertices
    # each list in this list contains the dist to the other vertexes
    g.graph = []
    for _ in range(vertex_count):
        line = []
        for i in range(vertex_count):
            line.append(random.randint(0,vertex_count-1))
        g.graph.append(line)

    g.dijkstra(random.randint(0,vertex_count-1))

for _ in range(100): #TODO: fix the function so it doesnt prduce broken results
    st = time.time()
    a(5)
    print(f"it took {time.time()-st}")
# This code is contributed by Divyanshu Mehta and Updated by Pranav Singh Sambyal

# a dictionary containing an end, start and also other nodes, we ideally would want to be able to change 
# start node easily and it also needs to be fast so we might need to rewrite it in c/cpp/rust etc


# 
# Create a set sptSet (shortest path tree set) that keeps track of vertices included in the shortest-path tree, i.e., 
# whose minimum distance from the source is calculated and finalized. Initially, this set is empty. 
# Assign a distance value to all vertices in the input graph. Initialize all distance values as INFINITE. 
# Assign the distance value as 0 for the source vertex so that it is picked first. 
# While sptSet doesn’t include all vertices 
#     Pick a vertex u which is not there in sptSet and has a minimum distance value. 
#     Include u to sptSet. 
#     Then update distance value of all adjacent vertices of u. 
#         To update the distance values, iterate through all adjacent vertices. 
#         For every adjacent vertex v, if the sum of the distance value of u (from source) and weight of edge u-v, is less than the distance value
#         of v, then update the distance value of v. 

# Note: We use a boolean array sptSet[] to represent the set of vertices included in SPT. If a value sptSet[v] is true, then vertex v 
# is included in SPT, otherwise not. Array dist[] is used to store the shortest distance values of all vertices.



