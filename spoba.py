"""importing"""
import random
import time
from itertools import combinations, groupby
import networkx as nx
import matplotlib.pyplot as plt
def gnp_random_connected_graph(num_of_nodes: int,
                               completeness: int,
                               directed: bool = False,
                               draw: bool = False):
    """
    Generates a random graph, similarly to an Erdős-Rényi 
    graph, but enforcing that the resulting graph is conneted (in case of undirected graphs)
    """
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    edges = combinations(range(num_of_nodes), 2)
    G.add_nodes_from(range(num_of_nodes))  
    for _, node_edges in groupby(edges, key = lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        if random.random() < 0.5:
            random_edge = random_edge[::-1]
        G.add_edge(*random_edge)
        for e in node_edges:
            if random.random() < completeness:
                G.add_edge(*e)
    for (u, v, w) in G.edges(data=True):
        w['weight'] = random.randint(-5, 20)
    if draw: 
        plt.figure(figsize=(10,6))
        if directed:
            pos = nx.arf_layout(G)
            nx.draw(G, pos, node_color='lightblue',
                    with_labels=True,
                    node_size=500,
                    arrowsize=20,
                    arrows=True)
            labels = nx.get_edge_attributes(G,'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        else:
            nx.draw(G, node_color='lightblue',
                    with_labels=True,
                    node_size=500)
    return G

class Kruskal:
    """Class to make algoritm"""
    def __init__(self, graph) -> None:
        """Kruskall init"""
        self.graph = graph
        self.vertices = {i: i for i in range(len(graph.nodes))}
        self.edges = list(graph.edges)
        self.edges.sort(key=lambda edge: graph[edge[0]][edge[1]]['weight'])
        self.minimum_spanning_tree = []
    def find(self, vertex):
        """finding roots for vertexes"""
        if self.vertices[vertex] != vertex:
            self.vertices[vertex] = self.find(self.vertices[vertex])
        return self.vertices[vertex]
    def union(self, u, v):
        """uniting roots in trees, уникаємо циклів"""
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            self.vertices[root_u] = root_v
    def kruskal_algorithm(self):
        """Створює фінальний каркас"""
        for edge in self.edges:
            u, v = edge
            if self.find(u) != self.find(v):
                self.minimum_spanning_tree.append(edge)
                self.union(u, v)
        return self.minimum_spanning_tree

G = gnp_random_connected_graph(2000, 1, False, False)
kruskal = Kruskal(G)
time_start=time.time()
minimum_spanning_tree = kruskal.kruskal_algorithm()
end_time=time.time()
for edge in minimum_spanning_tree:
    print(edge)
print(end_time-time_start)
