# -*- coding: utf-8 -*-
# autores:
#   - Victor José Figueira
# data:
#   - 09/06/2018

# Editado por:
#   - Gabriel Choptian
# Arquivos editados:
#   - data: [data] função: [função/ classe]
#   nada

import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.G = nx.Graph()

    def addNode(self, node):
        self.G.add_node(node)

    def removeNode(self, node):
        self.G.remove_node(node)

    def addEdge(self, node1, node2, weight=None):
        if (weight == None):
            self.G.add_edge(node1, node2)
        else:
            self.G.add_edge(node1, node2, weight=float(weight))

    def getEdgeWeight(self, node1, node2):
        return self.G[node1][node2]['weight']

    def setEdgeWeight(self, node1, node2, weight):
        self.G[node1][node2]['weight'] = float(weight)

    def removeEdge(self, node1, node2):
        self.G.remove_edge(node1, node2)

    def getNode(self, node):
        return self.G.node[node]

    def getEdge(self, node1, node2):
        return self.G[node1][node2]

    def getOrder(self):
        return (self.G.number_of_nodes())

    def numberOfEdges(self):
        return (self.G.number_of_edges())

    def getNodes(self):
        return (list(self.G.nodes))

    def getEdges(self):
        return (list(self.G.edges))

    def getDegree(self, node):
        return (self.G.degree[node])

    def getAdjacent(self, node):
        return (list(self.G.adj[node]))

    def numberOfAdjacent(self, node):
        return (len(self.getAdjacent(node)))

    def isComplete(self):
        nodes = self.getNodes()
        for node in nodes:
            count = 0
            adj_list = self.getAdjacent(node)
            for adj in adj_list:
                if (adj == node):
                    pass
                else:
                    count = count + 1
            if (count != (self.getOrder() - 1)):
                return False
        return True

    def isConnected(self):
        return (nx.is_connected(self.G))

    def isTree(self):
        return (nx.is_tree(self.G))

    def display(self):
        nx.draw(self.G, with_labels=True, font_weight='bold')
        plt.show()

    def BFS(self, node):
        queue = []
        color = {}
        distance = {}
        predecessor = {}
        for i in self.getNodes():
            color[i] = "w"
            distance[i] = "-1"
            predecessor[i] = None
        color[node] = "g"
        distance[node] = 0
        queue.append(node)
        while queue:
            U = queue.pop(0)
            for no in self.getAdjacent(U):
                if (color[no] == "w"):
                    color[no] = "g"
                    distance[no] = distance[U] + 1
                    predecessor[no] = U
                    queue.append(no)
            color[U] = "b"
        return distance

    def dijkstra(self, source, dest, path=True, cost=True):
        if (path and cost):
            return (nx.dijkstra_path(self.G, source, dest), nx.dijkstra_path_length(self.G, source, dest))
        elif (path):
            return (nx.dijkstra_path(self.G, source, dest))
        elif (cost):
            return (nx.dijkstra_path_length(self.G, source, dest))

    def getReachables(self, node):
        return nx.descendants(self.G, node)


class DiGraph(Graph):
    def __init__(self):
        self.G = nx.DiGraph()

    def isConnected(self):
        return (nx.is_strongly_connected(self.G))

    def getFTD(self, node):
        return nx.descendants(self.G, node)

    def getFTI(self, node):
        return nx.ancestors(self.G, node)

    def getInDegree(self, node):
        return self.G.in_degree(node)

    def getOutDegree(self, node):
        return self.G.out_degree(node)

    def isDAG(self):
        return nx.is_directed_acyclic_graph(self.G)

    def someTopologicalSort(self):
        return (list(reversed(list(nx.topological_sort(self.G)))))
