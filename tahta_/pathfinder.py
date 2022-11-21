
import sys,json
from typing import List

class PathFinder2:
    def __init__(self) -> None:
        pass

    def loadMap(self,path:str):
        with open(path,"r") as file:
            self.data = json.load(file)
            self.vertex_count = len(self.data)

    def minDistance(self,dist, alreadyvisited):
        min_v = sys.maxsize
        min_index = 0
        for u in range(self.vertex_count):
            if dist[u] < min_v and alreadyvisited[u] == False:
                min_v = dist[u]
                min_index = u

        return min_index

    def run(self, source:int):
        """Run the algorithm

        Args:
            source (int): destination
        """
        self.distances = [sys.maxsize] * self.vertex_count # create a list that contains the distances of every vertex
        self.distances[source] = 0 # set the source distance to 0 to make the algorithm start at this one 
        alreadyvisited = [False] * self.vertex_count #contains if we've already visited the node

        for i in range(self.vertex_count):
            nodeid = self.minDistance(self.distances, alreadyvisited)
            #print(f"{i}: {nodeid}")

            alreadyvisited[nodeid] = True #write that we've visited this place

            for t in range(self.vertex_count):
                neighbours:List[int] = self.data[nodeid]
                if neighbours.__contains__(t):
                    print(f"{t} is contained in {neighbours}")
                    sth = t
                else:
                    sth = False
                #if connection does exist and we haven't visited it before and  distance is bigger than the nodeid + connection 
                if sth != False:
                    if sth > 0 and alreadyvisited[t] == False and self.distances[t] > self.distances[nodeid] + sth: 
                        self.distances[t] = self.distances[nodeid] + 1 #sth
                elif sth == False:
                    pass


        for nodeid in range(self.vertex_count):
            print(f"{nodeid} dist: {self.distances[nodeid]} ")


pathfinder = PathFinder2()
pathfinder.loadMap("testmap.json")
pathfinder.run(0)