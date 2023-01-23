import sys
import json
from typing import List
import time


class PathFinder:
    def __init__(self) -> None:
        # contains connections and distances if I remember correctly
        self.data = []  # equal to self.map in pathmaker
        self.typedata = {}

    def loadMap(self, path: str):
        with open(path, "r") as file:
            rawdata = json.load(file)

        self.data = rawdata["map"]

        self.typedata = {}
        for id, val in enumerate(rawdata["typemap"].values()):
            # key is actually just the node id but in string
            self.typedata[id] = val

        self.vertex_count = len(self.data)

    def minDistance(self, dist, alreadyvisited):
        min_v = sys.maxsize
        min_index = 0
        for u in range(self.vertex_count):
            if dist[u] < min_v and alreadyvisited[u] is False:
                min_v = dist[u]
                min_index = u

        return min_index

    def run(self, source: int):
        """Run the algorithm

        Args:
            source (int): destination
        """
        self.distances = [
            sys.maxsize] * self.vertex_count  # create a list that contains the distances of every vertex
        # set the source distance to 0 to make the algorithm start at this one
        self.distances[source] = 0
        # contains if we've already visited the node
        alreadyvisited = [False] * self.vertex_count

        for i in range(self.vertex_count):
            nodeid = self.minDistance(self.distances, alreadyvisited)
            # print(f"{i}: {nodeid}")

            # write that we've visited this place
            alreadyvisited[nodeid] = True

            for t in range(self.vertex_count):
                neighbours: List[int] = self.data[nodeid]
                if neighbours.__contains__(t):
                    print(f"{t} is contained in {neighbours}")
                    sth = t
                else:
                    sth = False
                # if connection does exist and we haven't visited it before and  distance is bigger than the nodeid + connection
                if sth is not False:
                    if sth > 0 and alreadyvisited[t] is False and self.distances[t] > self.distances[nodeid] + sth:
                        self.distances[t] = self.distances[nodeid] + 1  # sth
                elif sth is False:
                    pass

        for nodeid in range(self.vertex_count):
            print(f"{nodeid} dist: {self.distances[nodeid]} ")

    def OLD_simple_run(self, startnode, endnode):
        distances = [sys.maxsize] * self.vertex_count
        distances[startnode] = 0
        previous = {node: None for node in range(self.vertex_count)}
        visited = [False] * self.vertex_count
        heap = [(0, startnode)]

        currentnode = startnode
        while True:
            for neighbor in self.data[currentnode]:
                potential = (distances[currentnode] + 1)
                if potential < distances[neighbor]:
                    distances[neighbor] = potential
                    print(f"lowered dist of node:{neighbor} to {potential}")
            visited[currentnode] = True

            minimum_index = currentnode
            val = sys.maxsize
            for index, dist in enumerate(distances):
                if dist < val and visited[index] is False:
                    minimum_index = index
                    val = dist
                    previous[neighbor] = currentnode
                    heap.append((dist, neighbor))
                    print(f"new minimum:{val} index:{minimum_index}")
            currentnode = minimum_index
            if visited[endnode] is True:
                print("WOOHOO FINALLY FOUND IT")
                print(distances, visited, previous)
                break
            print("end of cycle")

    def simple_run(self, start, end):
        # Initialize the heap with the starting node and set its distance to 0
        heap = [(0, start)]
        # create dictionary to store distances from the start node to each node
        distances = {node: float('inf') for node in range(self.vertex_count)}
        distances[start] = 0
        # Initialize a dictionary to store the previous node for each node in the shortest path
        previous = {node: None for node in range(self.vertex_count)}

        while heap:
            min_element = min(heap)
            # Pop the node with the smallest distance from the heap
            heap.remove(min_element)
            current_distance, current_node = min_element
            # If the current node is the end node, we have found the shortest path
            if current_node == end:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = previous[current_node]
                return path[::-1]
            # Update the distances and previous nodes for each neighbor of the current node
            for neighbor in self.data[current_node]:
                weight = 1
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heap.append((distance, neighbor))
        return None


# Şöyle her sınıfın her farklı çıkışa olan uzaklığını hesaplayıp sonra
# en küçük uzaklıklarını karşılaştırıcaz. Böylece sınıf sıralı kaçış
# rotası oluşturulacak

    def calc_escape_nodes(self):
        escape_nodes = []
        print(self.typedata)
        for key, val in self.typedata.items():
            if val == "exit":
                escape_nodes.append(int(key))
                print(f"room: {key} is an exit.")
        return escape_nodes

    def calculate_escape_routes(self):
        results = {}
        escape_nodes = self.calc_escape_nodes()
        print(f"escape nodes: {escape_nodes}")
        for roomid in range(self.vertex_count):
            roomtype = self.typedata[roomid]
            if roomtype == "classroom":
                for escape_node in escape_nodes:
                    results[roomid] = self.simple_run(roomid, escape_node)
                    print(f" Clasroom of id:{roomid} results: {results[roomid]}")

        return results


if __name__ == "__main__":
    pathfinder = PathFinder()
    pathfinder.loadMap("testmap.json")
    results = pathfinder.calculate_escape_routes()
    print(results)
    # pathfinder.calculate_escape_routes()
