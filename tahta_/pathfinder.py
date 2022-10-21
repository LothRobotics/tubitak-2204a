# TODO: TRY DIJKSTRA'S ALGORTIHM
# https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
# undirected graph = x can go to y and y can go to x
# directed graph = the way that each node can travel to is defined, x can go to y but maybe y cant go to x 
# https://www.youtube.com/watch?v=pVfj6mxhdMw

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

import random,sys,json
 
class Pathfinder():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] #for each vertex
                      for row in range(vertices)] #neighbors of that vertex
 
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
 
            print(f"{cout} {x}")
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

def test(vertex_count:int):
    g = Pathfinder(vertex_count) #when we give 9 this means that there are 9 vertices
    # each list in this list contains the dist to the other vertexes
    g.graph = []
    for _ in range(vertex_count):
        line = []
        for i in range(vertex_count):
            line.append(random.randint(0,vertex_count-1))
        line[random.randint(0,len(line)-1)] = 2 #make sure that there is at least 1 path from a vertex to another vertex
        g.graph.append(line)

    g.dijkstra(random.randint(0,vertex_count-1))

# st = time.time()
# for _ in range(100):
#     test(100)
# print(f"it took {time.time()-st}") # It took 6.4 seconds for 100 loops on 100 Vertex sized maps so this is fast enough

def LoadMap(path:str):
    with open(path,"r") as file:
        data = json.load(file)
    
    pathfinder = Pathfinder(len(data)) #when we give 9 this means that there are 9 vertices
    pathfinder.graph = data
    pathfinder.dijkstra(0)

#LoadMap("testmap.json")


class PathFinder3:
    def __init__(self) -> None:
        pass 
    def load_map(self,path:str):
        with open(path,"r") as file:
            data = json.load(file)
        
        self.map = data
    
    def run(self):
        pass


        





